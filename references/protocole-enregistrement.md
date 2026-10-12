# Protocole d'enregistrement — Comment logger une prédiction

Ce fichier définit la **discipline d'enregistrement** d'une prédiction dans le Calibration Engine. Il décrit les champs obligatoires, les règles de falsifiabilité, la validation préalable, et donne des exemples annotés (bons et mauvais).

---

## Pourquoi un protocole strict

Sans discipline d'enregistrement, le log devient un ramassis d'affirmations vagues qu'on peut, après coup, réinterpréter dans n'importe quel sens. C'est exactement ce que la calibration cherche à empêcher.

Le protocole impose donc trois exigences non-négociables, et c'est leur stricte application qui fait la valeur du log :

1. **Falsifiabilité préalable** — l'événement prédit doit être *observable* à l'horizon fixé.
2. **Probabilité explicite** — dans [0.01 ; 0.99] (pas de certitude) ; hors de [0.05 ; 0.95], justification obligatoire.
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
| `probabilite` | float [0.01–0.99] | Probabilité explicite de réalisation |
| `justification_extreme` | string | **Obligatoire si** `probabilite` < 0.05 ou > 0.95 : taux de base et raisons de cette quasi-certitude |
| `horizon_jours` | integer | Délai en jours entre l'enregistrement et l'échéance |
| `date_echeance` | date ISO | Date à laquelle la prédiction est résolue (ou passe à `expirée` faute de résolution claire) |
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

Une prédiction est **enregistrable** si et seulement si elle satisfait les **trois conditions opérationnelles** ci-dessous. Elles s'inspirent du critère de falsifiabilité de Popper (un énoncé scientifique doit pouvoir être réfuté par l'observation) ; leur formulation en trois critères est propre à ce skill.

### Condition 1 — Événement observable

L'énoncé doit décrire un événement vérifiable par observation publique, pas un état interne ou une "tendance générale".

❌ *"X va devenir plus puissant"* → non observable directement
✅ *"X obtiendra plus de 51% des voix au scrutin du 14 juin 2026"*

❌ *"L'inflation reste préoccupante"* → non observable
✅ *"L'inflation en glissement annuel (IPC, INSEE) sera > 4 % sur l'indice de septembre 2026"*

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
- Abandonner l'enregistrement et noter l'énoncé dans `notes-non-falsifiables.md` (gabarit fourni dans `references/notes-non-falsifiables.md`, à copier à côté du `calibration-log.md`).

---

## Règles de probabilité

### Plage admise : 0.01 à 0.99

Les valeurs 0 et 1 sont **interdites** : elles signifient « certitude », et une erreur à 0 ou 1 produit un log loss infini.

Entre 0.01 et 0.05, et entre 0.95 et 0.99, la valeur est admise mais exige un champ `justification_extreme` : taux de base explicite et raisons spécifiques de la quasi-certitude. C'est la zone où la sur-confiance coûte le plus cher : une prédiction à 0.95 qui échoue coûte 0.9025 en Brier et 3.0 en log loss ; à 0.99, 0.98 en Brier et 4.6 en log loss.

L'utilisateur qui dit *« je suis sûr à 100 % »* est invité à choisir une valeur dans la plage admise et à justifier la quasi-certitude.

*Harmonisation v1.1* : la version 1.0 imposait [0.05 ; 0.95], ce qui rendait impossible l'enregistrement des probabilités basses légitimement produites par `superforecasting-protocol` (taux de base de quelques pour cent). La plage commune de l'écosystème est désormais [0.01 ; 0.99].

### Pas d'arrondi excessif

Préférer `0.65` à `0.7` quand c'est ce que l'analyse suggère. Dans les données du Good Judgment Project, arrondir les prévisions à des catégories plus grossières dégrade systématiquement leur précision (Friedman et al., 2018) : la granularité porte de l'information.

À l'inverse, une précision à la décimale près (`0.642`) n'apporte rien si rien dans l'analyse ne la justifie. Préférer `0.64` ou `0.65`.

### Tenir compte de la base rate

Tetlock insiste (commandement 3, équilibre vue intérieure / vue extérieure) : avant de probabiliser, demander *« à quelle fréquence ce type d'événement se produit-il historiquement ? »*. Ce **taux de base** est le point de départ naturel. La probabilité personnelle s'éloigne du base rate dans la mesure où on a des raisons spécifiques de penser que ce cas est différent.

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
horizon_jours: 231
date_echeance: 2026-12-31
indicateur_bascule:
  - "Approche connue d'un fonds activiste (rendu public) avant septembre"
  - "Démission ou révocation d'au moins un membre du board avant octobre"
  - "Audit externe annoncé par le commissaire aux comptes"
condition_refutation: "Au 31/12/2026, aucun communiqué AMF de cession/fusion publié"
hypotheses_concurrentes:
  - "Restructuration interne sans cession (P=0.20)"
  - "Aucune action majeure, statu quo (P=0.10)"
  - "Scandale ou enquête bloquant l'opération (P=0.05)"
base_rate_estimee: "[FICTIF — exemple de format] X % des entreprises du CAC40 ont connu une cession/fusion majeure sur un horizon de 24 mois, période AAAA-AAAA, source : [à documenter]"
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
- Hypothèses concurrentes formulées, probabilités sommant à 1.00 (0.65 + 0.20 + 0.10 + 0.05).
- Taux de base explicite **et sourcé** (le chiffre doit venir d'une source vérifiable, pas d'une estimation de mémoire).
- *Point de vigilance* : passer d'un taux de base de l'ordre de 10 % à 0.65 est un écart considérable ; il doit être justifié par des facteurs spécifiques explicites (voir `detection-biais.md` §4).

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

Effet documenté : dans le Good Judgment Project, un module d'entraînement au raisonnement probabiliste de moins d'une heure a amélioré le Brier de 6 à 11 % par rapport au groupe contrôle (Chang, Chen, Mellers & Tetlock, 2016). La pratique répétée avec retour d'information compte aussi, mais aucune étude citée ici ne chiffre l'effet d'un nombre donné de séances. (La version 1.0 annonçait « 10-20 % après 3-6 séances », formulation sans source.)

---

## Formats acceptés en entrée

L'utilisateur peut soumettre une prédiction à enregistrer sous diverses formes ; le skill normalise :

- **Texte libre** : *"je pense que X va arriver avant juin, avec environ 70% de chances"*
- **Sortie d'un autre skill** : sortie complète de *Signaux* ou *Miroir Trans-échelle*
- **Format pré-structuré** : YAML/markdown déjà formaté à corriger ou compléter

Dans tous les cas, le skill produit l'entrée finale au format canonique défini ci-dessus.

---

## Références

- Chang, W., Chen, E., Mellers, B., & Tetlock, P. (2016). Developing expert political judgment. *Judgment and Decision Making*, 11(5), 509-526.
- Friedman, J. A., Baker, J. D., Mellers, B. A., Tetlock, P. E., & Zeckhauser, R. (2018). The value of precision in probability assessment: Evidence from a large-scale geopolitical forecasting tournament. *International Studies Quarterly*, 62(2), 410-422.
- Popper, K. (1959). *The Logic of Scientific Discovery*. Hutchinson.
