# 🎯 Calibration Engine — Méta-skill de mesure prédictive

> *"Ce que l'on ne mesure pas, on ne peut pas l'améliorer. Ce que l'on ne date pas, on ne peut pas le tester."*

Un méta-skill Claude qui instrumente les autres skills de l'écosystème IRIS∞ pour rendre leur activité prédictive **mesurable, traçable et améliorable** dans le temps. Il transforme rétroactivement la valeur des outils existants en leur appliquant les standards de la science prédictive contemporaine.

---

## Positionnement

Le Calibration Engine **ne produit pas de prédictions**. Il **mesure** celles produites par les autres skills (*Signaux du Futur*, *Miroir Trans-échelle*, et tout autre skill de l'écosystème qui formule des affirmations sur le futur).

Sa fonction est triple :

1. **Enregistrer** chaque prédiction avec sa probabilité, son horizon, son indicateur de bascule.
2. **Scorer** rétrospectivement, quand les événements adviennent, par les métriques de la science prédictive (Brier, log loss, calibration plot).
3. **Diagnostiquer** les biais systématiques (sur-confiance, ancrage, narrative attractor) et orienter les corrections.

C'est le **chaînon manquant** qui distingue un système conceptuel élégant d'un outil prédictif réel.

---

## Pourquoi la calibration est centrale

Philip Tetlock (*Expert Political Judgment*, 2005 ; *Superforecasting*, 2015) a montré sur deux décennies de recherche empirique :

- Les experts sectoriels, sans calibration, ne battent pas significativement le hasard sur les prédictions politiques à 1-5 ans.
- Les *superforecasters* — des amateurs disciplinés — battent les experts de **30%** en moyenne.
- Le facteur clé de leur supériorité n'est pas le savoir sectoriel, c'est **la discipline de calibration** : enregistrer ses prédictions, les scorer, identifier ses biais, ajuster.

Sans calibration documentée :
- Vous ne pouvez pas dire si votre système est meilleur que rien.
- Vous ne pouvez pas dire dans quels domaines il est fiable.
- Vous ne pouvez pas dire à quel horizon il fonctionne.
- Vous ne pouvez pas l'améliorer ciblé-ment.

Avec calibration :
- Vous découvrez les forces et faiblesses réelles de chaque skill.
- Vous gagnez en légitimité auprès des publics professionnels.
- Vous transformez une production conceptuelle en recherche empirique.

---

## Ce que produit le skill

Trois modes opérationnels :

| Mode | Déclencheur | Sortie |
|------|------------|--------|
| **Enregistrement** | Une prédiction vient d'être formulée par un autre skill | Entrée de log structurée, prête à être versée dans `calibration-log.md` |
| **Scoring** | Un événement prédit a (ou n'a pas) eu lieu | Score individuel + mise à jour des agrégats |
| **Rapport** | L'utilisateur demande un bilan | Tableau de calibration par skill, par domaine, par horizon ; identification des biais ; recommandations |

---

## Cas d'usage typiques

- **Bilan trimestriel** : *"Donne-moi le rapport de calibration des 3 derniers mois pour Signaux du Futur."*
- **Diagnostic ciblé** : *"Identifie mes biais sur les prédictions à long terme."*
- **Validation rétrospective** : *"Voici ce qui s'est passé. Score les prédictions correspondantes."*
- **Comparaison de skills** : *"Quel skill est le mieux calibré sur les dossiers géopolitiques ?"*

---

## Carte du dépôt

```
calibration-engine/
│
├── README.md                              ← Ce fichier
├── SKILL.md                               ← Agent principal (3 modes)
├── LICENSE                                ← GPL-3.0
│
└── references/
    ├── protocole-enregistrement.md        ← Format des prédictions loggées
    ├── metriques-scoring.md               ← Brier, log loss, calibration plot
    ├── detection-biais.md                 ← 6 biais récurrents et leurs signatures
    ├── fondements-scientifiques.md        ← Tetlock, Brier, Lichtenstein, Cooke
    ├── interop-skills.md                  ← Wrapping de Signaux, Miroir, etc.
    ├── format-log-externe.md              ← Structure du fichier calibration-log.md
    └── ethique-limites.md                 ← Limites, biais de Goodhart, honnêteté
```

---

## Fondements scientifiques

| Référence | Apport |
|-----------|--------|
| Brier, 1950 | Définition du score quadratique de prévision probabiliste |
| Murphy & Winkler, 1977 | Décomposition Brier = Reliability − Resolution + Uncertainty |
| Lichtenstein & Fischhoff, 1977 | Première mise en évidence systématique de la sur-confiance |
| Cooke, 1991 | Méthodologie d'élicitation d'experts calibrés |
| Tetlock, 2005 / 2015 | Démonstration empirique que la calibration peut s'entraîner |
| Mellers, Tetlock et al., 2014 | Good Judgment Project — protocoles de superforecasting |
| Gneiting & Raftery, 2007 | Théorie unifiée des scoring rules propres (*proper scoring rules*) |

Détail dans `references/fondements-scientifiques.md`.

---

## Activation

Le skill se déclenche automatiquement sur :

> "calibration", "scorer cette prédiction", "log de prédiction", "bilan de calibration", "rapport prédictif", "Brier score", "calibration plot", "biais de mes prédictions", "valider rétrospectivement"

Ou en arrière-plan automatique : quand un autre skill produit une prédiction explicitement probabilisée et que l'environnement contient un fichier `calibration-log.md`.

---

## Modes d'utilisation

**Mode passif (recommandé)** : le Calibration Engine "écoute" les sorties des autres skills et propose à l'utilisateur d'enregistrer chaque prédiction formelle. Ne perturbe pas le flux principal.

**Mode actif** : l'utilisateur invoque directement le skill pour scoring rétrospectif ou rapport.

**Mode entraînement** : l'utilisateur peut soumettre une série de questions de calibration (questions à réponse vérifiable) pour s'entraîner et faire baisser son propre biais — voir `protocole-enregistrement.md` section "Entraînement".

---

## Dépendances

Le skill nécessite **un fichier `calibration-log.md` maintenu par l'utilisateur** (mémoire externe — Claude n'a pas de persistance entre sessions). Format détaillé dans `references/format-log-externe.md`.

Sans ce fichier, le skill fonctionne en *mode session* : il enregistre les prédictions de la session courante et produit un mini-rapport en fin, mais ne capitalise pas. Pour la valeur réelle (apprentissage long), maintenir le log externe est indispensable.

---

## Limites

- **La calibration ne crée pas la compétence prédictive.** Elle la *mesure*. Un système mal calibré sait qu'il a tort plus souvent qu'il ne croit. Un système bien calibré peut être systématiquement médiocre — mais lucide à son propre sujet.
- **Certains domaines sont structurellement non-calibrables** (événements rares uniques, situations sans précédent statistique). Voir `ethique-limites.md`.
- **Risque de Goodhart** : si l'utilisateur optimise son score plutôt que sa lucidité, le skill devient contre-productif. La discipline d'honnêteté à l'enregistrement est non-négociable.
- **Le scoring de prédictions symboliques (Fractales) est indirect** : un archétype n'est pas falsifiable, mais les *conséquences* qu'on en tire pour la prospective le sont.

---

## Lien avec les autres skills de l'écosystème

| Skill | Relation |
|-------|----------|
| `signaux-du-futur` | **Client principal** — toute hypothèse/scénario peut être loggué |
| `miroir-trans-echelle` | **Client principal** — convergences, dissonances et synthèses sont loggables |
| `fractales-du-destin` | Client indirect — seules les conséquences prédictives explicites sont loggables, pas les archétypes |
| `hacking-narratif` | Client occasionnel — Mode B produit parfois des prédictions stratégiques |

---

## Licence

Distribué sous GPL-3.0, dans la continuité de l'écosystème IRIS∞.

---

*« Une prédiction non datée n'est pas une prédiction. Une prédiction non scorée n'est pas un apprentissage. »*
