# Interopérabilité avec les autres skills

Ce fichier décrit comment le Calibration Engine se connecte aux autres skills de l'écosystème pour **extraire les prédictions loggables**, les enregistrer et les scorer ultérieurement.

**Périmètre.** Les skills du cluster prédictif (`superforecasting-protocol`, `bayesian-updater`, `prediction-engine`) sont livrés avec celui-ci. *Signaux du Futur*, *Miroir Trans-échelle*, *Hacking Narratif*, *Fractales du Destin*, *Métalangage des Résonances* et *Miroir des Paradigmes* sont des skills **externes** de l'écosystème IRIS∞, non inclus dans ces dépôts : les règles ci-dessous s'appliquent à leurs sorties lorsqu'ils sont installés.

---

## Architecture générale

Le Calibration Engine est un **observateur**. Il ne perturbe pas les pipelines des autres skills ; il les "lit" à la sortie et extrait ce qui est falsifiable.

```
┌──────────────────────────┐     sortie      ┌─────────────────────────┐
│  superforecasting-proto. │ ──────────────► │                         │
│  signaux-du-futur        │ ──────────────► │                         │
│  miroir-trans-echelle    │                 │   CALIBRATION ENGINE    │
│  hacking-narratif        │ ──────────────► │   (observateur)         │
│  autre skill             │                 │                         │
└──────────────────────────┘                 └────────────┬────────────┘
                                                          │
                                                          ▼
                                              calibration-log.md
                                              (mémoire externe)
```

Deux modes d'activation :

1. **Mode actif** : l'utilisateur colle la sortie d'un skill et demande d'en extraire les prédictions loggables.
2. **Mode passif** : l'agent détecte dans la sortie d'un skill des marqueurs de prédiction (probabilité explicite, horizon temporel, indicateur de bascule) et propose automatiquement un enregistrement.

---

## Wrapping de `superforecasting-protocol`

La fiche de prédiction de `superforecasting-protocol` contient déjà un bloc « Métadonnées pour Calibration Engine » au format du log (identifiant `PRED-AAAA-MM-JJ-NNN`, échéance, domaine, statut). Procédure :

1. Pour une question binaire : une entrée, `probabilite` = probabilité du « oui ».
2. Pour un ensemble de scénarios MECE : une entrée `type: multi-classes` (format ci-dessous), scorée avec le Brier multi-classes.
3. Reprendre les indicateurs précoces comme `indicateur_bascule` et les anti-indicateurs comme éléments de `condition_refutation`.

---

## Wrapping de `signaux-du-futur` *(externe)*

### Ce qui est directement loggable

*Signaux du Futur* produit par construction des éléments qui correspondent au protocole d'enregistrement :

| Élément dans Signaux | Mapping dans le log |
|---------------------|---------------------|
| Question d'incertitude | → `sujet` |
| Hypothèse Hx (ex : "H1 — effondrement institutionnel") | → `prediction` |
| Probabilité formulée ou implicite | → `probabilite` |
| Indicateur de bascule | → `indicateur_bascule` |
| Scénario optimiste / probable / critique | → prédictions multi-classes |

### Procédure d'extraction

1. Identifier les **3 hypothèses concurrentes** dans la sortie.
2. Pour chacune : vérifier la falsifiabilité (test du sceptique).
3. Récupérer les probabilités. Si elles ne sont pas explicitées, demander à l'utilisateur de les chiffrer avant enregistrement.
4. Créer une entrée par hypothèse **ou** une entrée multi-classes avec les 3 hypothèses.

### Format multi-classes recommandé pour Signaux

