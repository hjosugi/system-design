import unittest

from consistent_hash import (
    ConsistentHashRing,
    assign_all,
    distribution,
    imbalance,
    modulo_assign,
    remap_fraction,
    sample_keys,
)


class ConsistentHashRingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.keys = sample_keys(5_000)

    def _build(self, nodes, replicas=150) -> ConsistentHashRing:
        ring = ConsistentHashRing(replicas=replicas)
        for node in nodes:
            ring.add_node(node)
        return ring

    def test_same_key_maps_to_same_node(self) -> None:
        ring = self._build(["a", "b", "c"])
        for key in self.keys[:100]:
            self.assertEqual(ring.get_node(key), ring.get_node(key))

    def test_all_keys_assigned_to_known_nodes(self) -> None:
        nodes = {"a", "b", "c"}
        ring = self._build(nodes)
        for key in self.keys:
            self.assertIn(ring.get_node(key), nodes)

    def test_empty_ring_returns_none(self) -> None:
        ring = ConsistentHashRing(replicas=10)
        self.assertIsNone(ring.get_node("anything"))

    def test_adding_node_remaps_small_fraction(self) -> None:
        ring = self._build(["a", "b", "c", "d"])
        before = assign_all(ring, self.keys)
        ring.add_node("e")
        after = assign_all(ring, self.keys)
        frac = remap_fraction(before, after)
        # With 5 nodes the ideal is ~1/5 = 20%. Must be well below 50%.
        self.assertLess(frac, 0.5)
        self.assertGreater(frac, 0.0)

    def test_adding_node_only_moves_keys_onto_the_new_node(self) -> None:
        # Consistent hashing must not shuffle keys between pre-existing nodes;
        # every key that moves should move ONTO the newly added node.
        ring = self._build(["a", "b", "c", "d"])
        before = assign_all(ring, self.keys)
        ring.add_node("e")
        after = assign_all(ring, self.keys)
        for key, old_node in before.items():
            if after[key] != old_node:
                self.assertEqual(after[key], "e")

    def test_removing_node_only_reassigns_its_keys(self) -> None:
        ring = self._build(["a", "b", "c", "d"])
        before = assign_all(ring, self.keys)
        ring.remove_node("c")
        after = assign_all(ring, self.keys)
        for key, old_node in before.items():
            if old_node == "c":
                # Its keys must move somewhere else (c is gone).
                self.assertNotEqual(after[key], "c")
            else:
                # Keys not on c must stay exactly where they were.
                self.assertEqual(after[key], old_node)

    def test_remove_fraction_matches_removed_nodes_share(self) -> None:
        ring = self._build(["a", "b", "c", "d"])
        before = assign_all(ring, self.keys)
        c_share = sum(1 for n in before.values() if n == "c") / len(self.keys)
        ring.remove_node("c")
        after = assign_all(ring, self.keys)
        frac = remap_fraction(before, after)
        # Exactly c's keys move, nothing more.
        self.assertAlmostEqual(frac, c_share, places=6)

    def test_more_replicas_improve_balance(self) -> None:
        nodes = ["a", "b", "c", "d"]
        few = imbalance(distribution(self._build(nodes, replicas=1), self.keys))
        many = imbalance(distribution(self._build(nodes, replicas=200), self.keys))
        # More virtual nodes => closer to a perfectly even (imbalance 1.0) ring.
        self.assertLess(many, few)
        self.assertLess(many, 1.5)

    def test_beats_modulo_hashing_on_remap(self) -> None:
        ring = self._build(["a", "b", "c", "d"])
        before = assign_all(ring, self.keys)
        ring.add_node("e")
        after = assign_all(ring, self.keys)
        consistent_frac = remap_fraction(before, after)

        mod_before = modulo_assign(self.keys, ["a", "b", "c", "d"])
        mod_after = modulo_assign(self.keys, ["a", "b", "c", "d", "e"])
        mod_frac = remap_fraction(mod_before, mod_after)

        # Modulo hashing reshuffles almost everything; consistent hashing moves
        # far fewer keys.
        self.assertGreater(mod_frac, 0.5)
        self.assertLess(consistent_frac, mod_frac)

    def test_idempotent_add_and_remove(self) -> None:
        ring = self._build(["a", "b"])
        snapshot = assign_all(ring, self.keys)
        ring.add_node("a")  # already present: no-op
        ring.remove_node("zzz")  # absent: no-op
        self.assertEqual(assign_all(ring, self.keys), snapshot)
        self.assertEqual(ring.nodes, {"a", "b"})


if __name__ == "__main__":
    unittest.main()
