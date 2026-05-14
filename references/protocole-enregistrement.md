# Protocole d'enregistrement — Comment logger une prédiction

Ce fichier définit la **discipline d'enregistrement** d'une prédiction dans le Calibration Engine. Il décrit les champs obligatoires, les règles de falsifiabilité, la validation préalable, et donne des exemples annotés (bons et mauvais).

---

## Pourquoi un protocole strict

Sans discipline d'enregistrement, le log devient un ramassis d'affirmations vagues qu'on peut, après coup, réinterpréter dans n'importe quel sens. C'est exactement ce que la calibration cherche à empêcher.

Le protocole impose donc trois exigences non-négociables, et c'est leur stricte application qui fait la valeur du log :

1. **Falsifiabilité préalable** — l'événement prédit doit être *observable* à l'horizon fixé.
2. **Probabilité explicite** — entre 0.05 et 0.95 (pas de certitude).
3. **Indicateur de bascule** — au moins un événement intermédiaire vérifiable.

Une affirmation qui ne remplit pas ces trois conditions **n'est pas enregistrable**. Le skill demande reformulation ou refuse.

---

## Les champs obligatoires

Chaque entrée de prédiction porte les champs suivants :

| Champ | Type | Contenu |
|-------|------|---------|
| `id` | string | Identifiant unique : `PRED-YYYY-MM-DD-NNN` |
| `timestamp` | datetime ISO | Date+heure d'enregistrement |
| `skill_source` | string | Skill qui a produit la prédiction (ou "humain" si formulée directement) |
| `domaine` | string | géopolitique / économie / social / technologique / personnel / autre |
| `sujet` | string | Désignation courte (5-10 mots) du dossier |
| `prediction` | string | L'énoncé prédictif complet, **falsifiable** |
| `probabilite` | float [0.05–0.95] | Probabilité explicite de réalisation |
| `horizon_jours` | integer | Délai maximal en jours après lequel l'entrée passe à `expirée` |
| `indicateur_bascule` | list | Au moins un événement intermédiaire observable |
| `condition_refutation` | string | Énoncé clair de ce qui invaliderait la prédiction |
| `statut` | enum | ouverte / résolue / expirée / non-évaluable |

---

## Les champs optionnels mais recommandés

| Champ | Pourquoi |
|-------|----------|
| `hypotheses_concurrentes` | Liste les hypothèses rivales avec leurs probabilités. Force la pensée ACH. |
| `biais_surveilles` | Liste des biais identifiés comme menace (confirmation, ancrage, etc.). |
| `base_rate_estimee` | Fréquence historique de ce type d'événement. Discipline Tetlock. |
| `sources` | URLs ou références aux sources OSINT principales. |
| `confiance_metacognitive` | Niveau (basse/moyenne/haute) de votre confiance dans votre propre confiance. |
| `comment_changer_avis` | Quels indicateurs feraient bouger la probabilité ? |

---

## Règles de falsifiabilité

Une prédiction est **enregistrable** si et seulement si elle satisfait les **trois conditions de Popper opérationnelles** :

### Condition 1 — Événement observable

L'énoncé doit décrire un événement vérifiable par observation publique, pas un état interne ou une "tendance générale".

❌ *"X va devenir plus puissant"* → non observable directement
✅ *"X obtiendra plus de 51% des voix au scrutin du 14 juin 2026"*

❌ *"L'inflation reste préoccupante"* → non observable
✅ *"L'inflation glissante annuelle sera > 4% à fin Q3 2026 selon l'INSEE"*

### Condition 2 — Seuil quantitatif ou qualitatif net

L'énoncé doit fixer un seuil au-dessus/en-dessous duquel le verdict bascule.

❌ *"Le cours de l'action va monter"* → quel seuil ?
✅ *"Le cours de l'action atteindra ou dépassera 50€ avant le 30 septembre 2026"*

❌ *"La crise va s'aggraver"* → quel critère d'aggravation ?
✅ *"Le nombre de manifestations recensées par le Ministère de l'Intérieur dépassera 500 par mois pendant au moins 2 mois consécutifs"*

### Condition 3 — Date limite

L'énoncé doit fixer un horizon temporel borné, au-delà duquel la prédiction est résolue (positivement ou négativement).

❌ *"X arrivera un jour"* → horizon infini, jamais falsifiable
✅ *"X arrivera avant le 31 décembre 2026"*

---

## Le test du sceptique

Avant d'enregistrer, le skill applique mentalement le **test du sceptique** : un tiers méfiant pourrait-il, à la date d'échéance, déterminer **sans ambiguïté** si la prédiction est vraie ou fausse ?

- Si **oui** → enregistrable.
- Si **non** → demander reformulation.

Si après reformulation l'utilisateur ne parvient pas à satisfaire le test, le skill propose deux options :
- Marquer l'entrée comme **note prospective non-scorable** (utile pour mémoire, mais hors agrégats).
- Abandonner l'enregistrement et noter dans une annexe `notes-non-falsifiables.md`.

---

## Règles de probabilité

### Plage admise : 0.05 à 0.95

Les valeurs 0 et 1 sont **interdites**. Elles signifient "certitude", qui n'a pas sa place en prédiction.

L'utilisateur qui dit *"je suis sûr à 100%"* est invité à reformuler à 0.95 et à indiquer dans un commentaire pourquoi cette quasi-certitude.

Au-delà de 0.95, un Brier individuel est si bas en cas d'échec qu'il distord la moyenne. Au-delà de 0.99, un échec produit un log loss astronomique. La discipline scientifique évite ces extrêmes.

