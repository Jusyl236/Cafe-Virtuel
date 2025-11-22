import unittest
import numpy as np
from prototype import Mem4ristor


class TestMem4ristor(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)  # Rend les tests reproductibles
        self.mem = Mem4ristor()

    def test_adapt_valid_voltage(self):
        # Appel simple : doit retourner un état valide et journaliser
        state = self.mem.adapt(0.5)
        self.assertIn(state, self.mem.states)
        self.assertEqual(len(self.mem.log), 1)
        self.assertEqual(len(self.mem.transition_history), 1)

        # Plusieurs appels ne doivent pas faire planter et rester dans les états connus
        for _ in range(50):
            s = self.mem.adapt(0.3 + 0.4 * np.random.random())
            self.assertIn(s, self.mem.states)

        # Test de forget()
        self.mem._state = "intuition"
        msg = self.mem.forget()
        self.assertIn("certitude", msg.lower())
        self.assertEqual(self.mem._state, "certitude")

    def test_adapt_invalid_voltage(self):
        with self.assertRaises(ValueError):
            self.mem.adapt(-0.1)
        with self.assertRaises(ValueError):
            self.mem.adapt(1.3)

    def test_hash_state(self):
        # Test du format de hash et de l'ajout à transition_history
        h = self.mem._hash_state("certitude", "probable", 0.1)
        self.assertEqual(len(h), 64)
        self.assertEqual(len(self.mem.transition_history), 1)
        t = self.mem.transition_history[0]
        self.assertEqual(t["from_state"], "certitude")
        self.assertEqual(t["to_state"], "probable")
        self.assertAlmostEqual(t["voltage"], 0.1, places=3)

    def test_oracle_state(self):
        # Force v pour se rapprocher d'un état oracle
        self.mem.v = -2.0
        state = self.mem.adapt(0.0)
        self.assertEqual(state, "oracle")

    def test_audit_report(self):
        # Génère quelques transitions
        for _ in range(20):
            self.mem.adapt(0.3 + 0.4 * np.random.random())

        report = self.mem.get_audit_report()
        self.assertGreaterEqual(report["total_transitions"], 20)
        self.assertIn("state_distribution", report)
        self.assertIsInstance(report["recent_activity"], list)

    def test_cognitive_analysis(self):
        # Pas assez de données → erreur
        analysis_small = self.mem.cognitive_analysis(window_size=10)
        self.assertIn("error", analysis_small)

        # Génère suffisamment de transitions
        for _ in range(100):
            self.mem.adapt(0.3 + 0.4 * np.random.random())

        analysis = self.mem.cognitive_analysis(window_size=50)
        self.assertIn("stability_index", analysis)
        self.assertIn("cognitive_volatility", analysis)
        self.assertIn("dominant_state", analysis)
        self.assertIn("state_entropy", analysis)
        self.assertTrue(0.0 <= analysis["stability_index"] <= 1.0)


if __name__ == "__main__":
    unittest.main()
