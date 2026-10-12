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

Les travaux de Philip Tetlock et de ses collègues (*Expert Political Judgment*, 2005 ; *Superforecasting*, 2015 ; Good Judgment Project, 2011-2015) établissent notamment :

- Les experts, en moyenne, font à peine mieux que des règles simples ou le hasard sur des prédictions politiques à horizon de plusieurs années.
- Dans le tournoi IARPA, l'équipe Good Judgment a battu le groupe contrôle de plus de 50 % ; Good Judgment affirme aussi une précision supérieure de plus de 30 % à celle d'analystes du renseignement (chiffre institutionnel, méthode non publiée sur la page source).
- La précision dépend d'aptitudes et de dispositions, mais aussi de pratiques entraînables : entraînement court (gain de 6 à 11 % sur le Brier ; Chang et al., 2016), travail en équipe, mises à jour fréquentes, et **retour d'information sur ses propres prédictions** — ce que fournit ce skill.

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
├── README.md                              ← Ce fichier (page du dépôt, non chargé par l'agent)
├── SKILL.md                               ← Agent principal (3 modes)
├── LICENSE                                ← GPL-3.0
├── scripts/
│   └── scoring.py                         ← Brier, log loss, BSS, Murphy, bins (stdlib)
├── tests/
│   ├── test_scoring.py                    ← Vérification des valeurs citées
│   └── fixtures/exemple-rapport.json      ← Log fictif du rapport d'exemple
│
└── references/
    ├── protocole-enregistrement.md        ← Format des prédictions loggées
    ├── metriques-scoring.md               ← Brier, log loss, calibration plot
    ├── detection-biais.md                 ← 6 familles de biais et leurs signatures
    ├── notes-non-falsifiables.md          ← Gabarit pour les énoncés non scorables
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
| Murphy, 1973 | Décomposition Brier = Reliability − Resolution + Uncertainty |
| Fischhoff, Slovic & Lichtenstein, 1977 ; Lichtenstein & Fischhoff, 1977 | Sur-confiance aux certitudes extrêmes ; effet difficile/facile |
| Cooke, 1991 | Méthodologie d'élicitation d'experts calibrés |
| Tetlock, 2005 / 2015 | Évaluation empirique du jugement politique expert |
| Mellers et al., 2014, 2015 ; Chang et al., 2016 | Good Judgment Project — effets de l'entraînement, des équipes, des dispositions |
| Gneiting & Raftery, 2007 | Règles de score strictement propres (Brier, log loss) |
| Gneiting, Balabdaoui & Raftery, 2007 | Calibration et sharpness |

Détail dans `references/fondements-scientifiques.md`.

---

## Activation

Le déclenchement repose sur le champ `description` du `SKILL.md`, seul champ chargé à l'avance par les agents conformes à la spécification Agent Skills. Formulations typiques : « scorer cette prédiction », « bilan de calibration », « Brier », « biais de mes prédictions », « ai-je eu raison ».

## Tests

```bash
python3 -m unittest discover -s tests -v
```

---

## Modes d'utilisation

**Mode passif (recommandé)** : le Calibration Engine "écoute" les sorties des autres skills et propose à l'utilisateur d'enregistrer chaque prédiction formelle. Ne perturbe pas le flux principal.

**Mode actif** : l'utilisateur invoque directement le skill pour scoring rétrospectif ou rapport.

**Mode entraînement** : l'utilisateur peut soumettre une série de questions de calibration (questions à réponse vérifiable) pour s'entraîner — voir `references/protocole-enregistrement.md`, section « Mode entraînement ».

---

## Dépendances

Le skill nécessite **un fichier `calibration-log.md` maintenu par l'utilisateur**, qui fait foi entre sessions. Les scores sont calculés par `scripts/scoring.py` (Python 3, bibliothèque standard). Format détaillé dans `references/format-log-externe.md`.

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
| `superforecasting-protocol` | **Client principal** — fiches de prédiction déjà au format du log |
| `bayesian-updater` | Alimente le champ `revisions` ; audite les révisions passées |
| `prediction-engine` | Orchestrateur qui route vers ce skill (Mode C) |
| `signaux-du-futur` *(externe)* | Client principal — hypothèses et scénarios loggables |
| `miroir-trans-echelle` *(externe)* | Hypothèses P2 et dérivations P3, sous plafond narrative attractor |
| `fractales-du-destin` *(externe)* | Client indirect — seules les conséquences prédictives explicites sont loggables |
| `hacking-narratif` *(externe)* | Client occasionnel — Mode B |

---

## Licence

Distribué sous GPL-3.0, dans la continuité de l'écosystème IRIS∞.

---

*« Une prédiction non datée n'est pas une prédiction. Une prédiction non scorée n'est pas un apprentissage. »*
