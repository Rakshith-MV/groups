import itertools
import math
import unittest

from groups import MnA, MnM, Dn, Sn


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


if __name__ == "__main__":
    unittest.main()
