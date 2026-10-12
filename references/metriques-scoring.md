# Métriques de scoring — Brier, log loss, calibration plot

Ce fichier expose les métriques utilisées par le Calibration Engine pour scorer rétrospectivement les prédictions. Toutes sont calculées par `scripts/scoring.py`.

**Statut des métriques.** Seuls le **Brier score** et le **log loss** sont des *proper scoring rules* — plus précisément *strictly proper* : annoncer sa vraie probabilité minimise strictement la perte attendue (Gneiting & Raftery, 2007). Les autres éléments de ce fichier ne sont pas des règles de score : la **sharpness** est une propriété des prévisions (leur dispersion), l'**accuracy** une métrique de décision à seuil (non propre : elle ignore la valeur des probabilités), le **calibration plot** un diagnostic visuel, et la **décomposition de Murphy** une analyse du Brier.

---

## 1. Brier Score

### Définition

Proposé par Glenn Brier en 1950 pour la météorologie, le Brier score est la **métrique de référence** de la prédiction probabiliste binaire. (La formulation originale de Brier somme sur les deux catégories et varie de 0 à 2 ; la forme binaire ci-dessous, la plus courante, varie de 0 à 1.)

Pour une prédiction unique :

```
BS = (f − o)²
```

où :
- `f` = probabilité prédite ∈ [0, 1]
- `o` = outcome observé ∈ {0, 1}

Pour une série de N prédictions :

```
BS = (1/N) × Σ (fᵢ − oᵢ)²
```

### Interprétation

| BS | Lecture |
|----|---------|
| 0 | Prédictions parfaites (proba 1 quand outcome=1, proba 0 quand outcome=0) |
| 0.25 | Toujours dire 0.5 — **quel que soit** l'équilibre de l'échantillon, car (0.5 − o)² = 0.25 pour o = 0 comme pour o = 1 |
| 1 | Pire performance possible : dire 1 quand outcome = 0, ou 0 quand outcome = 1 |

**Règle pratique** : un BS < 0.25 sur un échantillon suffisant bat le « toujours 0.5 ». C'est un minimum, pas une preuve de compétence : sur un échantillon déséquilibré, il faut battre le baseline du taux de base ō(1 − ō) (voir §7).

### Exemple

| Prédiction | Probabilité | Outcome | BS individuel |
|-----------|-------------|---------|---------------|
| P1 | 0.80 | 1 | (0.80 − 1)² = 0.04 |
| P2 | 0.80 | 0 | (0.80 − 0)² = 0.64 |
| P3 | 0.20 | 0 | (0.20 − 0)² = 0.04 |
| P4 | 0.50 | 1 | (0.50 − 1)² = 0.25 |

BS moyen = (0.04 + 0.64 + 0.04 + 0.25) / 4 = **0.2425**

→ légèrement meilleur que « toujours 0.5 », mais l'échantillon est beaucoup trop petit pour conclure quoi que ce soit.

---

## 2. Log Loss (Logarithmic Score)

### Définition

```
LL = − [o × log(f) + (1−o) × log(1−f)]
```

Pour N prédictions :

```
LL = − (1/N) × Σ [oᵢ × log(fᵢ) + (1−oᵢ) × log(1−fᵢ)]
```

Logarithme naturel (ln), résultat en nats. Une prédiction de 0 ou 1 qui se trompe produit un score infini — d'où l'**interdiction** des valeurs 0 et 1 à l'enregistrement (plage admise : [0.01 ; 0.99]).

### Interprétation

| LL | Lecture |
|----|---------|
| 0 | Prédictions parfaites |
| 0.693 (= ln 2) | Performance équivalente à toujours dire 0.5 |
| +∞ | Catastrophe (proba 0 sur outcome=1, ou proba 1 sur outcome=0) |

### Différence avec Brier

Le log loss **pénalise plus sévèrement** les prédictions confiantes et fausses. Une prédiction de 0.95 qui se révèle fausse :
- Brier : (0.95 − 0)² = 0.9025
- Log loss : −ln(0.05) = 2.996

Le log loss est utilisé quand on veut **fortement décourager la sur-confiance**. C'est une métrique courante en apprentissage automatique.

### Quand utiliser quel score

- **Brier** : score intuitif, lisible, comparable. Métrique principale du Calibration Engine.
- **Log loss** : utilisé en complément pour identifier les sur-confiances catastrophiques.

Le rapport de calibration affiche les deux.

---

## 3. Décomposition de Murphy (1973)

Murphy (1973, *Journal of Applied Meteorology*, 12(4), 595-600) a montré que le Brier score se décompose en **trois composantes** instructives :

```
BS = Reliability − Resolution + Uncertainty
```

### Reliability (calibration)

Mesure à quel point les probabilités prédites correspondent aux fréquences observées.
- Reliability ≈ 0 : très bonne calibration
- Reliability élevée : sur-confiance ou sous-confiance systématiques

```
Reliability = (1/N) × Σₖ nₖ × (fₖ̄ − oₖ̄)²
```

où l'on regroupe les prédictions en groupes k, `fₖ̄` étant la probabilité moyenne du groupe k et `oₖ̄` la fréquence observée dans ce groupe.

