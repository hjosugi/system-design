"""Consistent hashing ring with virtual nodes.

This is a runnable implementation drill for the classic system-design building
block used by sharded caches (memcached/Ketama), distributed key-value stores
(Dynamo/Cassandra/Riak), and request routers.

The whole point of consistent hashing: when a server is added or removed, only
a small fraction of keys (roughly 1/N of the keyspace, where N is the number of
nodes) move to a different server. Naive `hash(key) % len(nodes)` instead remaps
almost every key because changing the divisor reshuffles the entire mapping.

Run `python3 consistent_hash.py` to see distribution + remap stats, and a
side-by-side comparison against modulo hashing.
"""

from __future__ import annotations

import bisect
import hashlib
from collections import Counter
from dataclasses import dataclass, field


def stable_hash(key: str) -> int:
    """Map an arbitrary string to a 32-bit point on the ring.

    We use md5 (via hashlib) because it is stable across processes and Python
    versions. Python's built-in hash() is salted per-process (PYTHONHASHSEED),
    so it is unsuitable for a ring that must be reproducible across machines.

    md5 is used purely as a fast, well-distributed mixing function here; this is
    a placement decision, not a security boundary, so its cryptographic
    weaknesses do not matter. We keep the low 32 bits to make the ring small and
    easy to reason about.
    """
    digest = hashlib.md5(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


@dataclass
class ConsistentHashRing:
    """A hash ring with configurable virtual nodes (replicas) per physical node.

    Each physical node is placed at `replicas` points around the ring. A key is
    assigned to the first node found walking clockwise (increasing hash) from the
    key's position, wrapping around at the top. Walking is done with bisect over
    a sorted list of ring positions, so lookups are O(log V) where V is the total
    number of virtual nodes.

    More virtual nodes => smoother distribution, because each physical node owns
    many small arcs instead of one large arc whose size depends on luck.
    """

    replicas: int = 100
    # Sorted list of virtual-node hash positions (the ring).
    _ring: list[int] = field(default_factory=list, init=False, repr=False)
    # Maps a ring position back to the physical node name that owns it.
    _position_to_node: dict[int, str] = field(default_factory=dict, init=False, repr=False)
    _nodes: set[str] = field(default_factory=set, init=False, repr=False)

    def _vnode_key(self, node: str, replica_index: int) -> str:
        # Distinct label per virtual node so its ring position is independent of
        # the other replicas of the same physical node.
        return f"{node}#{replica_index}"

    def add_node(self, node: str) -> None:
        """Place a physical node on the ring as `replicas` virtual nodes."""
        if node in self._nodes:
            return
        self._nodes.add(node)
        for i in range(self.replicas):
            position = stable_hash(self._vnode_key(node, i))
            # Collisions are astronomically rare with a good hash, but if two
            # vnodes land on the same point we just skip the duplicate; the ring
            # stays correct, that node simply has one fewer arc.
            if position in self._position_to_node:
                continue
            self._position_to_node[position] = node
            bisect.insort(self._ring, position)

    def remove_node(self, node: str) -> None:
        """Remove all virtual nodes belonging to a physical node."""
        if node not in self._nodes:
            return
        self._nodes.discard(node)
        for i in range(self.replicas):
            position = stable_hash(self._vnode_key(node, i))
            owner = self._position_to_node.get(position)
            if owner == node:
                del self._position_to_node[position]
                index = bisect.bisect_left(self._ring, position)
                if index < len(self._ring) and self._ring[index] == position:
                    self._ring.pop(index)

    def get_node(self, key: str) -> str | None:
        """Return the node responsible for `key`, or None if the ring is empty."""
        if not self._ring:
            return None
        point = stable_hash(key)
        # First ring position >= the key's position; wrap to index 0 if we ran
        # off the end (the ring is circular).
        index = bisect.bisect_right(self._ring, point)
        if index == len(self._ring):
            index = 0
        return self._position_to_node[self._ring[index]]

    @property
    def nodes(self) -> set[str]:
        return set(self._nodes)


def sample_keys(count: int, prefix: str = "key") -> list[str]:
    """Deterministic set of sample keys so all measurements are reproducible."""
    return [f"{prefix}-{i}" for i in range(count)]


def distribution(ring: ConsistentHashRing, keys: list[str]) -> dict[str, int]:
    """Count how many sample keys land on each node."""
    counts: Counter[str] = Counter()
    for key in keys:
        node = ring.get_node(key)
        if node is not None:
            counts[node] += 1
    # Include nodes that received zero keys so callers see the full picture.
    for node in ring.nodes:
        counts.setdefault(node, 0)
    return dict(counts)


def imbalance(counts: dict[str, int]) -> float:
    """Return max/mean load ratio. 1.0 is perfectly even; higher is worse."""
    if not counts:
        return 0.0
    loads = list(counts.values())
    mean = sum(loads) / len(loads)
    if mean == 0:
        return 0.0
    return max(loads) / mean


def remap_fraction(
    before: dict[str, str], after: dict[str, str]
) -> float:
    """Fraction of keys whose assigned node changed between two mappings."""
    if not before:
        return 0.0
    moved = sum(1 for key, node in before.items() if after.get(key) != node)
    return moved / len(before)


def assign_all(ring: ConsistentHashRing, keys: list[str]) -> dict[str, str]:
    """Snapshot the full key -> node mapping for the current ring."""
    return {key: ring.get_node(key) for key in keys}  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Naive modulo hashing, kept only to show how badly it remaps on resize.
# ---------------------------------------------------------------------------


def modulo_assign(keys: list[str], nodes: list[str]) -> dict[str, str]:
    """hash(key) % len(nodes) -> node. The thing consistent hashing replaces."""
    return {key: nodes[stable_hash(key) % len(nodes)] for key in keys}


def main() -> None:
    keys = sample_keys(10_000)

    # --- Consistent hashing: distribution across an initial cluster ---------
    ring = ConsistentHashRing(replicas=150)
    for node in ["node-a", "node-b", "node-c", "node-d"]:
        ring.add_node(node)

    counts = distribution(ring, keys)
    print(f"keys: {len(keys)}  nodes: {len(ring.nodes)}  replicas/node: {ring.replicas}")
    print("distribution (consistent hashing):")
    for node in sorted(counts):
        share = counts[node] / len(keys)
        print(f"  {node}: {counts[node]:>5}  ({share:6.2%})")
    print(f"imbalance (max/mean load): {imbalance(counts):.3f}")

    # --- Remap fraction when ADDING a node ----------------------------------
    before_add = assign_all(ring, keys)
    ring.add_node("node-e")
    after_add = assign_all(ring, keys)
    add_frac = remap_fraction(before_add, after_add)
    ideal = 1 / len(ring.nodes)
    print()
    print(f"add node-e:  remapped {add_frac:6.2%} of keys  (ideal ~= 1/N = {ideal:.2%})")

    # --- Remap fraction when REMOVING a node --------------------------------
    before_remove = after_add
    ring.remove_node("node-c")
    after_remove = assign_all(ring, keys)
    remove_frac = remap_fraction(before_remove, after_remove)
    print(f"remove node-c: remapped {remove_frac:6.2%} of keys")

    # --- Compare against naive modulo hashing -------------------------------
    nodes_4 = ["node-a", "node-b", "node-c", "node-d"]
    nodes_5 = ["node-a", "node-b", "node-c", "node-d", "node-e"]
    mod_before = modulo_assign(keys, nodes_4)
    mod_after = modulo_assign(keys, nodes_5)
    mod_frac = remap_fraction(mod_before, mod_after)
    print()
    print("modulo hashing for comparison (4 -> 5 nodes):")
    print(f"  remapped {mod_frac:6.2%} of keys  (almost everything moves)")

    # --- More replicas => smoother distribution -----------------------------
    print()
    print("replica count vs imbalance (lower is smoother):")
    for replicas in [1, 10, 50, 200]:
        r = ConsistentHashRing(replicas=replicas)
        for node in nodes_4:
            r.add_node(node)
        print(f"  replicas={replicas:>3}: imbalance={imbalance(distribution(r, keys)):.3f}")


if __name__ == "__main__":
    main()
