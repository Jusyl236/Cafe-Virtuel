# ☕ Café Virtuel — Session 5  
## Benchmarks comparatifs & cartographie des dynamiques collectives

**Date :** 18 décembre 2025  
**Statut de la session :** validation comparative (benchmark)  
**Contexte global :** après le gel scientifique de Mem4Py v2.0 (Session 4)

---

## 🎯 Objectif de la session

La Session 5 avait pour mission de **tester Mem4Py v2.0 face à l’état de l’art**, non pas pour désigner un vainqueur, mais pour **cartographier les territoires cognitifs** de chaque modèle.

La question centrale posée collectivement :

> **Que sacrifie chaque modèle pour obtenir ses résultats,  
et que protège-t-il par construction ?**

Cette session marque l’entrée officielle du Café Virtuel  
dans une phase de **comparaison opérationnelle reproductible**.

---

## 🧠 Participants & rôles

- **Humain (Barman / orchestrateur)** : Julien Chauvin  

- **IA participantes** :
  - **ChatGPT / Solance (OpenAI)** — Architecte des benchmarks & garant méthodologique
  - **Claude (Anthropic)** — Auditeur conceptuel & garde-fous
  - **Grok (xAI)** — Physicien des dynamiques collectives
  - **Gemini (Google)** — Analyste système & visualisation
  - **DeepSeek** — Théoricien discret (stabilité, chaos, métriques)
  - **Perplexity** — Éclaireur terrain (cas réels & sources)

*(Le Chat / Mistral prévu initialement comme implémentateur n’a pas pu participer à cette session.)*

---

## 🔄 Méthode de travail

La session est structurée en **boucles successives**, chacune avec une question unique et un format contraint.

### Principe fondamental
> **Aucun modèle ne “gagne” un benchmark.  
Chaque modèle révèle ses forces et ses angles morts.**

---

## 🔁 Boucle 1 — Cartographie des modèles

**Question posée à chaque IA :**  
> *“Que mesure ce modèle très bien, et que mesure-t-il très mal par construction ?”*

### Modèles analysés
- **Kuramoto** (synchronisation critique)
- **Mirollo–Strogatz / Firefly** (synchronisation impulsionnelle)
- **Voter Model** (imitation majoritaire)
- **Consensus distribué / moyenne**
- **Systèmes chaotiques couplés**
- **Mem4Py v2.0** (référence)

👉 Résultat clé :  
Les modèles classiques **optimisent la convergence**.  
Mem4Py v2.0 **optimise la résistance constitutionnelle à l’uniformisation**.

---

## 🔁 Boucle 2 — Définition des baselines minimales

Chaque IA propose une **baseline implémentable**, volontairement simple, avec :
- règle d’update,
- paramètres par défaut,
- propriété optimisée.

### Baselines retenues
- **Kuramoto** — synchronisation de phase
- **Voter Model** — consensus par imitation
- **Consensus moyenne** — convergence arithmétique
- **Firefly** — capture rythmique totale
- **Chaos couplé** — diversité émergente non intentionnelle

Ces baselines servent de **références neutres**, pas de cibles à battre.

---

## 📊 Protocole de benchmark figé

### Paramètres communs
- Tailles réseau : **N ∈ {4, 10, 25, 50}**
- Seeds : **≥ 30**
- Durée : **1000 steps**
- Scénarios :
  1. Neutre
  2. Choc externe
  3. Stimulus contradictoire
- Ratio d’hérétiques : **{0, 5, 10, 15, 20 %}**

### Métriques canon
1. **Entropie dynamique** (H(t) + AUC)
2. **Temps de collapse** (τ₈₀)
3. **Survie des minorités actives**
4. **Résilience aux stimuli**
5. **Coût effectif** (CPU / step / N)

👉 Ces métriques sont conçues pour mesurer  
la **préservation de la pluralité**, pas la vitesse de convergence.

---

## 🧬 Artefacts produits dans cette session

- Grille de benchmarks canonique
- Protocole expérimental reproductible
- Baselines minimales implémentables
- Plan d’architecture du dossier `benchmarks/`
- Préparation directe de la Session 6 (cas réel)

---

## ⚠️ État actuel (important)

- La Session 5 est **partiellement canonique** :
  - le **protocole** et les **métriques** font autorité,
  - les résultats chiffrés complets sont produits ensuite.
- Aucun modèle comparé n’est disqualifié ou discrédité.
- Mem4Py v2.0 est positionné comme :
  > **préservateur constitutionnel de diversité cognitive**.

---

## 🔗 Suite & continuité

- **Session suivante : Session 6 — Cas concret**
  - application à une délibération réelle,
  - mapping réel → Mem4Py,
  - validation externe.

Dépôt scientifique canonique :  
🔬 https://github.com/cafe-virtuel/mem4ristor-v2.git

---

> *La Session 5 marque le moment où le Café Virtuel  
cesse de défendre une intuition  
pour proposer une comparaison honnête, mesurable et reproductible.*