```yaml
id: PRED-2026-05-14-007
skill_source: signaux-du-futur
type: multi-classes
prediction_centrale: "Quelle sera la trajectoire du dossier X dans les 9 mois ?"
classes:
  - label: "H1 — Cession/fusion majeure"
    prediction: "Annonce officielle de cession ou fusion avant 31/12/2026"
    probabilite: 0.60
  - label: "H2 — Restructuration interne"
    prediction: "Réorganisation sans cession, confirmée par communiqué officiel"
    probabilite: 0.25
  - label: "H3 — Scandale/blocage"
    prediction: "Enquête publique ou contentieux majeur rendant toute opération impossible"
    probabilite: 0.15
# Vérification : 0.60 + 0.25 + 0.15 = 1.00 ✓
indicateur_bascule:
  - "Démission d'un directeur financier avant septembre"
  - "Annonce d'un investisseur activiste"
horizon_jours: 230
```

### Règle de somme

Pour les prédictions multi-classes, les probabilités doivent sommer à 1.00 (±0.01 pour les arrondis). Si elles ne le font pas, demander ajustement avant enregistrement.

---

## Wrapping de `miroir-trans-echelle` *(externe)*

### Ce qui est loggable et ce qui ne l'est pas

*Miroir Trans-échelle* produit trois types de contenu, avec des statuts très différents :

| Contenu | Loggable ? | Pourquoi |
|---------|-----------|---------|
| Archétypes actifs (P1) | ❌ Non | Non falsifiable |
| Phrase symbolique FdD (P1) | ❌ Non | Non falsifiable |
| Signaux faibles (P2) | ❌ Non directement | Ce sont des observations, pas des prédictions |
| Hypothèses concurrentes (P2) | ✅ Oui | Même logique que Signaux |
| Scénarios P2 | ✅ Oui | Si probabilisés |
| Convergences fortes (P3) | ⚠️ Conditionnel | Si l'utilisateur en tire une prédiction explicite |
| Dissonances (P3) | ⚠️ Conditionnel | Idem |
| Recommandations (P3) | ✅ Si probabilisées | "Hypothèse prioritaire avec proba X" |

### Extraction des convergences fortes

Quand la P3 identifie une convergence forte et en tire une recommandation (ex : *"verrouillé sur deux axes — hypothèse H1 prioritaire"*), le Calibration Engine peut logger :

```yaml
id: PRED-2026-05-14-010
skill_source: miroir-trans-echelle
prediction: "H1 (cession/fusion) se réalisera avant 31/12/2026 — convergence P1+P2"
probabilite: 0.65   # ← L'utilisateur doit confirmer ce chiffre
# NOTE : base OSINT (Signaux seul) = 0.55 ; la convergence P1+P2 ne peut
# ajouter plus de +0.10 (règle du narrative attractor) → plafond 0.65
indicateur_bascule: [...]
metadata:
  biais_surveilles: [narrative_attractor]
  note: "Intuition initiale 0.70, ramenée à 0.65 (−0.05) en application
         du plafond narrative attractor (base OSINT 0.55 + 0.10)"
```

### La règle du cap narrative attractor

Toute prédiction issue de *Miroir Trans-échelle* qui bénéficie d'une "convergence forte" P1+P2 doit appliquer un **cap automatique** :

- La convergence symbolique ne peut augmenter la probabilité OSINT de base de **plus de +0.10**, quel que soit le niveau de départ.
- Exemple : si Signaux seul aurait donné 0.55, Miroir peut aller à 0.65 au maximum.
- Si l'intuition est d'aller plus haut, le plafond s'applique quand même ; le champ `metadata.note` documente l'écart entre l'intuition et la valeur retenue.
- Si la hausse passe par une mise à jour bayésienne, elle doit respecter BF ≤ 1.49 (voir `bayesian-updater/references/interop-skills.md` §2, où l'ancienne borne BF ≈ 1.5–2.0 a été corrigée car elle autorisait jusqu'à +0.16).

---

## Wrapping de `hacking-narratif` *(externe)*

*Hacking Narratif* produit rarement des prédictions probabilistes formelles. Il est concerné uniquement dans son **Mode B (stratégique)** quand il formule des prédictions sur des narratifs collectifs.

