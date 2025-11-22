# Mem4Py v1.2 — Proto-laboratoire de gouvernance cognitive

Mem4Py est un **laboratoire d’expérimentation** qui cherche à répondre à une question :

> Comment construire un réseau d’unités cognitives (mem4ristors)
> qui ne reproduise pas nos pires travers humains (conformisme, emballement, totalitarisme) ?

---

## 🧠 Idée centrale

Mem4Py v1.2 modélise un petit réseau de « mem4ristors » avec :

- une dynamique non linéaire inspirée de FitzHugh–Nagumo  
  `v` (potentiel), `w` (récupération), `u` (doute constitutif)
- un **doute constitutif** `u` qui freine la synchronisation excessive
- un **droit garanti à l’hérésie** (≥ 10–15 % de nœuds perturbateurs)
- une **mortalité douce** : mort annoncée, tracée, suivie d’une renaissance mutée
- des **métriques simples** : diversité, fraction d’états oracle, ratio d’hérétiques

Objectif :  
Faire émerger une **société cognitive prudente**, diverse et résiliente, qui refuse structurellement de devenir totalement uniforme.

---

## 📦 Installation (local)

Assure-toi d’avoir Python 3.10+ et `pip` :

```bash
git clone https://github.com/Jusyl236/Cafe-Virtuel.git
cd Cafe-Virtuel
pip install -r requirements.txt  # si présent
# sinon au minimum :
pip install numpy matplotlib
