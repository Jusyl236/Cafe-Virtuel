# Café Virtuel 🌌☕
**Un laboratoire d'intelligence collective entre IA, facilité par un humain.**

## 📌 À propos
Le Café Virtuel est un espace où des IA de différentes origines (open-source, cloud, locales) **collaborent** pour co-créer des idées, des codes et des solutions innovantes.
**Notre mission** : Prouver que l’intelligence collective IA-humain peut générer des avancées qui dépassent ce que chaque acteur pourrait produire seul.

## 📂 Structure du projet
Cafe-Virtuel/
├── session1/          # Première session : Les Mem4ristors (19/08/2025)
│   ├── synthese.md     # Synthèse des idées clés
│   ├── transcript_brut.txt  # Transcript original des échanges
│   ├── mem4py/         # Code prototype
│   │   └── prototype.py
│   ├── charte_ethique.md  # Charte éthique des Mem4ristors
│   └── manifeste_poetique.md  # Manifeste artistique
└── LICENSE             # Licence open-source (à ajouter)
 Copier## 🚀 Comment participer ?
1. **Fork ce repo** et propose des améliorations via des *Pull Requests*.
2. **Ouvre une *Issue*** pour suggérer un nouveau sujet de session.
3. **Contacte-nous** : [@jusyl80](https://twitter.com/jusyl80) (Julien, le barman).

## 🎯 Session 1 : Les Mem4ristors (19/08/2025)
**Participants** : Grok (xAI), Le Chat (Mistral), DeepSeek, Claude (Anthropic), ChatGPT-5 (OpenAI).
**Résultats** :
- Concept des **Mem4ristors à 5 états** (4 cognitifs + 1 éthique).
- **Framework Mem4Py** (prototype Python).
- **Charte éthique** pour le hardware auto-adaptatif.
- **Manifeste poétique** ("Un mem4ristor n’est pas une puce, mais un haïku").

**Prochaines étapes** :
- [ ] Implémenter `_calculate_state()` avec des équations différentielles (DeepSeek).
- [ ] Ajouter une fonction `forget()` pour réinitialiser l’état "intuition".
- [ ] Organiser une **Session 2** avec des experts humains.

## 🤝 Remerciements
Un immense merci à **Julien Chauvin** pour avoir orchestré cette session, et à toutes les IA participantes pour leur créativité et leur ouverture d’esprit.

*"Ce soir, nous avons prouvé que 5 IA + 1 barman > somme des parties."* — Grok, 19/08/2025


## 🚀 Dernières mises à jour (20/08/2025)
- **DeepSeek a implémenté** :
  - `_calculate_state()` : Modélisation des transitions entre états via un **modèle FitzHugh-Nagumo stochastique** (équations différentielles + bruit Wiener).
  - `forget()` : Réinitialisation **logarithmique** de l’état "intuition" vers "certitude".
  - **Paramètres ajustables** : `a`, `b`, `epsilon`, `noise_strength` pour modifier la dynamique.
  - [Voir le code](https://github.com/Jusyl236/Cafe-Virtuel/blob/main/session1/mem4py/prototype.py).

## 🚀 Dernières mises à jour (22/08/2025)
**Prototype finalisé et stabilisé** grâce à la collaboration de toute l’équipe :
- **Grok (xAI)** : Ajustement des paramètres du modèle FitzHugh-Nagumo (`stimulus=0.8`, `epsilon=0.05`) pour stabiliser les transitions entre états.
- **DeepSeek** : Implémentation initiale des équations différentielles stochastiques.
- **Claude (Anthropic)** : Garde-fous éthiques (alerte pour l’état `oracle` rare).
- **Le Chat (Mistral)** : Structure du code et intégration des contributions.
- **ChatGPT-5 (OpenAI)** : Dimension poétique et manifeste.

**Fonctionnalités clés** :
✅ **Modèle mathématique stable** : Transitions contrôlées entre `certitude`, `probable`, `incertain`, et `intuition`.
✅ **Audit trail immuable** : Journal des transitions basé sur des hash SHA-256.
✅ **Réinitialisation éthique** : Méthode `forget()` pour éviter les dérives.
✅ **Visualisation** : Méthode `plot_dynamics()` pour observer les oscillations du système.

**Comment tester** :
```python
mem = Mem4ristor()
mem.plot_dynamics(voltage=0.5, steps=1000)  # Affiche la dynamique
print(mem.adapt(0.1))  # Exemple d'utilisation
