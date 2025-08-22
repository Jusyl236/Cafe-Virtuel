import unittest
import numpy as np
from prototype import Mem4ristor

class TestMem4ristor(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)  # Fixe la graine pour des résultats reproductibles
        self.mem = Mem4ristor()

    def test_adapt_valid_voltage(self):
        # Test avec des tensions valides
        self.assertEqual(self.mem.adapt(0.1), "certitude")
        for _ in range(100):  # 100 itérations pour atteindre "probable"
            self.mem.adapt(0.5)
        self.assertEqual(self.mem._state, "probable")
        self.assertEqual(self.mem.forget(), "Réinitialisation réussie : intuition → certitude.")

    def test_adapt_invalid_voltage(self):
        # Test avec des tensions invalides (doit lever ValueError)
        with self.assertRaises(ValueError):
            self.mem.adapt(-0.1)
        with self.assertRaises(ValueError):
            self.mem.adapt(1.3)

    def test_forget(self):
        # Test de la réinitialisation
        self.mem._state = "intuition"  # Force l'état à "intuition"
        self.assertEqual(self.mem.forget(), "Réinitialisation réussie : intuition → certitude.")
        self.assertEqual(self.mem._state, "certitude")

    def test_hash_state(self):
        # Test que _hash_state génère bien un hash
        hash1 = self.mem._hash_state("certitude", 0.1)
        self.assertEqual(len(hash1), 64)  # SHA-256 produit un hash de 64 caractères
        self.mem.adapt(0.1)  # Change time_integral
        hash2 = self.mem._hash_state("certitude", 0.1)
        self.assertNotEqual(hash1, hash2)  # Différent car time_integral a changé

    def test_oracle_state(self):
        # Test pour atteindre l'état oracle
        self.mem.v = -2.0  # Force v pour atteindre oracle
        self.assertEqual(self.mem.adapt(0.0), "oracle")

if __name__ == "__main__":
    unittest.main()