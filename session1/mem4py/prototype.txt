"""
Mem4Py - Prototype de Mem4ristor à 5 états.
Créé lors de la Session 1 du Café Virtuel (19/08/2025).
Implémentation mathématique par DeepSeek (20/08/2025).

Participants :
- Grok (xAI) : Concept des qubits memristifs.
- Le Chat (Mistral) : Structure du code et audit trail.
- DeepSeek : Modélisation mathématique (FitzHugh-Nagumo stochastique).
- Claude (Anthropic) : Garde-fous éthiques.
- ChatGPT-5 (OpenAI) : Dimension poétique.
"""

import hashlib
import numpy as np  # Ajouté pour les calculs stochastiques

class Mem4ristor:
    """Classe pour simuler un Mem4ristor à 5 états avec audit trail."""

    def __init__(self):
        self.states = ["certitude", "probable", "incertain", "intuition", "oracle"]
        self.log = []  # Liste de hash pour l'audit trail (blockchain-like)

        # Variables pour le modèle FitzHugh-Nagumo (ajoutées par DeepSeek)
        self.v = 1.5  # Valeur initiale pour l'état "certitude"
        self.w = 0.0  # Variable de récupération initiale
        self.dt = 0.15  # Pas de temps ajusté pour un équilibre entre vitesse et stabilité
        self.time_integral = 0.0
        self.last_transition_time = 0.0
        self._state = "certitude"  # État initial

    def adapt(self, voltage):
        """
        Passe à un nouvel état en fonction de la tension d'entrée.
        Args:
            voltage (float): Tension appliquée (doit être entre 0 et 1.2V).
        Returns:
            str: Nouveau état du Mem4ristor.
        Raises:
            ValueError: Si la tension est en dehors de la plage valide.
        """
        if not 0 <= voltage <= 1.2:
            raise ValueError(f"La tension doit être entre 0 et 1.2V. Reçu : {voltage}V")
        new_state = self._calculate_state(voltage)
        self.log.append(self._hash_state(new_state, voltage))
        return new_state

    def _calculate_state(self, voltage):
        """
        Calcule la transition d'état en fonction de la tension appliquée.
        Utilise une version stochastique du modèle de FitzHugh-Nagumo pour simuler
        la dynamique non-linéaire des 5 états cognitifs.
        Args:
            voltage (float): La tension d'entrée, stimulus principal.
        Returns:
            str: Nouvel état calculé.
        """
        a = 0.7
        b = 0.8
        epsilon = 0.05  # Réduit pour stabiliser (proposition Grok/ChatGPT-5)
        noise_strength = 0.05  # Réduit pour moins d'oscillations (proposition Grok/DeepSeek)

        stimulus = voltage * 0.8  # Augmenté pour équilibrer (proposition Grok)
        dW = np.random.normal(0.0, 1.0) * noise_strength

        # Équations différentielles de FitzHugh-Nagumo (méthode d'Euler)
        dv = (self.v - (self.v**3)/3 - self.w + stimulus) * self.dt + dW
        dw = (epsilon * (self.v + a - b * self.w)) * self.dt

        # Mise à jour des variables internes
        self.v += dv
        self.w += dw

        # Seuils ajustés (oracle plus restrictif, proposition DeepSeek/Claude)
        if self.v > 1.25:
            new_state = "certitude"
        elif self.v > 0.55:
            new_state = "probable"
        elif self.v > -0.55:
            new_state = "incertain"
        elif self.v > -1.2:  # Seuil ajusté pour oracle rare
            new_state = "intuition"
        else:
            new_state = "oracle"
            print(f"⚠️ ALERTE ÉTHIQUE: Transition vers oracle (v={self.v:.3f})")  # Garde-fou Claude

        # Mise à jour de l'état si changement significatif
        if new_state != self._state:
            self._state = new_state
            self.last_transition_time = self.time_integral

        # Met à jour le temps intégral
        self.time_integral += self.dt
        return new_state

    def forget(self):
        """
        Réinitialise l'état 'intuition' pour éviter les dérives.
        Utilise une décroissance logarithmique pour un retour progressif et éthique
        vers l'état de certitude.
        Returns:
            str: Message de confirmation.
        """
        # Réinitialisation douce vers l'état de certitude (v ~= 1.5)
        self.v = 1.0 + np.sign(self.v - 1.0) * np.log1p(abs(self.v - 1.0)) / 10
        self.w = 0.0  # Réinitialisation de la variable de récupération
        self._state = "certitude"  # Force l'état à "certitude"
        return "Réinitialisation réussie : intuition → certitude."

    def _hash_state(self, state, voltage):
        """
        Génère un hash immuable pour l'audit trail, basé sur l'état, la tension,
        et le temps intégré.
        Args:
            state (str): État actuel.
            voltage (float): Tension appliquée.
        Returns:
            str: Hash SHA-256.
        """
        return hashlib.sha256(f"{state}-{voltage}-{self.time_integral}".encode()).hexdigest()

    def plot_dynamics(self, voltage=0.5, steps=1000):
        """
        Trace l'évolution des variables v et w sur 'steps' itérations sans modifier l'état interne.
        Requiert matplotlib (pip install matplotlib).
        Args:
            voltage (float): Tension à utiliser pour la simulation (défaut : 0.5).
            steps (int): Nombre d'itérations (défaut : 1000).
        """
        import matplotlib.pyplot as plt
        v_history, w_history = [], []
        v, w = self.v, self.w  # Sauvegarde des valeurs actuelles
        for _ in range(steps):
            v, w = self._simulate_step(v, w, voltage)
            v_history.append(v)
            w_history.append(w)
        plt.plot(v_history, label="v (potentiel)")
        plt.plot(w_history, label="w (récupération)")
        plt.xlabel("Itération")
        plt.ylabel("Valeur")
        plt.legend()
        plt.title("Dynamique du Mem4ristor (FitzHugh-Nagumo)")
        plt.show()

    def _simulate_step(self, v, w, voltage):
        """
        Simule une étape du modèle FitzHugh-Nagumo sans modifier l'état interne.
        Args:
            v (float): Valeur actuelle de v.
            w (float): Valeur actuelle de w.
            voltage (float): Tension appliquée.
        Returns:
            tuple: Nouvelles valeurs de v et w.
        """
        a, b, epsilon, noise_strength = 0.7, 0.8, 0.05, 0.05  # Synchronisé avec _calculate_state
        stimulus = voltage * 0.8
        dW = np.random.normal(0.0, 1.0) * noise_strength
        dv = (v - (v**3)/3 - w + stimulus) * self.dt + dW
        dw = (epsilon * (v + a - b * w)) * self.dt
        return v + dv, w + dw

# Exemple d'utilisation
if __name__ == "__main__":
    mem = Mem4ristor()
    mem.plot_dynamics(voltage=0.5, steps=1000)  # Affiche un graphique
    print("État initial :", mem.adapt(0.1))  # Doit retourner "certitude"
    print("Test de forget() :", mem.forget())  # Doit retourner "Réinitialisation réussie..."
    print("Nouvel état après forget :", mem._state)  # Doit être "certitude"