### Ce qui est loggable

- Mode B, si l'analyse débouche sur une prédiction de type : *"Ce récit va se dégrader dans les X semaines."*
- Formulation possible : *"Le cadrage actuel de X va être remplacé par un cadrage Y avant [date], visible dans les titres de presse dominante."*

### Procédure

Même logique que Signaux. L'indicateur de bascule doit être observable dans la presse ou les réseaux sociaux.

---

## Wrapping de `fractales-du-destin` *(externe)*

### Le cas particulier du symbolique pur

Les sorties de *Fractales du Destin* sont structurellement non-falsifiables : un archétype actif, une Phrase FdD, un motif récurrent — aucun de ces éléments ne peut être *directement* vrai ou faux au sens empirique.

**Le Calibration Engine n'enregistre jamais directement une lecture Fractales.**

### La voie indirecte : prédiction dérivée

Si l'utilisateur dit : *"Ce tirage m'indique que l'archétype du Passeur est actif, ce qui me fait penser que X va se terminer dans les 3 mois"* — alors **la prédiction dérivée** (*X va se terminer dans les 3 mois*) est loggable, à condition d'être falsifiable.

Format d'enregistrement :

```yaml
skill_source: fractales-du-destin
note_methodologique: "Prédiction dérivée d'une lecture symbolique — non issue
  directement de l'archétype mais d'une inférence de l'utilisateur. Biais
  narrative attractor à surveiller particulièrement."
probabilite: [à fixer par l'utilisateur après dépouillement symbolique]
```

### Règle d'humilité pour les prédictions dérivées de Fractales

Les prédictions dérivées de Fractales *seules* (sans confirmation OSINT) portent une probabilité inférieure à 0.65 (convention de prudence du skill, à réviser au vu du log) et notent dans les `biais_surveilles` : `narrative_attractor`.

Elles peuvent néanmoins être précieuses pour détecter si la lecture symbolique a une valeur prédictive résiduelle — une fois le log suffisamment riche, comparer Brier de "Fractales seul" vs "Signaux seul" vs "Miroir" est très instructif.

---

## Invocation formelle entre sessions

Le Calibration Engine travaille toujours **sur le `calibration-log.md` fourni en contexte**, qui fait foi même si l'environnement dispose d'une mémoire. Protocole recommandé en début de session :

1. L'utilisateur fournit `calibration-log.md` en contexte.
2. L'utilisateur indique le mode souhaité : enregistrement / scoring / rapport.
3. L'agent travaille sur le fichier et produit les mises à jour à copier.

Pour les sessions où plusieurs skills sont utilisés conjointement, l'utilisateur peut activer le Calibration Engine "en arrière-plan" avec l'instruction :

> *"Active Calibration Engine en mode passif : propose-moi d'enregistrer chaque prédiction probabilisée produite par un autre skill au fil de la session."*

---

## Tableau de compatibilité

| Skill | Loggable directement | Via dérivation | Notes |
|-------|---------------------|----------------|-------|
| `superforecasting-protocol` | ✅ Oui | — | Fiche déjà au format du log |
| `bayesian-updater` | Révisions uniquement | — | Champ `revisions` des entrées existantes |
| `signaux-du-futur` *(externe)* | ✅ Oui | — | Skill amont le mieux aligné |
| `miroir-trans-echelle` *(externe)* | ✅ Hypothèses P2 | ✅ Convergences P3 | Plafond narrative attractor (+0.10) |
| `hacking-narratif` *(externe)* | ✅ Mode B seulement | — | Mode A non loggable |
| `fractales-du-destin` *(externe)* | ❌ Non | ✅ Dérivations | Humilité + biais notés |
| `metalangage-resonances` *(externe)* | ❌ Non | Rarement | Non prédictif par nature |
| `miroir-des-paradigmes` *(externe)* | ❌ Non | ❌ Non | Usage personnel, hors périmètre |
