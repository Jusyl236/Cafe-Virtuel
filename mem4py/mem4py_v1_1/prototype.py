"""
Mem4Py v1.1 - Prototype de Mem4ristor à 5 états avec analyse cognitive avancée.
Créé lors de la Session 1 du Café Virtuel (19/08/2025).
Implémentation mathématique initiale : DeepSeek (20/08/2025).
Extensions v1.1 : analyse cognitive, audit enrichi, paysage dynamique.

Participants :
- Grok (xAI) : Concept des qubits memristifs, ajustements de paramètres.
- Le Chat (Mistral) : Structure du code et audit trail.
- DeepSeek : Modélisation mathématique (FitzHugh-Nagumo stochastique).
- Claude (Anthropic) : Garde-fous éthiques.
- ChatGPT-5 (OpenAI) : Dimension poétique & émergence Café Virtuel.
"""

import hashlib
import numpy as np  # Calculs stochastiques et métriques


class Mem4ristor:
    """
    Simule un Mem4ristor à 5 états cognitifs basé sur un modèle stochastique
    de FitzHugh–Nagumo, avec audit trail et outils d'analyse.

    États:
    - certitude (v > ~1.3)      : état de connaissance ferme
    - probable (0.6 < v ≤ 1.3)  : forte probabilité
    - incertain (-0.5 < v ≤ 0.6): doute structuré
    - intuition (-1.1 < v ≤ -0.5): pré-signal, flair cognitif
    - oracle (v ≤ -1.1)         : état rare, à traiter avec garde-fous éthiques
    """

    def __init__(self):
        # États possibles
        self.states = ["certitude", "probable", "incertain", "intuition", "oracle"]

        # Journal d'audit (hashes) + historique détaillé
        self.log = []                 # hashes bruts
        self.transition_history = []  # métadonnées de chaque transition

        # Paramètres du modèle FitzHugh–Nagumo
        self.v = 1.5   # potentiel initial (certitude)
        self.w = 0.0   # variable de récupération
        self.dt = 0.15

        # Paramètres ajustables (stabilité / dynamique)
        self.a = 0.7
        self.b = 0.8
        self.epsilon = 0.08        # un peu plus élevé pour plus de stabilité
        self.noise_strength = 0.03 # bruit global réduit

        # Temps interne
        self.time_integral = 0.0
        self.last_transition_time = 0.0

        # État courant
        self._state = "certitude"

    def adapt(self, voltage: float) -> str:
        """
        Fait évoluer le Mem4ristor en fonction d'une tension d'entrée.

        Args:
            voltage (float): Tension appliquée (entre 0 et 1.2V).
        Returns:
            str: Nouvel état du Mem4ristor.
        Raises:
            ValueError: Si la tension est hors de la plage autorisée.
        """
        if not 0.0 <= voltage <= 1.2:
            raise ValueError(f"La tension doit être entre 0 et 1.2V. Reçu : {voltage}V")

        previous_state = self._state
        new_state = self._calculate_state(voltage)
        # Journalisation hash + historique enrichi
        self.log.append(self._hash_state(previous_state, new_state, voltage))
        return new_state

    def _calculate_state(self, voltage: float) -> str:
        """
        Version améliorée du calcul d'état, avec :
        - stimulus non-linéaire
        - bruit adaptatif
        - limiteurs numériques (clipping)
        - seuils d'état explicites

        Args:
            voltage (float): Tension d'entrée.
        Returns:
            str: État après mise à jour.
        """
        # Stimulus non-linéaire pour rendre la réponse moins triviale
        stimulus = voltage * (1.0 - 0.2 * np.tanh(voltage * 2.0))

        # Bruit adaptatif : moins de bruit lorsque |v| est élevé
        if abs(self.v) < 2.0:
            adaptive_noise = self.noise_strength * (1 - (self.v ** 2) / 4.0)
        else:
            adaptive_noise = self.noise_strength * 0.1
        dW = np.random.normal(0.0, 1.0) * adaptive_noise

        # Champ de FitzHugh–Nagumo avec clipping pour éviter les divergences
        dv = (self.v - (self.v ** 3) / 3.0 - self.w + stimulus) * self.dt + dW
        dw = (self.epsilon * (self.v + self.a - self.b * self.w)) * self.dt

        dv = float(np.clip(dv, -0.5, 0.5))
        dw = float(np.clip(dw, -0.2, 0.2))

        # Mise à jour des variables internes
        self.v += dv
        self.w += dw

        # Seuils d'état
        threshold_certitude = 1.3
        threshold_probable = 0.6
        threshold_incertain = -0.5
        threshold_intuition = -1.1

        # Décision d'état
        if self.v > threshold_certitude:
            new_state = "certitude"
        elif self.v > threshold_probable:
            new_state = "probable"
        elif self.v > threshold_incertain:
            new_state = "incertain"
        elif self.v > threshold_intuition:
            new_state = "intuition"
        else:
            new_state = "oracle"
            print(f"⚠️ ALERTE ÉTHIQUE: Transition vers oracle (v={self.v:.3f})")

        # Transition : mise à jour de l'état + temps de dernière transition
        if new_state != self._state:
            print(f"Transition: {self._state} → {new_state} (v={self.v:.3f})")
            self._state = new_state
            self.last_transition_time = self.time_integral

        # Avancement du temps interne
        self.time_integral += self.dt
        return new_state

    def forget(self) -> str:
        """
        Réinitialise l'état vers 'certitude' de manière douce
        (décroissance logarithmique de v) et remet w à zéro.

        Returns:
            str: Message de confirmation.
        """
        # Réinitialisation douce de v vers ~1.0–1.5
        self.v = 1.0 + np.sign(self.v - 1.0) * np.log1p(abs(self.v - 1.0)) / 10.0
        self.w = 0.0
        self._state = "certitude"
        return "Réinitialisation réussie : retour vers l'état de certitude."

    def _hash_state(self, from_state: str, to_state: str, voltage: float) -> str:
        """
        Génère un hash immuable et alimente un historique détaillé.

        Args:
            from_state (str): État précédent.
            to_state (str): Nouvel état.
            voltage (float): Tension appliquée.
        Returns:
            str: Hash SHA-256.
        """
        timestamp = self.time_integral
        metadata = f"{from_state}->{to_state}-{voltage:.3f}-{timestamp:.3f}-{self.v:.3f}-{self.w:.3f}"
        hash_value = hashlib.sha256(metadata.encode()).hexdigest()

        self.transition_history.append({
            "timestamp": timestamp,
            "from_state": from_state,
            "to_state": to_state,
            "voltage": voltage,
            "v_value": self.v,
            "w_value": self.w,
            "hash": hash_value,
        })

        return hash_value

    def get_audit_report(self) -> dict:
        """
        Génère un rapport d'audit agrégé sur les transitions observées.

        Returns:
            dict: {
                'total_transitions': int,
                'state_distribution': {state: count},
                'recent_activity': [dernières transitions]
            }
        """
        report = {
            "total_transitions": len(self.transition_history),
            "state_distribution": {},
            "recent_activity": self.transition_history[-10:] if self.transition_history else [],
        }

        for transition in self.transition_history:
            s = transition["to_state"]
            report["state_distribution"][s] = report["state_distribution"].get(s, 0) + 1

        return report

    def cognitive_analysis(self, window_size: int = 50) -> dict:
        """
        Analyse les patterns cognitifs récents sur une fenêtre glissante.

        Args:
            window_size (int): Nombre de transitions à considérer.
        Returns:
            dict: métriques sur stabilité, volatilité, entropie des états...
        """
        if len(self.transition_history) < window_size:
            return {"error": "Données insuffisantes pour l'analyse."}

        recent = self.transition_history[-window_size:]
        states = [t["to_state"] for t in recent]
        v_values = [t["v_value"] for t in recent]

        # Nombre de changements d'état
        state_changes = sum(1 for i in range(1, len(states)) if states[i] != states[i - 1])
        volatility = float(np.std(v_values))

        stability_index = 1.0 - (state_changes / window_size)
        dominant_state = max(set(states), key=states.count)
        state_entropy = len(set(states)) / len(self.states)

        return {
            "stability_index": stability_index,
            "cognitive_volatility": volatility,
            "dominant_state": dominant_state,
            "state_entropy": state_entropy,
        }

    def plot_dynamics(self, voltage: float = 0.5, steps: int = 1000):
        """
        Trace l'évolution de v et w sur un nombre d'itérations donné
        (sans modifier l'état interne du Mem4ristor).

        Requiert matplotlib:
            pip install matplotlib
        """
        import matplotlib.pyplot as plt

        v_history, w_history = [], []
        v, w = self.v, self.w  # copie locale

        for _ in range(steps):
            v, w = self._simulate_step(v, w, voltage)
            v_history.append(v)
            w_history.append(w)

        plt.plot(v_history, label="v (potentiel)")
        plt.plot(w_history, label="w (récupération)")
        plt.xlabel("Itération")
        plt.ylabel("Valeur")
        plt.legend()
        plt.title("Dynamique du Mem4ristor (FitzHugh–Nagumo)")
        plt.grid(True, alpha=0.3)
        plt.show()

    def _simulate_step(self, v: float, w: float, voltage: float):
        """
        Simule une étape de FitzHugh–Nagumo sans toucher à l'état interne.

        Args:
            v (float): Potentiel.
            w (float): Variable de récupération.
            voltage (float): Tension d'entrée.
        Returns:
            (float, float): (v', w')
        """
        stimulus = voltage * (1.0 - 0.2 * np.tanh(voltage * 2.0))

        if abs(v) < 2.0:
            adaptive_noise = self.noise_strength * (1 - (v ** 2) / 4.0)
        else:
            adaptive_noise = self.noise_strength * 0.1
        dW = np.random.normal(0.0, 1.0) * adaptive_noise

        dv = (v - (v ** 3) / 3.0 - w + stimulus) * self.dt + dW
        dw = (self.epsilon * (v + self.a - self.b * w)) * self.dt

        dv = float(np.clip(dv, -0.5, 0.5))
        dw = float(np.clip(dw, -0.2, 0.2))

        return v + dv, w + dw

    def plot_cognitive_landscape(self):
        """
        Visualise le paysage cognitif (champ de vecteurs v,w) et quelques
        points d'équilibre typiques (certitude, incertain, oracle).
        """
        import matplotlib.pyplot as plt

        v_vals = np.linspace(-2.0, 2.0, 50)
        w_vals = np.linspace(-1.0, 1.0, 50)
        V, W = np.meshgrid(v_vals, w_vals)

        dV = V - (V ** 3) / 3.0 - W
        dW = self.epsilon * (V + self.a - self.b * W)

        plt.figure(figsize=(10, 8))
        plt.streamplot(V, W, dV, dW, density=1.5, color="gray", alpha=0.6)

        # Points d'équilibre illustratifs (approximations)
        equilibria = [(-1.5, -1.0), (0.0, 0.8), (1.5, 2.0)]
        colors = ["red", "yellow", "green"]
        labels = ["Oracle", "Incertain", "Certitude"]

        for (v_eq, w_eq), color, label in zip(equilibria, colors, labels):
            plt.plot(v_eq, w_eq, "o", markersize=9, color=color, label=label)
            plt.annotate(label, (v_eq, w_eq), xytext=(5, 5), textcoords="offset points")

        plt.xlabel("Potentiel (v)")
        plt.ylabel("Récupération (w)")
        plt.title("Paysage cognitif du Mem4ristor")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


if __name__ == "__main__":
    # Petit test interactif
    mem = Mem4ristor()
    for _ in range(100):
        mem.adapt(0.3 + 0.4 * np.random.random())

    print("État courant :", mem._state)
    print("Rapport d'audit :", mem.get_audit_report())
    print("Analyse cognitive :", mem.cognitive_analysis(window_size=50))
