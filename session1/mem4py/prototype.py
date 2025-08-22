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
import time
import numpy as np  # Ajouté pour les calculs stochastiques

class Mem4ristor:
    """Classe pour simuler un Mem4ristor à 5 états avec audit trail."""

    def __init__(self):
        self.states = ["certitude", "probable", "incertain", "intuition", "oracle"]
        self.log = []  # Liste de hash pour l'audit trail (blockchain-like)

        # Variables pour le modèle FitzHugh-Nagumo (ajoutées par DeepSeek)
        self.v = 1.5  # Valeur initiale pour l'état "certitude"
        self.w = 0.0  # Variable de récupération initiale
        self.dt = 0.1  # Pas de temps pour l'intégration
        self.time_integral = 0.0
        self.last_transition_time = 0.0
        self._state = "certitude"  # État initial

    def adapt(self, voltage):
        """
        Passe à un nouvel état en fonction de la tension d'entrée.
        Args:
            voltage (float): Tension appliquée (entre 0 et 1.2V).
        Returns:
            str: Nouveau état du Mem4ristor.
        """
        new_state = self._calculate_state(voltage)
        self.log.append(self._hash_state(new_state, voltage))
        return new_state

    def _calculate_state(self, voltage):
        """
        Calcule la transition d'état en fonction de la tension appliquée.
        Utilise une version stochastique du modèle de FitzHugh-Nagumo pour simuler
        la dynamique non-linéaire des 4 états cognitifs.
        Args:
            voltage (float): La tension d'entrée, stimulus principal.
        """
        # Paramètres du modèle (ajustables)
        a = 0.7
        b = 0.8
        epsilon = 0.08
        noise_strength = 0.05  # Force du bruit stochastique (σ)

        # Transforme le voltage en stimulus
        stimulus = voltage * 0.5

        # Terme stochastique (bruit Wiener) pour V4 (incertitude/intuition)
        dW = np.random.normal(0.0, 1.0) * noise_strength

        # Équations différentielles de FitzHugh-Nagumo (méthode d'Euler)
        dv = (self.v - (self.v**3)/3 - self.w + stimulus) * self.dt + dW
        dw = (epsilon * (self.v + a - b * self.w)) * self.dt

        # Mise à jour des variables internes
        self.v += dv
        self.w += dw

        # Seuils dynamiques pour les transitions d'état
        if self.v > 1.25:
            new_state = "certitude"
        elif self.v > 0.55:
            new_state = "probable"
        elif self.v > -0.55:
            new_state = "incertain"
        else:
            new_state = "intuition"

        # Met à jour l'état si changement significatif
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
        """
        # Réinitialisation douce vers l'état de certitude (v ~= 1.5)
        self.v = 1.0 + np.sign(self.v - 1.0) * np.log1p(abs(self.v - 1.0)) / 10
        self.w = 0.0  # Réinitialisation de la variable de récupération
        self._state = "certitude"  # Force l'état à "certitude"
        return "Réinitialisation réussie : intuition → certitude."

    def _hash_state(self, state, voltage):
        """
        Génère un hash immuable pour l'audit trail.
        Args:
            state (str): État actuel.
            voltage (float): Tension appliquée.
        Returns:
            str: Hash SHA-256 de l'état + tension + timestamp.
        """
        return hashlib.sha256(f"{state}-{voltage}-{time.time()}".encode()).hexdigest()

# Exemple d'utilisation
if __name__ == "__main__":
    mem = Mem4ristor()
    print("État initial :", mem.adapt(0.1))  # Doit retourner "certitude"
    print("Test de forget() :", mem.forget())  # Doit retourner "Réinitialisation réussie..."
    print("Nouvel état après forget :", mem._state)  # Doit être "certitude"
