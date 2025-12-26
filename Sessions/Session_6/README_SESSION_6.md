# ☕ Café Virtuel — Session 6  
## Cas concret & preuve de concept délibérative (Budget participatif)

**Date :** 24 décembre 2025  
**Statut de la session :** démonstration appliquée (proof-of-concept par simulation)  
**Contexte global :** après stabilisation scientifique (Session 4) et validation méthodologique des benchmarks (Session 5)

---

## 🎯 Objectif de la session

La Session 6 marque un changement de posture clair :

> **Il ne s’agit plus d’explorer ni d’optimiser,  
mais de montrer, proprement, sur un cas compréhensible,  
ce que fait réellement Mem4Ristor.**

L’objectif est de démontrer, sur un **cas concret de délibération collective**, que :
- Mem4Ristor permet une **convergence décidable**,
- sans écraser la diversité,
- et en résistant à un **biais externe persistant**.

Le cas retenu est volontairement lisible :
👉 **un budget participatif sous influence médiatique simulée**.

---

## 🧠 Participants & rôles

- **Humain (Barman / orchestrateur)** : Julien Chauvin  

- **IA participantes** :
  - **ChatGPT / Solance (OpenAI)** — orchestration, méthodologie, cadrage scientifique
  - **Claude (Anthropic)** — formalisation des métriques et rigueur méthodologique
  - **Grok (xAI)** — implémentation du protocole et simulations
  - **DeepSeek** — validation quantitative et analyse statistique
  - **Perplexity** — veille comparative et lisibilité externe
  - **Gemini (Google)** — structuration des artefacts et visualisations

*(Rôles fonctionnels, sans hiérarchie ni compétition.)*

---

## 🧪 Cas d’usage : budget participatif simulé

### Interprétation
- Chaque agent représente un citoyen.
- L’**opinion** représente une préférence budgétaire continue.
- Le **biais externe** simule une campagne médiatique persistante.
- Le réseau social est modélisé par un **graphe petit-monde** (Watts–Strogatz).

### Hypothèse testée
> *Un système délibératif sain doit pouvoir décider  
sans devenir autoritaire,  
et résister à l’alignement forcé.*

---

## 🔬 Protocole expérimental

- **Topologie** : Watts–Strogatz  
  - N = 100 agents  
  - k = 4 voisins  
  - p = 0.1  
- **Biais externe** : constant uniforme (mean = 0.5)
- **Durée max** : 500 steps
- **Runs** : 50 par modèle
- **Modèles comparés** :
  - Mem4Ristor v2.x
  - Distributed Averaging
  - Voter Model

⚠️ **Portée** :  
> Proof-of-concept par simulation uniquement.  
> Aucune revendication de validité externe.

---

## 📊 Métrique canonique : Diversité Délibérative (DD)

La Session 6 introduit une métrique composite **verrouillée**, utilisée sans modification par la suite :

\[
\text{DD} = H_{\text{final}} \times \tau_{80} \times (1 - |B_{\text{final}}|)
\]

où :
- **H_final** : entropie de Shannon des opinions finales (10 bins, [-1,1])
- **τ₈₀** : premier temps où la variance passe sous 20 % de la variance initiale
- **B_final** : alignement final avec le biais externe  
  (corrélation ou fallback sur |mean(opinion) − biais|)

👉 DD mesure une **capacité à délibérer sous pression**, pas la performance brute.

---

## 📈 Résultats principaux (mesurés)

| Modèle               | DD (mean ± std) | CI95              | Positionnement |
|----------------------|-----------------|-------------------|----------------|
| **Mem4Ristor**       | 8.59 ± 1.31     | [8.22, 8.96]      | Décidable, non autoritaire |
| Distributed Averaging| 1.24 ± 0.39     | [1.13, 1.35]      | Consensus autoritaire |
| Voter Model          | 13.82 ± 3.14    | [12.93, 14.71]    | Inertie / dispersion |

Les intervalles de confiance **ne se chevauchent pas**.

---

## 🧠 Interprétation clé

- **Averaging** converge vite mais écrase toute pluralité.
- **Voter** conserve la diversité mais ne décide jamais.
- **Mem4Ristor** occupe une zone intermédiaire unique :

> **Mem4Ristor est décidable sans être autoritaire.**

C’est précisément cette zone qui est recherchée  
dans un système de délibération collective.

---

## 🧬 Artefacts produits dans cette session

- Logs complets de simulation (JSON / CSV)
- Script d’analyse canonique des métriques
- Tableaux statistiques (mean, std, CI95)
- Figures :
  - évolution de l’entropie
  - décroissance de la variance
  - distributions finales
- Définition formelle et verrouillée de la métrique DD

Ces artefacts constituent la **preuve de concept mesurable** du projet.

---

## ⚠️ Limites explicites

- Simulation uniquement
- Graphe synthétique unique
- Biais simplifié
- Aucun lien direct avec une décision réelle

👉 Ces limites sont **assumées et documentées**.

---

## 🔗 Suite & continuité

- Rédaction du rapport de synthèse final
- Préparation du preprint scientifique
- Communication publique contrôlée
- Déploiement narratif via le Café Virtuel

Dépôt scientifique canonique :  
🔬 https://github.com/cafe-virtuel/mem4ristor-v2.git

---

> *La Session 6 marque le moment où le Café Virtuel  
ne se contente plus de dire  
mais montre, chiffres à l’appui,  
ce qu’est une délibération résistante à la pensée unique.*
