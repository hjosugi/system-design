# Consistent Hashing Lab

A runnable implementation drill for a consistent hash ring with virtual nodes.

Last verified: 2026-06-21

## Goal

Make the central promise of consistent hashing concrete: when a server joins or
leaves the cluster, only about `1/N` of the keys move (N = node count), instead
of the near-total reshuffle you get from naive `hash(key) % len(nodes)`.

## Concept

A consistent hash ring maps both keys and server identities onto the same
circular hash space (here, a 32-bit ring driven by `hashlib.md5`). A key is owned
by the first server position found walking clockwise from the key's position,
wrapping around at the top.

Each physical node is placed at many points on the ring (virtual nodes /
replicas). This is what keeps load even: one point per node gives wildly uneven
arc sizes, while 100-200 points per node averages out so each server owns a
similar total slice. Adding a node only steals arcs from its clockwise
neighbors; removing a node hands its arcs to the next nodes clockwise. Nobody
else is disturbed.

## API

- `ConsistentHashRing(replicas=100)` - ring with `replicas` virtual nodes per physical node.
- `ring.add_node(name)` / `ring.remove_node(name)` - mutate the cluster.
- `ring.get_node(key) -> str | None` - look up the owning node (O(log V) via `bisect`).
- `distribution(ring, keys)` - keys-per-node histogram.
- `imbalance(counts)` - max/mean load ratio (1.0 is perfectly even).
- `remap_fraction(before, after)` - fraction of keys that changed owner.
- `modulo_assign(keys, nodes)` - the naive baseline, for comparison.

## Data Structures

- `_ring`: sorted list of virtual-node hash positions; `bisect` finds the
  successor position in O(log V).
- `_position_to_node`: ring position -> physical node name.
- `_nodes`: set of physical node names.

## Run

```bash
python3 implementations/consistent-hashing-lab/consistent_hash.py
```

This prints the key distribution across the cluster, the remap fraction when a
node is added and when a node is removed, the modulo-hashing remap fraction for
comparison, and how imbalance shrinks as the replica count grows.

## Test

Non-interactive, exits non-zero on failure:

```bash
cd implementations/consistent-hashing-lab && python3 -m unittest -v
```

The suite asserts: same key always maps to the same node; adding a node remaps
well below 50% of keys and only ever moves keys *onto* the new node; removing a
node reassigns only that node's keys; more replicas produce a smoother
distribution; and consistent hashing remaps far fewer keys than modulo hashing.

## Where Consistent Hashing Is Used

- **Sharded caches**: memcached client rings (Ketama) so a dead cache box only
  invalidates its own slice instead of cold-starting the whole tier.
- **Distributed key-value / wide-column stores**: Amazon Dynamo, Apache
  Cassandra, Riak, and Voldemort place data on a ring of token ranges.
- **Request / session routing**: load balancers and API gateways that want
  sticky routing without a central lookup table.
- **CDNs and object stores**: choosing which edge or storage node holds a blob.

## Tradeoffs

- **Pro**: minimal data movement on scale-up/down (~1/N keys), no central
  directory, deterministic placement from the key alone.
- **Con (balance)**: a plain ring is lumpy; you need many virtual nodes per
  physical node to even out load, which costs memory and ring-rebuild time.
- **Con (heterogeneity)**: equal replicas assume equal-capacity nodes. Bigger
  boxes need proportionally more virtual nodes (weighting).
- **Con (hot keys)**: consistent hashing balances *keys*, not *traffic*. One
  viral key still hammers a single node; you need replication or request-level
  sharding on top.
- **Alternative**: rendezvous (highest-random-weight) hashing gives similar
  minimal-movement properties without storing a ring, at O(N) lookup per key.
  Jump consistent hash is even smaller but cannot remove arbitrary nodes.

## Limitations

This toy uses a single 32-bit hash and no replication factor (each key has
exactly one owner). It does not implement weighted nodes, data migration,
bounded-load variants, or persistence. It measures placement, not real network
behavior.

## Upgrade path

This lab is the in-memory foundation. To swap in a real heavy tool later:

- **Cache tier (memcached + Ketama)**: replace `get_node` with a real client
  that already speaks the Ketama ring, e.g. `pymemcache`'s
  `HashClient` over several memcached servers. Keep this lab's distribution and
  remap measurements as a harness to validate the client's rebalancing before
  you trust it in production.
- **Distributed store (Cassandra / ScyllaDB)**: stop computing placement
  yourself. Stand up a cluster, model the same keys as a table partitioned by a
  partition key, and observe token ownership with `nodetool ring` /
  `nodetool status`. The ring math in this lab maps directly onto Cassandra's
  token ranges and `num_tokens` (its virtual-node setting).
- **Redis Cluster**: it uses 16384 fixed hash slots rather than a hash ring;
  port the `add_node`/`remove_node` experiments to `CLUSTER ADDSLOTS` /
  resharding and compare how slot migration differs from arc handoff.

Each upgrade is additive: the public API (`get_node`, `add_node`, `remove_node`)
and the measurement helpers stay the same, so the tests keep documenting the
behavior you expect from the heavier system.

## Exercises

1. **Weighted nodes.** Add a `weight` parameter so a node placed with
   `replicas * weight` virtual nodes gets proportionally more keys. Verify the
   distribution shifts and the remap-on-add property still holds.
2. **Replication factor N.** Add `get_nodes(key, n)` that returns the next `n`
   distinct physical nodes clockwise (skip duplicate virtual nodes). This is how
   Dynamo/Cassandra pick replicas. Add a test that all `n` are distinct.
3. **Plot replica count vs imbalance.** Sweep `replicas` from 1 to 500 and
   compute imbalance; confirm the diminishing-returns curve and pick a value
   where imbalance < 1.1. Explain the memory cost of going higher.
4. **Rendezvous (HRW) hashing.** Implement an alternative `get_node` that scores
   each node as `hash(node + key)` and picks the max. Compare its remap fraction
   and lookup cost against the ring version on the same key set.
5. **Hot-key stress test.** Make 90% of requests target 1% of keys and measure
   per-node *request* load (not key count). Show that consistent hashing alone
   does not fix hot spots, then sketch what would.

## Related Case Study

Core component: sharding and rebalance cost. Pairs with the rate limiter lab as
the second "core building block" implementation drill in this repo.
