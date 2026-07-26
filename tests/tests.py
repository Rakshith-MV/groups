import itertools
import math
import unittest

from groups import MnA, MnM, Dn, Sn, Pn


class GroupAxiomTests(unittest.TestCase):
    """
    Generic axiom checks (closure, identity, inverses, associativity) applied
    to every concrete group family. These are sanity checks, not proofs -
    associativity in particular is checked by sampling rather than
    exhaustively for larger groups.
    """

    def _check_group_axioms(self, group, expected_order=None):
        elements = group.elements()

        if expected_order is not None:
            self.assertEqual(len(elements), expected_order)

        # The identity is the unique element satisfying e*e == e; this avoids
        # relying on group._identity, whose type is inconsistent across
        # group families (a raw int for MnA, an `element` object elsewhere).
        idempotents = [e for e in elements if e * e == e]
        self.assertEqual(len(idempotents), 1, "expected exactly one identity element")
        identity = idempotents[0]

        # Identity acts as identity on both sides
        for e in elements:
            self.assertEqual(identity * e, e)
            self.assertEqual(e * identity, e)

        # Every element has an inverse that multiplies to the identity
        for e in elements:
            inv = group._inverses[e]
            self.assertEqual(e * inv, identity)
            self.assertEqual(inv * e, identity)

        # Closure: product of any two elements is itself in the group
        element_set = set(elements)
        for a, b in itertools.product(elements, repeat=2):
            self.assertIn(a * b, element_set)

        # Associativity, sampled over triples (exhaustive for small groups)
        sample = elements if len(elements) <= 6 else elements[:6]
        for a, b, c in itertools.product(sample, repeat=3):
            self.assertEqual((a * b) * c, a * (b * c))

    def test_modulo_additive(self):
        for n in (4, 6, 9):
            with self.subTest(n=n):
                self._check_group_axioms(MnA(n, generators=['1']), expected_order=n)

    def test_modulo_multiplicative(self):
        # Order of (Z/nZ)* is Euler's totient of n
        totients = {5: 4, 8: 4, 9: 6}
        for n, phi_n in totients.items():
            with self.subTest(n=n):
                self._check_group_axioms(MnM(n, generators=['1']), expected_order=phi_n)

    def test_dihedral(self):
        # Dn(n) takes n as the group's own order (must be even: D_{n/2} has order n)
        for n in (6, 8, 10):
            with self.subTest(n=n):
                self._check_group_axioms(Dn(n, generators=['r^1', 'f']), expected_order=n)

    def test_symmetric(self):
        for n in (2, 3, 4):
            with self.subTest(n=n):
                self._check_group_axioms(Sn(n, 0, ['(01)']), expected_order=math.factorial(n))

    def test_alternating(self):
        for n in (3, 4):
            with self.subTest(n=n):
                self._check_group_axioms(Sn(n, 1, ['(012)']), expected_order=math.factorial(n) // 2)

    def test_product_group(self):
        g1 = MnA(2)
        g2 = MnA(3)
        product_g = Pn([g1, g2])
        self._check_group_axioms(product_g, expected_order=6)



class NormalitySubgroupTests(unittest.TestCase):
    """
    S3 is a convenient small example with a mix of normal and non-normal
    subgroups, and is small enough that the full lattice is always computed
    (never hits the size cutoff), so it's a good sanity check for
    is_normal() and cosets().
    """

    def setUp(self):
        self.s3 = Sn(3, 0, ['(01)'])
        self.subs = self.s3.subgroups()

    def test_trivial_and_whole_group_are_normal(self):
        trivial = min(self.subs, key=len)
        whole = max(self.subs, key=len)
        self.assertTrue(self.s3.is_normal(trivial))
        self.assertTrue(self.s3.is_normal(whole))

    def test_order_2_subgroups_not_normal(self):
        order_2 = [H for H in self.subs if len(H) == 2]
        self.assertEqual(len(order_2), 3)
        for H in order_2:
            self.assertFalse(self.s3.is_normal(H))

    def test_order_3_subgroup_is_normal(self):
        order_3 = [H for H in self.subs if len(H) == 3]
        self.assertEqual(len(order_3), 1)
        self.assertTrue(self.s3.is_normal(order_3[0]))

    def test_cosets_partition_the_group(self):
        for H in self.subs:
            cosets = self.s3.cosets(H)
            # every element appears in exactly one coset
            covered = set()
            for c in cosets:
                self.assertTrue(covered.isdisjoint(c))
                covered |= c
            self.assertEqual(covered, set(self.s3.elements()))
            # index * |H| == |G|
            self.assertEqual(len(cosets) * len(H), len(self.s3.elements()))

    def test_left_right_cosets_agree_iff_normal(self):
        for H in self.subs:
            left = set(self.s3.cosets(H, side='left'))
            right = set(self.s3.cosets(H, side='right'))
            self.assertEqual(left == right, self.s3.is_normal(H))


class HomomorphismTests(unittest.TestCase):
    def test_a3_to_s3_homomorphisms(self):
        import sys, os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'web'))
        from web.app import get_group_instance, find_homomorphisms

        dom = get_group_instance('S', 3, 'A_n')
        codom = get_group_instance('S', 3, 'S_n')

        subs = dom.subgroups()
        normal_subs = sorted([H for H in subs if dom.is_normal(H)], key=len)

        # Trivial kernel -> 2 injective embeddings of A3 into S3
        k0_str = {str(k) for k in normal_subs[0]}
        homs0 = find_homomorphisms(dom, codom, k0_str)
        self.assertEqual(len(homs0), 2)
        self.assertTrue(all(h['is_injective'] for h in homs0))

        # Full group kernel -> 1 trivial homomorphism
        k1_str = {str(k) for k in normal_subs[1]}
        homs1 = find_homomorphisms(dom, codom, k1_str)
        self.assertEqual(len(homs1), 1)
        self.assertFalse(homs1[0]['is_injective'])


if __name__ == "__main__":
    unittest.main()
