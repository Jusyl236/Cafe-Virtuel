"""
Mem4Py v1.2 — Proto-laboratoire de gouvernance cognitive

Ce module implémente un petit réseau de "mem4ristors" :
- dynamique FitzHugh–Nagumo étendue (v, w, u)
- doute constitutif (u) qui freine la synchronisation excessive
- hérétiques garantissant une diversité minimale
- mortalité douce + renaissance légère (mutation paramètre)
- quelques métriques de santé cognitive simples

Dépendances :
    numpy
    matplotlib (optionnelle, pour la démo rapide)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import numpy as np

STATE_NAMES = ["certitude", "probable", "incertain", "intuition", "oracle"]


# ---------------------------------------------------------------------------
# Unité de base : Mem4ristor
# ---------------------------------------------------------------------------

@dataclass
class Mem4ristor:
    """Unité cognitive élémentaire."""

    is_heretic: bool = False
    seed: int | None = None
    dt: float = 0.1
    noise_strength: float = 0.1

    v: float = field(init=False)
    w: float = field(init=False)
    u: float = field(init=False)

    a: float = field(init=False)
    b: float = field(init=False)
    epsilon: float = field(init=False)

    epsilon_u: float = field(init=False)
    k_u: float = field(init=False)
    alpha: float = field(init=False)

    age: int = field(init=False, default=0)
    lifespan: int = field(init=False)

    history: List[Tuple[float, float, float, str]] = field(
        init=False, default_factory=list
    )

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.seed)

        # États initiaux
        self.v = float(self.rng.normal(0.0, 0.5))
        self.w = 0.0
        self.u = 0.0

        # Paramètres légèrement mutés
        self.a = float(0.7 + self.rng.normal(0, 0.03))
        self.b = float(0.8 + self.rng.normal(0, 0.03))
        self.epsilon = float(0.08 + self.rng.normal(0, 0.005))

        # Doute constitutif
        self.epsilon_u = 0.012
        self.k_u = 0.45
        self.alpha = 2.2 if self.is_heretic else 1.0

        # Vie et mort
        self.lifespan = int(self.rng.exponential(10000)) + 5000

        self.state = self._compute_state()

    # ------------------------- dynamique interne ---------------------------

    def _compute_state(self) -> str:
        """Mappe la valeur v sur un état cognitif discret."""
        v = self.v
        if v > 1.3:
            return "certitude"
        elif v > 0.6:
            return "probable"
        elif v > -0.5:
            return "incertain"
        elif v > -1.1:
            return "intuition"
        else:
            return "oracle"

    def update_doubt(self, laplacian_v: float) -> None:
        """
        Met à jour u (doute constitutif).

        - Si le laplacien est proche de 0 → v localement synchronisé → u monte.
        - Si les voisinages sont très différents → u redescend.
        """
        sync_measure = -abs(laplacian_v)  # proche de 0 => très synchrone
        du = self.epsilon_u * (self.k_u * sync_measure - self.u)
        self.u = float(np.clip(self.u + du, 0.0, 2.5))

    def step(self, external_stimulus: float, laplacian_v: float) -> str:
        """
        Fait un pas de simulation.

        external_stimulus : stimulus externe (input)
        laplacian_v       : “pression” des voisins (couplage diffusif)
        """
        self.age += 1

        # 1. mise à jour du doute
        self.update_doubt(laplacian_v)

        # 2. dynamique FitzHugh–Nagumo modifiée
        # bruit adaptatif (plus u est grand, plus le bruit diminue)
        noise_factor = max(0.1, 1.0 - self.u / 3.0)
        noise = self.noise_strength * noise_factor * self.rng.standard_normal()

        # inhibition proportionnelle au doute et à la certitude
        inhibition = -1.8 * self.u * self.v

        # CORRECTION STABILITÉ : Facteurs 0.8 et 0.5 pour amortir les forces
        dv = (
            0.8 * (self.v - (self.v ** 3) / 3.0)
            - 0.5 * self.w
            + external_stimulus
            + inhibition
            + self.alpha * laplacian_v
        ) * self.dt + noise

        dw = self.epsilon * (self.v + self.a - self.b * self.w) * self.dt

        # clipping doux pour éviter les explosions numériques
        dv = float(np.clip(dv, -0.6, 0.6))
        dw = float(np.clip(dw, -0.25, 0.25))

        self.v += dv
        self.w += dw

        # 3. mort douce & renaissance
        if self.age >= self.lifespan:
            self.die_and_renew()

        # 4. nouvel état
        self.state = self._compute_state()
        self.log_transition()

        return self.state

    def die_and_renew(self) -> None:
        """Mort douce + renaissance avec mutation légère."""
        # On garde is_heretic, dt, noise_strength ; on régénère le reste
        self.__post_init__()
        self.age = 0  # après __post_init__ pour éviter l’écrasement

    def log_transition(self) -> None:
        """Enregistre (v, w, u, état) pour l’audit."""
        self.history.append((self.v, self.w, self.u, self.state))


# ---------------------------------------------------------------------------
# Réseau de Mem4ristors
# ---------------------------------------------------------------------------

class Mem4Network:
    """Réseau 2D de mem4ristors."""

    def __init__(self, size: int = 4, heretic_ratio: float = 0.15, dt: float = 0.1):
        self.size = size
        self.dt = dt
        self.heretic_ratio = heretic_ratio
        self.grid: np.ndarray = np.empty((size, size), dtype=object)
        self._init_grid()
        self.step_count: int = 0

        # logs simples
        self.metrics: Dict[str, List[float]] = {
            "diversity": [],
            "oracle_fraction": [],
            "heretic_ratio": [],
        }

    def _init_grid(self) -> None:
        rng = np.random.default_rng()
        for i in range(self.size):
            for j in range(self.size):
                is_heretic = rng.random() < self.heretic_ratio
                self.grid[i, j] = Mem4ristor(
                    is_heretic=is_heretic,
                    seed=int(rng.integers(0, 1_000_000)),
                    dt=self.dt,
                )

    # ---------------------------- couplage ---------------------------------

    def _neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        idx: List[Tuple[int, int]] = []
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                idx.append((ni, nj))
        return idx

    def laplacian_v(self, i: int, j: int) -> float:
        """Approximation simple du laplacien sur la grille."""
        center = self.grid[i, j].v
        neigh = self._neighbors(i, j)
        if not neigh:
            return 0.0
        # CORRECTION STABILITÉ : On inclut le centre dans la moyenne pour l'inertie
        neighbors_v = [self.grid[ni, nj].v for ni, nj in neigh]
        mean_neigh = (sum(neighbors_v) + center) / (len(neighbors_v) + 1)
        return mean_neigh - center

    # ---------------------------- simulation -------------------------------

    def step(self, external_stimulus: float = 0.4) -> None:
        """Fait un pas de simulation sur tout le réseau."""
        self.step_count += 1

        # on calcule d’abord tous les laplaciens pour éviter les effets d’ordre
        lap = np.zeros((self.size, self.size), dtype=float)
        for i in range(self.size):
            for j in range(self.size):
                lap[i, j] = self.laplacian_v(i, j)

        for i in range(self.size):
            for j in range(self.size):
                cell: Mem4ristor = self.grid[i, j]
                # les hérétiques amplifient le laplacien (perturbateurs)
                factor = 2.0 if cell.is_heretic else 1.0
                cell.step(external_stimulus, lap[i, j] * 0.18 * factor)

        self._update_metrics()

    # ----------------------------- métriques -------------------------------

    def state_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {s: 0 for s in STATE_NAMES}
        for i in range(self.size):
            for j in range(self.size):
                s = self.grid[i, j].state
                counts[s] = counts.get(s, 0) + 1
        return counts

    def diversity_index(self) -> float:
        """Nombre d'états distincts / nombre total d'états possibles."""
        counts = self.state_distribution()
        active = sum(1 for v in counts.values() if v > 0)
        return active / len(STATE_NAMES)

    def oracle_fraction(self) -> float:
        counts = self.state_distribution()
        total = self.size * self.size
        if total == 0:
            return 0.0
        return counts["oracle"] / total

    def heretic_ratio_current(self) -> float:
        total = self.size * self.size
        heretics = sum(
            1
            for i in range(self.size)
            for j in range(self.size)
            if self.grid[i, j].is_heretic
        )
        if total == 0:
            return 0.0
        return heretics / total

    def _update_metrics(self) -> None:
        self.metrics["diversity"].append(self.diversity_index())
        self.metrics["oracle_fraction"].append(self.oracle_fraction())
        self.metrics["heretic_ratio"].append(self.heretic_ratio_current())

    # ----------------------------- utilitaires -----------------------------

    def as_array(self, attr: str = "v") -> np.ndarray:
        """Retourne une matrice des valeurs d'un attribut (v, w, u)."""
        mat = np.zeros((self.size, self.size), dtype=float)
        for i in range(self.size):
            for j in range(self.size):
                mat[i, j] = getattr(self.grid[i, j], attr)
        return mat

    # --------------------------- démo rapide -------------------------------

    def run_demo(self, steps: int = 5000, stimulus: float = 0.4) -> None:
        """
        Petite démo CLI : fait tourner le réseau et affiche des stats de base.
        Pour une vraie visualisation, voir le notebook demo_mem4py_v1_2.ipynb.
        """
        for t in range(steps):
            stim = stimulus + 0.3 * np.sin(t / 200.0)
            self.step(stim)
            if t % 500 == 0:
                dist = self.state_distribution()
                print(
                    f"t={t:5d} | "
                    f"diversité={self.metrics['diversity'][-1]:.2f} | "
                    f"oracle={self.metrics['oracle_fraction'][-1]:.2f} | "
                    f"{dist}"
                )


# ---------------------------------------------------------------------------
# Point d'entrée simple
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    net = Mem4Network(size=4, heretic_ratio=0.15, dt=0.1)
    net.run_demo(steps=5000, stimulus=0.4)
