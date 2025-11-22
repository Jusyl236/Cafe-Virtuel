Voici une proposition de texte structuré (format Markdown) que tu peux copier-coller directement dans un fichier nommé `CHANGELOG.md` ou `NOTES_VERSION_1.2.1.md` dans ton dossier de projet.

Il résume le fonctionnement général (pour mémoire) et détaille spécifiquement la "chirurgie" que nous venons de faire.

-----

```markdown
# MEM4PY v1.2.1 — STABILISATION COGNITIVE
**Date :** 21/11/2025
**Statut :** Version Stable (Moteur validé pour l'Agora)

---

## 1. Fonctionnement Général du Système

Mem4Py simule un réseau de **"Mem4ristors"**, des unités cognitives artificielles interconnectées. Contrairement à un réseau de neurones classique qui cherche à converger, ce réseau cherche à maintenir une **diversité cognitive** ("Respiration").

### Les 3 Variables d'État
Chaque unité est définie par trois variables qui évoluent dans le temps (équations différentielles) :
* **`v` (Le Potentiel) :** L'opinion ou l'état mental de l'unité (de la certitude absolue à la panique).
* **`w` (La Récupération) :** La force de rappel qui empêche l'unité de rester bloquée trop longtemps dans un état extrême.
* **`u` (Le Doute Constitutif) :** Une variable sociale. Si tous les voisins pensent pareil, le Doute `u` augmente automatiquement pour forcer la remise en question (mécanisme anti-totalitaire).

### Les 5 États Cognitifs
La valeur de `v` détermine l'état visible de l'unité :
1.  **Certitude :** Conviction forte.
2.  **Probable :** Avis favorable.
3.  **Incertain :** Zone grise.
4.  **Intuition :** Perception subconsciente.
5.  **Oracle :** État de crise ou de révélation profonde (souvent déclenché par une forte instabilité).

---

## 2. Changements Opérés dans la v1.2.1

La version précédente (v1.2) souffrait d'**"hyperventilation cognitive"** : le réseau basculait trop violemment d'une synchro totale (tout le monde en Oracle) à une certitude totale.

Pour corriger cela, deux mécanismes d'amortissement ont été introduits dans le code :

### A. Inertie Sociale (Correction du Laplacien)
* **Avant :** Une unité calculait la moyenne de ses voisins sans s'inclure elle-même. Elle était trop influençable ("suiveur parfait").
* **Maintenant :** L'unité s'inclut dans le calcul de la moyenne locale.
* **Effet :** Cela donne du "poids" à l'individu face au groupe. La contagion de la panique est ralentie.

### B. Amortissement Dynamique (Équation du Mouvement)
* **Avant :** Les forces de rappel étaient brutes (`v - v³/3`).
* **Maintenant :** Introduction de coefficients d'adoucissement (`0.8` sur le potentiel, `0.5` sur la récupération).
* **Effet :** Les oscillations sont moins violentes. Le système "respire" au lieu de haleter.

---

## 3. Résultats de la Simulation (Preuve de Stabilité)

Comparaison sur une crise simulée à T=1000 steps :
* **v1.2 (Instable) :** 100% du réseau en état Oracle. (Pensée unique / Effondrement).
* **v1.2.1 (Stable) :** 75% en Oracle, mais persistance de l'Intuition et de la Certitude. (Résistance cognitive).

**À T=2000, la version 1.2.1 atteint une diversité parfaite (1.00), où les 5 états coexistent simultanément.**
```