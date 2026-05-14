# 🎯 Superforecasting Protocol — Discipline de prédiction structurée

> *"Une prédiction qui ne précise ni horizon, ni probabilité, ni condition de réfutation n'est pas une prédiction. C'est une opinion."*

Un skill Claude qui applique la **discipline du Good Judgment Project** (Tetlock & Mellers) à toute question prospective : décomposition Fermi, base rates, scénarios probabilisés, indicateurs observables, conditions de falsification. Transforme une intuition en prédiction structurée, scorable, améliorable.

---

## Positionnement

Ce skill ne *remplace* pas l'analyse OSINT ni l'intuition stratégique. Il les **discipline**. Il prend une question prospective brute et en produit une *prédiction techniquement valide* — c'est-à-dire :

- assortie d'une probabilité numérique explicite,
- décomposée en sous-questions tractables,
- ancrée dans une base rate historique,
- formulée en plusieurs scénarios concurrents qui somment à 100%,
- accompagnée d'indicateurs observables datés,
- réfutable par des conditions précises.

C'est la discipline minimum sans laquelle aucun système prédictif ne peut s'améliorer dans le temps.

---

## Pourquoi ce skill

L'analyse géopolitique, économique et organisationnelle souffre d'une faille structurelle documentée par Tetlock dans *Expert Political Judgment* (2005) : les experts produisent en moyenne des prédictions **à peine meilleures que le hasard**, et systématiquement moins bonnes qu'un protocole disciplinaire appliqué par des amateurs entraînés.

Le facteur clé n'est pas le savoir sectoriel. C'est la **discipline méthodologique**. Le Good Judgment Project (2011-2015), financé par l'IARPA, a démontré qu'un protocole en 7 étapes permettait à des prévisionnistes amateurs de battre les analystes professionnels du renseignement américain de 30% en moyenne (Mellers, Stone, Atanasov et al., *Psychological Science*, 2015).

Ce skill encode ce protocole et le rend applicable à toute question prospective de l'écosystème IRIS∞.

---

## Ce que produit le skill

Sur une question prospective soumise, le skill produit une **fiche de prédiction structurée** comprenant :

| Section | Contenu |
|---------|---------|
| **Reformulation** | La question en forme falsifiable (date, indicateur, seuil) |
| **Triage** | Type de question, horizon, prédictibilité estimée |
| **Décomposition** | Sous-questions tractables (Fermi) |
| **Base rate** | Fréquence historique (outside view) |
| **Inside view** | Ajustements spécifiques au cas |
| **Scénarios** | 3 à 5 scénarios concurrents avec probabilités sommant à 100% |
| **Indicateurs** | Événements observables datés qui actualiseraient chaque scénario |
| **Réfutation** | Conditions précises de falsification |
| **Cadence de révision** | Quand reprendre l'analyse |

Cette fiche est conçue pour être :
- **scorable** rétrospectivement par `calibration-engine`
- **actualisable** par `bayesian-updater` quand l'info évolue
- **traçable** pour audit ou apprentissage rétrospectif

---

## Cas d'usage typiques

- **Question géopolitique** : *"Quelle est la probabilité d'une rupture diplomatique entre X et Y dans les 12 prochains mois ?"*
- **Décision stratégique** : *"Cette restructuration aboutira-t-elle dans les délais annoncés ?"*
- **Prospective sectorielle** : *"L'industrie X subira-t-elle une consolidation majeure d'ici 2027 ?"*
- **Anticipation organisationnelle** : *"Ce dirigeant restera-t-il en fonction au-delà de l'horizon Z ?"*

Le skill est **inadapté** aux questions :
- Sans horizon temporel ("un jour", "à long terme")
- Sans indicateur observable ("la situation va se dégrader")
- À portée existentielle/morale ("est-ce que la démocratie va survivre")
- Sans base de comparaison historique

Dans ces cas, le skill **demande une reformulation** plutôt que de produire une fausse prédiction.

---

## Carte du dépôt

```
superforecasting-protocol/
│
├── README.md                              ← Ce fichier
├── SKILL.md                               ← Agent principal (protocole 7 étapes)
├── LICENSE                                ← GPL-3.0
│
└── references/
    ├── protocole-7-etapes.md              ← Détail opératoire de chaque étape
    ├── base-rates-outside-view.md         ← Méthode Kahneman + sources de base rates
    ├── decomposition-fermi.md             ← Décomposer une question complexe
    ├── scenarios-probabilites.md          ← Probabilités granulaires & somme à 100%
    └── biais-courants.md                  ← Pièges à éviter (overconfidence, narrative…)
```

---

## Fondements théoriques

| Référence | Apport |
|-----------|--------|
| **Tetlock & Gardner (2015)** — *Superforecasting* | Protocole opérationnel principal |
| **Tetlock (2005)** — *Expert Political Judgment* | Diagnostic : pourquoi les experts échouent |
| **Mellers et al. (2015)** — Good Judgment Project results | Validation empirique du protocole |
| **Kahneman (2011)** — *Thinking, Fast and Slow* | Outside view, base rate, biais |
| **Heuer (1999)** — *Psychology of Intelligence Analysis* | ACH, contrôle des biais |
| **Klein (2007)** — Pre-Mortem technique | Discipline anti-surajustement |
| **Hubbard (2010)** — *How to Measure Anything* | Calibration de l'incertitude |

Détail dans chaque fichier de référence.

---

## Activation

Le skill se déclenche automatiquement sur :

> "prédiction structurée", "forecast", "superforecasting", "probabilité de", "quelle est la probabilité", "horizon prospectif", "discipline de prédiction", "GJP protocol"

Ou sur toute question prospective qui demande une probabilité explicite.

---

## Modes d'utilisation

**Mode rapide** (10-15 min) : protocole compact, scénarios essentiels.
**Mode standard** (30-45 min) : protocole complet en 7 étapes.
**Mode approfondi** : protocole + interaction avec `bayesian-updater` pour mise à jour itérative + journalisation pour `calibration-engine`.

---

## Dépendances et interopérabilité

Ce skill est conçu pour fonctionner **seul ou orchestré** :

| Skill frère | Relation |
|-------------|----------|
| `signaux-du-futur` | Source amont — fournit le matériau OSINT brut |
| `bayesian-updater` | Skill aval — actualise les prédictions quand l'info arrive |
| `calibration-engine` | Skill aval — score les prédictions a posteriori |
| `miroir-trans-echelle` | Skill cousin — complète par lecture symbolique croisée |

---

## Limites

- **La discipline ne crée pas la prescience.** Même rigoureux, le skill ne prédit pas mieux que ce que l'information disponible permet.
- **Les probabilités sont des estimations subjectives.** Elles ne sont pas des fréquences objectives — elles deviennent valides *à mesure que la calibration s'établit*.
- **Le protocole est coûteux.** Une bonne prédiction structurée prend 30-60 minutes minimum. Ce n'est pas un outil de réaction rapide.
- **Le skill ne convient pas aux décisions à effet de seuil critique** (vie/mort, action immédiate) — il convient à la décision sous incertitude raisonnée.

---

## Licence

GPL-3.0, écosystème IRIS∞.

---

*« La prédiction n'est pas un don. C'est une discipline. Elle se mesure, elle s'entraîne, elle s'améliore — ou elle reste opinion. »*