**Exactitude de l'identité.** BS = REL − RES + UNC est **exacte** quand les groupes correspondent aux valeurs de prévision distinctes. Avec des bins de largeur fixe (ex. 0.1), les prévisions d'un même bin diffèrent, et un terme résiduel intra-bin apparaît. `scripts/scoring.py` fournit les deux versions (`murphy_exact`, `murphy_bins`) et affiche le résidu.

### Resolution (discrimination)

Mesure la capacité à distinguer les cas qui arrivent de ceux qui n'arrivent pas.
- Resolution élevée : bonne discrimination
- Resolution ≈ 0 : prédictions toutes proches du base rate

```
Resolution = (1/N) × Σₖ nₖ × (oₖ̄ − ō)²
```

où `ō` est la fréquence globale d'occurrence sur tout l'échantillon.

### Uncertainty

Variance intrinsèque de l'événement, hors de contrôle du prédicteur.

```
Uncertainty = ō × (1 − ō)
```

Maximum 0.25 quand `ō = 0.5`.

### Lecture combinée

Un bon système prédictif a :
- Reliability **faible** (bien calibré)
- Resolution **élevée** (discriminant)

Un système peut être **bien calibré et inutile** : dire systématiquement le taux de base ō donne reliability 0 et resolution 0. (Dire toujours 0.5 n'est bien calibré que si ō ≈ 0.5 : sa reliability vaut (0.5 − ō)².) C'est pourquoi il faut les deux.

---

## 4. Calibration Plot (Reliability Diagram)

### Construction

1. Trier toutes les prédictions par probabilité prédite.
2. Diviser en **10 bins de largeur 0.1** : [0.0 ; 0.1), [0.1 ; 0.2), …, [0.9 ; 1.0]. Le dernier bin inclut 1.0 ; chaque prédiction tombe dans exactement un bin.
3. Pour chaque bin :
   - Calculer la probabilité moyenne prédite (`f̄`)
   - Calculer la fréquence observée d'occurrence (`ō`)
4. Tracer `ō` en fonction de `f̄`.

### Lecture

- **Diagonale parfaite** : calibration idéale.
- **Sur-confiance** = prévisions **trop extrêmes** : la fréquence observée est plus proche de 0.5 que la probabilité annoncée. La courbe est **sous** la diagonale pour p > 0.5 (vous dites 0.8, ça arrive 0.6 fois) et **au-dessus** pour p < 0.5 (vous dites 0.2, ça arrive 0.35 fois). Elle est donc plus plate que la diagonale.
- **Sous-confiance** = prévisions **pas assez tranchées** : la fréquence observée est plus loin de 0.5 que la probabilité annoncée (vous dites 0.8, ça arrive 0.95 fois ; vous dites 0.2, ça arrive 0.05 fois). Courbe plus pentue que la diagonale.
- **Biais directionnel** : courbe entièrement au-dessus (vous sous-estimez systématiquement la fréquence des événements) ou entièrement en dessous (vous la surestimez).
- **Cassures locales** : biais spécifiques à des plages de probabilité.

### Format textuel produit par le skill

Le tableau est produit par `scripts/scoring.py report` (champ `calibration`). Lecture automatique : « cohérent » si |obs − p moy.| ≤ 0.10 ; « effectif trop faible » si n < 5 ; sinon sur-confiance ou sous-confiance selon le sens défini ci-dessus.

```
Bin          | p moy. | obs.  | n | lecture
[0.0, 0.1)   | 0.05   | 0.00  | 4 | effectif trop faible
[0.1, 0.2)   | 0.15   | 0.20  | 5 | cohérent
…
[0.7, 0.8)   | 0.75   | 0.60  | 5 | sur-confiance (prévisions trop extrêmes)
[0.8, 0.9)   | 0.85   | 0.75  | 4 | effectif trop faible
[0.9, 1.0]   | 0.92   | 0.67  | 3 | effectif trop faible
```

(Extrait du rapport d'exemple calculé sur `tests/fixtures/exemple-rapport.json`, données fictives.)

### Taille minimale d'échantillon

Un calibration plot devient lisible à partir de **30-50 prédictions résolues** (ordre de grandeur pratique, pas un seuil statistique). En dessous, les bins sont trop peu peuplés pour conclure. Le rapport doit indiquer ce caveat explicitement.

---

## 5. Sharpness

### Définition

Pour des prévisions binaires, on mesure ici la sharpness par l'**écart quadratique moyen des probabilités prédites à 0.5** (une mesure simple parmi d'autres ; chez Gneiting et al., la sharpness désigne plus généralement la concentration des distributions prédictives). Un système "lâche" (toutes prédictions ≈ 0.5) a une sharpness nulle. Un système "tranché" (prédictions ≈ 0 ou 1) a une sharpness élevée.

```
Sharpness = (1/N) × Σ (fᵢ − 0.5)²
```

### Pourquoi ça compte

Un système qui « joue prudent » (probabilités toujours proches de 0.5 ou du taux de base) peut être bien calibré sans rien apporter. C'est de la calibration triviale. La sharpness révèle si le système prend de vrais risques probabilistes.

Le principe formulé par Gneiting, Balabdaoui & Raftery (2007, *Journal of the Royal Statistical Society B*, 69(2), 243-268) :

> *Maximiser la sharpness des distributions prédictives, sous contrainte de calibration.*

C'est-à-dire : être aussi tranché que possible, **sans** sacrifier la calibration.

---

## 6. Taux d'exactitude (accuracy)

### Définition

L'accuracy est la part des prédictions « du bon côté » de 0.5 :

```
Accuracy = (TP + TN) / N'
```

où TP = vrais positifs (p > 0.5 ET outcome = 1), TN = vrais négatifs (p < 0.5 ET outcome = 0), et N' le nombre de prédictions avec p ≠ 0.5. Les prédictions à exactement 0.5 n'expriment aucun pari : elles sont exclues et leur nombre est affiché.

### Limites

L'accuracy est une **métrique grossière** car elle ne tient pas compte de la probabilité :
- Une prédiction à 0.51 et une à 0.99 comptent pareil si elles sont vraies.

L'accuracy n'est pas une règle de score propre : on peut l'améliorer en déclarant des probabilités plus tranchées que sa croyance réelle. Le Brier et le log loss sont donc à privilégier pour évaluer ; l'accuracy ne sert qu'à communiquer un résultat à un public non statisticien, toujours accompagnée du Brier.

---

## 7. Comparaison à un baseline

Tout rapport doit comparer la performance à au moins **deux baselines** :

### Baseline 1 — Toujours dire le base rate

Brier obtenu en disant systématiquement le taux de base observé ō sur l'échantillon (référence dite « climatologique »). C'est le baseline « sans aucune information spécifique au cas ». Il vaut au plus 0.25 et est d'autant plus bas que l'échantillon est déséquilibré.

```
BS_baseline = ō × (1 − ō)
```

### Baseline 2 — Toujours dire 0.5

Brier qu'on obtient en disant systématiquement 0.5.

```
BS_05 = 0.25 (toujours, par construction)
```

### Indicateur composite : Brier Skill Score

```
BSS = 1 − (BS / BS_baseline)
```

- BSS = 1 → prédiction parfaite
- BSS = 0 → équivalent au baseline
- BSS < 0 → **pire que le baseline** (vous nuisez à l'information)

Le BSS n'est pas défini si ō vaut 0 ou 1 (baseline nul). Toujours préciser le baseline utilisé : « BSS vs 0.5 » et « BSS vs taux de base » diffèrent. C'est l'indicateur le plus parlant pour communiquer la valeur ajoutée du système.

---

## 8. Multi-classes et événements catégoriels

Pour les prédictions qui ne sont pas binaires (ex : 4 scénarios avec leurs probabilités), on étend le Brier en multi-classe :

```
BS_multi = (1/N) × Σᵢ Σⱼ (fᵢⱼ − oᵢⱼ)²
```

où `j` indexe les classes (scénarios), avec `Σⱼ fᵢⱼ = 1` et `oᵢⱼ ∈ {0, 1}` (le scénario réalisé prend 1, les autres 0). Ce score varie de 0 à **2** : il n'est pas directement comparable au Brier binaire (pour deux classes, il en vaut exactement le double).

Le Calibration Engine accepte ce format pour les ensembles de scénarios MECE produits par `superforecasting-protocol` ou *Signaux du Futur* (`scripts/scoring.py multiclass`).

---

## 9. Tableau récapitulatif

| Métrique | Plage | Statut | But | Quand l'utiliser |
|----------|-------|--------|-----|------------------|
| Brier score (binaire) | [0, 1] | Règle de score strictement propre | Score général | Toujours |
| Brier multi-classes | [0, 2] | Règle de score strictement propre | Scénarios MECE | Prédictions multi-classes |
| Log loss | [0, +∞] | Règle de score strictement propre | Pénaliser la sur-confiance | Toujours en complément |
| Reliability | [0, 1] | Composante du Brier | Calibration | Décomposition |
| Resolution | [0, 0.25] | Composante du Brier | Discrimination | Décomposition |
| Uncertainty | [0, 0.25] | Composante du Brier | Difficulté intrinsèque | Décomposition |
| Sharpness (écart² à 0.5) | [0, 0.25] | Propriété des prévisions | Audace probabiliste | Audit du risque de « trivialité » |
| Calibration plot | — | Diagnostic visuel | Calibration par plage | Au moins 30 prédictions |
| BSS | ]−∞, 1] | Score relatif | Valeur vs baseline | Communication |
| Accuracy | [0, 1] | Métrique de décision, non propre | Vulgarisation | Communication non technique |

---

## Notes pour l'agent

- Toujours afficher Brier et log loss ensemble.
- Toujours afficher les deux baselines (0.25 et ō(1 − ō)) et les BSS correspondants.
- Ne jamais calculer un agrégat de tête : `scripts/scoring.py report`.
- À partir de 30 prédictions résolues, produire le calibration plot.
- En dessous de 30, indiquer : *"Échantillon insuffisant pour une calibration robuste — interpréter avec prudence."*
- En dessous de 10, ne produire qu'un score brut + warning fort.
