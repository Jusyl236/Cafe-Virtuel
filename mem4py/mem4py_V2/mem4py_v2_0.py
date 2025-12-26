import numpy as np
from typing import Dict, List

class Mem4ristorV2:
    """
    Implémentation finale de la v2.0 du Mem4ristor, avec :
    - Dynamique FHN étendue (v, w, u).
    - Couplage social atténué et filtré par (1 - u).
    - Hérétiques (couplage inversé).
    - Résistance cognitive (terme -α·tanh(v)).
    - Bruit gaussien sur v.
    """

    def __init__(self, seed: int = None, is_heretic: bool = False):
        self.rng = np.random.RandomState(seed)
        self.v = self.rng.uniform(-1.5, 1.5)  # Potentiel cognitif
        self.w = self.rng.uniform(0, 1)      # Variable de récupération
        self.u = 0.0                         # Variable de doute
        self.is_heretic = is_heretic

        # Paramètres de référence v2.0 (Claude)
        self.a = 0.7
        self.b = 0.8
        self.epsilon = 0.08
        self.D = 0.12
        self.epsilon_u = 0.02
        self.k_u = 0.8
        self.sigma_baseline = 0.05
        self.alpha = 0.1
        self.sigma_noise = 0.05
        self.dt = 0.1

    def update(self, I_stimulus: float, laplacian_v: float, N_size: int) -> None:
        """Mise à jour de l'état du Mem4ristor v2.0."""
        # Bruit réaliste
        eta_v = self.rng.normal(0, self.sigma_noise)

        # Couplage social atténué par le doute et adapté à la taille du réseau
        D_eff = self.D / np.sqrt(N_size)
        if self.is_heretic:
            I_ext = I_stimulus - D_eff * (1 - self.u) * laplacian_v
        else:
            I_ext = I_stimulus + D_eff * (1 - self.u) * laplacian_v

        # Dynamique FHN étendue avec résistance cognitive
        dv_dt = self.v - (self.v**3)/5 - self.w + I_ext - self.alpha * np.tanh(self.v) + eta_v
        dw_dt = self.epsilon * (self.v + self.a - self.b * self.w)

        # Stress social et baseline
        sigma_social = abs(laplacian_v)
        du_dt = self.epsilon_u * (self.k_u * sigma_social + self.sigma_baseline - self.u)

        # Mise à jour
        self.v += dv_dt * self.dt
        self.w += dw_dt * self.dt
        self.u += du_dt * self.dt
        self.u = max(0.0, min(self.u, 1.0))  # Clamping [0,1]

    @property
    def state(self) -> str:
        """Retourne l'état cognitif basé sur v."""
        if self.v < -1.5:
            return "oracle"
        elif -1.5 <= self.v < -0.8:
            return "intuition"
        elif -0.8 <= self.v <= 0.8:
            return "incertain"
        elif 0.8 < self.v <= 1.5:
            return "probable"
        else:
            return "certitude"

    def step(self, I_stimulus: float, laplacian_v: float, N_size: int) -> None:
        """Effectue une étape de simulation."""
        self.update(I_stimulus, laplacian_v, N_size)

class Mem4NetworkV2:
    """
    Réseau de Mem4ristors v2.0 avec gestion des hérétiques et calcul du Laplacien.
    """

    def __init__(self, size: int, heretic_ratio: float = 0.15, seed: int = 42):
        self.size = size
        self.rng = np.random.RandomState(seed)
        self.network = [[Mem4ristorV2(seed=i + j * size + seed, is_heretic=(self.rng.uniform(0, 1) < heretic_ratio))
                         for i in range(size)] for j in range(size)]

    def compute_laplacian(self, i: int, j: int) -> float:
        """Calcule le Laplacien pour le Mem4ristor (i, j)."""
        neighbors = []
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                neighbors.append(self.network[ni][nj].v)
        if neighbors:
            return np.mean(neighbors) - self.network[i][j].v
        return 0.0

    def step_all(self, I_stimulus: float = 0.0) -> None:
        """Effectue une étape de simulation pour tout le réseau."""
        for i in range(self.size):
            for j in range(self.size):
                laplacian_v = self.compute_laplacian(i, j)
                self.network[i][j].step(I_stimulus, laplacian_v, self.size)

    def get_states(self) -> List[str]:
        """Retourne les états de tous les Mem4ristors."""
        return [self.network[i][j].state for i in range(self.size) for j in range(self.size)]

    def get_u_mean(self) -> float:
        """Retourne la moyenne de u sur le réseau."""
        u_values = [self.network[i][j].u for i in range(self.size) for j in range(self.size)]
        return np.mean(u_values)

# Fonctions de test pour DeepSeek
def run_test_isolation(steps: int = 1000) -> Dict:
    mem = Mem4ristorV2(seed=42)
    for _ in range(steps):
        mem.step(I_stimulus=0.0, laplacian_v=0.0, N_size=1)
    return {
        'state': mem.state,
        'u': mem.u,
        'v': mem.v
    }

def run_test_network(size: int, steps: int = 1000) -> Dict:
    network = Mem4NetworkV2(size=size)
    states_history = []
    for _ in range(steps):
        network.step_all()
        states_history.append(network.get_states())

    final_states = network.get_states()
    unique, counts = np.unique(final_states, return_counts=True)
    state_distribution = dict(zip(unique, counts))

    # Calcul de l'entropie
    probabilities = counts / size**2
    entropy = -np.sum(probabilities * np.log(probabilities + 1e-10))

    return {
        'state_distribution': state_distribution,
        'diversity': len(unique) / 5,
        'oracle_fraction': state_distribution.get('oracle', 0) / (size**2),
        'u_mean': network.get_u_mean(),
        'entropy': entropy
    }

# Exemple d'utilisation
if __name__ == "__main__":
    # Test d'isolation
    isolation_result = run_test_isolation(steps=1000)
    print("Résultat test isolation :", isolation_result)

    # Tests réseau
    for size in [4, 10, 25]:
        result = run_test_network(size=size, steps=1000)
        print(f"Résultat test {size}x{size} :", result)