### Pas d'arrondi excessif

Préférer `0.65` à `0.7` quand c'est ce que l'analyse suggère. La granularité informe sur l'effort de calibration.

À l'inverse, ne pas afficher une fausse précision : `0.642` est suspect si rien dans l'analyse ne justifie ce niveau. Préférer `0.65`.

### Tenir compte de la base rate

Tetlock insiste : avant de probabiliser, demander *"à quelle fréquence ce type d'événement se produit-il historiquement ?"*. Cette **base rate** est l'ancrage naturel. La probabilité personnelle s'éloigne du base rate dans la mesure où on a des raisons spécifiques de penser que ce cas est différent.

Un champ optionnel `base_rate_estimee` permet de tracer cet ancrage.

---

## L'indicateur de bascule

L'indicateur de bascule est un **événement intermédiaire** dont l'apparition (ou non) modifierait votre probabilité avant l'échéance.

Il a deux fonctions :

1. **Permettre l'actualisation bayésienne** entre la date d'enregistrement et la date de résolution.
2. **Forcer la spécification mentale** : quelqu'un qui ne sait pas formuler un indicateur de bascule ne sait pas vraiment ce qu'il prédit.

### Bons indicateurs

- *"Démission d'au moins un membre du board avant juin 2026"*
- *"Annonce officielle d'un fonds activiste prenant >5% du capital"*
- *"Publication d'un avis du procureur ouvrant une enquête formelle"*

### Mauvais indicateurs

- *"Sensation générale de tension qui monte"* (non observable)
- *"Tout indice qui irait dans ce sens"* (tautologique)
- *"X commence à faire des choses bizarres"* (subjectif)

---

## Exemples annotés

### Exemple A — Prédiction excellente (enregistrable)

```yaml
id: PRED-2026-05-14-001
timestamp: 2026-05-14T16:42:00+02:00
skill_source: signaux-du-futur
domaine: économie / entreprises
sujet: "Restructuration entreprise X"
prediction: "X annoncera officiellement une cession majeure (>30% du capital) ou une fusion avec une autre cotée du CAC40 avant le 31 décembre 2026, vérifiable par un communiqué AMF."
probabilite: 0.65
horizon_jours: 230
indicateur_bascule:
  - "Approche connue d'un fonds activiste (rendu public) avant septembre"
  - "Démission ou révocation d'au moins un membre du board avant octobre"
  - "Audit externe annoncé par le commissaire aux comptes"
condition_refutation: "Au 31/12/2026, aucun communiqué AMF de cession/fusion publié"
hypotheses_concurrentes:
  - "Restructuration interne sans cession (P=0.20)"
  - "Aucune action majeure, statu quo (P=0.10)"
  - "Scandale ou enquête bloquant l'opération (P=0.05)"
base_rate_estimee: "12% des entreprises du CAC40 ont connu une cession/fusion majeure sur un horizon de 24 mois entre 2010-2024"
biais_surveilles: [confirmation, narrative_attractor]
sources:
  - "Reuters 12/05/2026 — démission CFO"
  - "Les Échos 14/05/2026 — analyse sectorielle"
statut: ouverte
```

**Pourquoi c'est bon** :
- Événement observable (communiqué AMF).
- Seuil net (>30%, ou fusion CAC40).
- Date limite précise.
- Indicateurs de bascule précis et observables.
- Hypothèses concurrentes formulées avec probabilités sommant à ~1.
- Base rate explicite.

### Exemple B — Prédiction non enregistrable (à reformuler)

```yaml
prediction: "X est en train de perdre le contrôle de la situation"
probabilite: 0.75
horizon_jours: 90
```

**Problèmes** :
- "Perdre le contrôle" : non observable, subjectif.
- Aucun seuil.
- Aucun indicateur de bascule.

**Reformulation proposée par l'agent** :

> *Pour rendre cette prédiction enregistrable, peux-tu préciser :*
> *(a) quel événement observable indiquerait la "perte de contrôle" — démission ? Conflit ouvert ? Décision invalidée ? Vote de défiance ?*
> *(b) quel seuil et à quelle date ?*
> *(c) quel indicateur intermédiaire pourrait te confirmer la trajectoire ?*

---

## Mode entraînement

Le skill peut être utilisé pour **entraîner la calibration personnelle** en dehors des dossiers réels.

Procédure :
1. L'utilisateur génère ou récupère un lot de **questions binaires à réponse vérifiable** (questions Tetlock, GJP, Metaculus, ou questions de culture générale).
2. Pour chacune, il formule sa probabilité avant de vérifier la réponse.
3. Le skill enregistre, puis score, puis produit un mini-rapport.
4. Au fil de séances répétées, l'utilisateur observe sa courbe de calibration s'améliorer.

Effet documenté (Tetlock & Mellers, GJP) : 10-20% d'amélioration du Brier score après 3-6 séances d'entraînement bien menées.

---

## Formats acceptés en entrée

L'utilisateur peut soumettre une prédiction à enregistrer sous diverses formes ; le skill normalise :

- **Texte libre** : *"je pense que X va arriver avant juin, avec environ 70% de chances"*
- **Sortie d'un autre skill** : sortie complète de *Signaux* ou *Miroir Trans-échelle*
- **Format pré-structuré** : YAML/markdown déjà formaté à corriger ou compléter

Dans tous les cas, le skill produit l'entrée finale au format canonique défini ci-dessus.
