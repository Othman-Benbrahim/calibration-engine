# Métriques de scoring — Brier, log loss, calibration plot

Ce fichier expose les **métriques propres de la science prédictive** utilisées par le Calibration Engine pour scorer rétrospectivement les prédictions. Toutes les métriques décrites sont des *proper scoring rules* (Gneiting & Raftery, 2007) — c'est-à-dire qu'elles incitent l'honnêteté probabiliste (annoncer sa vraie probabilité produit le meilleur score attendu).

---

## 1. Brier Score

### Définition

Inventé par Glenn Brier en 1950 pour la météorologie, le Brier score est la **métrique de référence** de la prédiction probabiliste binaire.

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
| 0.25 | Performance équivalente à toujours dire 0.5 (baseline sur événements équilibrés) |
| 0.5 | Pire performance possible : dire 1 quand outcome=0, ou 0 quand outcome=1 |

**Règle pratique** : un système qui produit un BS < 0.25 sur un échantillon suffisant *bat le hasard*. C'est le minimum à viser.

### Exemple

| Prédiction | Probabilité | Outcome | BS individuel |
|-----------|-------------|---------|---------------|
| P1 | 0.80 | 1 | (0.80 − 1)² = 0.04 |
| P2 | 0.80 | 0 | (0.80 − 0)² = 0.64 |
| P3 | 0.20 | 0 | (0.20 − 0)² = 0.04 |
| P4 | 0.50 | 1 | (0.50 − 1)² = 0.25 |

BS moyen = (0.04 + 0.64 + 0.04 + 0.25) / 4 = **0.2425**

→ légèrement meilleur que le hasard, mais peu impressionnant (l'échantillon est trop petit pour conclure).

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

Log naturel (ln). Convention : `log(0) = +∞`, donc une prédiction de 0 ou 1 qui se trompe produit un score infini — d'où l'**interdiction** des probabilités extrêmes (0 et 1) à l'enregistrement.

### Interprétation

| LL | Lecture |
|----|---------|
| 0 | Prédictions parfaites |
| 0.693 (= ln 2) | Performance équivalente à toujours dire 0.5 |
| +∞ | Catastrophe (proba 0 sur outcome=1, ou proba 1 sur outcome=0) |

### Différence avec Brier

Le log loss **pénalise plus sévèrement** les prédictions confiantes et fausses. Une prédiction de 0.95 qui se révèle fausse :
- Brier : (0.95 − 0)² = 0.9025
- Log loss : −log(0.05) = 2.996

Le log loss est utilisé quand on veut **fortement décourager la sur-confiance**. C'est la métrique standard en machine learning et en pari sportif.

### Quand utiliser quel score

- **Brier** : score intuitif, lisible, comparable. Métrique principale du Calibration Engine.
- **Log loss** : utilisé en complément pour identifier les sur-confiances catastrophiques.

Le rapport de calibration affiche les deux.

---

## 3. Décomposition de Murphy (1973)

Le Brier score se décompose en **trois composantes** instructives :

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

où l'on bin les prédictions par tranche de probabilité, `fₖ̄` étant la probabilité moyenne dans le bin k, `oₖ̄` la fréquence observée dans ce bin.

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

Maximum 0.25 quand `ō = 0.5` (événement balanced).

### Lecture combinée

Un bon système prédictif a :
- Reliability **faible** (bien calibré)
- Resolution **élevée** (discriminant)

Un système peut être **bien calibré et inutile** (toujours dire 0.5 ≈ reliability 0, resolution 0, sans valeur). C'est pourquoi il faut les deux.

---

## 4. Calibration Plot (Reliability Diagram)

### Construction

1. Trier toutes les prédictions par probabilité prédite.
2. Diviser en **10 bins** : [0.0–0.1], [0.1–0.2], …, [0.9–1.0].
3. Pour chaque bin :
   - Calculer la probabilité moyenne prédite (`f̄`)
   - Calculer la fréquence observée d'occurrence (`ō`)
4. Tracer `ō` en fonction de `f̄`.

### Lecture

- **Diagonale parfaite** : calibration idéale.
- **Courbe sous la diagonale** : sur-confiance (vous dites 0.8 mais ça arrive 0.6 fois).
- **Courbe au-dessus de la diagonale** : sous-confiance (vous dites 0.4 mais ça arrive 0.6 fois).
- **Cassures locales** : biais spécifiques à des plages de probabilité.

### Format textuel produit par le skill

```
Prob bin   | Obs freq | Cas    | Visualisation
─────────────────────────────────────────────────────
0.0-0.1    | 0.08     | n=4    | ▓░░░░░░░░░  bien calibré
0.1-0.2    | 0.15     | n=6    | ▓▓░░░░░░░░  bien calibré
0.2-0.3    | 0.32     | n=8    | ▓▓▓░░░░░░░  bien calibré
0.3-0.4    | 0.38     | n=5    | ▓▓▓▓░░░░░░  bien calibré
0.4-0.5    | 0.41     | n=3    | ▓▓▓▓░░░░░░  bien calibré
0.5-0.6    | 0.56     | n=7    | ▓▓▓▓▓▓░░░░  bien calibré
0.6-0.7    | 0.62     | n=9    | ▓▓▓▓▓▓░░░░  bien calibré
0.7-0.8    | 0.61     | n=8    | ▓▓▓▓▓▓░░░░  ⚠ sur-confiance modérée
0.8-0.9    | 0.66     | n=5    | ▓▓▓▓▓▓▓░░░  ⚠ sur-confiance forte
0.9-0.95   | 0.75     | n=4    | ▓▓▓▓▓▓▓▓░░  ⚠ sur-confiance sévère
```

### Taille minimale d'échantillon

Une calibration plot devient lisible à partir de **30-50 prédictions résolues**. En dessous, les bins sont trop peu peuplés pour conclure. Le rapport doit indiquer ce caveat explicitement.

---

## 5. Sharpness

### Définition

La sharpness mesure la **distance moyenne des probabilités prédites à 0.5**. Un système "lâche" (toutes prédictions ≈ 0.5) a une sharpness nulle. Un système "tranché" (prédictions ≈ 0 ou 1) a une sharpness élevée.

```
Sharpness = (1/N) × Σ (fᵢ − 0.5)²
```

### Pourquoi ça compte

Un système peut avoir un Brier faible **uniquement parce qu'il joue prudent** (dit toujours 0.5). C'est de la calibration triviale. La sharpness révèle si le système prend de vrais risques probabilistes.

La règle (Gneiting et al., 2007) :

> *Maximiser la sharpness, soumis à la contrainte de calibration.*

C'est-à-dire : être aussi tranché que possible, **sans** sacrifier la calibration.

---

## 6. Taux d'exactitude (accuracy)

### Définition

Sur les prédictions où probabilité > 0.5, le taux d'exactitude est la fraction qui se réalisent.

```
Accuracy = (TP + TN) / N
```

où TP = vrai positifs (proba > 0.5 ET outcome = 1), TN = vrai négatifs (proba < 0.5 ET outcome = 0).

### Limites

L'accuracy est une **métrique grossière** car elle ne tient pas compte de la probabilité :
- Une prédiction à 0.51 et une à 0.99 comptent pareil si elles sont vraies.

Le Brier et le log loss sont **strictement supérieurs**. L'accuracy est cependant utile pour communiquer un résultat à un public non-statisticien.

---

## 7. Comparaison à un baseline

Tout rapport doit comparer la performance à au moins **deux baselines** :

### Baseline 1 — Toujours dire le base rate

Brier minimal qu'on obtient en disant systématiquement le base rate observé sur l'échantillon. C'est le baseline "sans aucune info supplémentaire".

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

C'est l'indicateur le plus parlant pour communiquer la valeur ajoutée du système.

---

## 8. Multi-classes et événements catégoriels

Pour les prédictions qui ne sont pas binaires (ex : 4 scénarios avec leurs probabilités), on étend le Brier en multi-classe :

```
BS_multi = (1/N) × Σᵢ Σⱼ (fᵢⱼ − oᵢⱼ)²
```

où `j` indexe les classes (scénarios), avec `Σⱼ fᵢⱼ = 1` et `oᵢⱼ ∈ {0, 1}` (le scénario réalisé prend 1, les autres 0).

Le Calibration Engine accepte ce format pour les prédictions de *Signaux du Futur* qui produisent typiquement 3 scénarios (optimiste / probable / critique) avec probabilités.

---

## 9. Tableau récapitulatif

| Métrique | Plage | But | Quand l'utiliser |
|----------|-------|-----|------------------|
| Brier score | [0, 1] | Score général | Toujours |
| Log loss | [0, +∞] | Pénaliser sur-confiance | Toujours en complément |
| Reliability | [0, 0.25] | Calibration pure | Décomposition Brier |
| Resolution | [0, 0.25] | Discrimination | Décomposition Brier |
| Sharpness | [0, 0.25] | Audace probabiliste | Audit risque "trivialité" |
| Calibration plot | — | Diagnostic visuel | Au moins 30 prédictions |
| BSS | [-∞, 1] | Valeur vs baseline | Communication publique |
| Accuracy | [0, 1] | Vulgarisation | Communication non-technique |

---

## Notes pour l'agent

- Toujours afficher Brier et log loss ensemble.
- Toujours afficher le baseline 0.25 et le BSS pour situer la performance.
- Au-delà de 30 prédictions résolues, produire le calibration plot.
- En dessous de 30, indiquer : *"Échantillon insuffisant pour une calibration robuste — interpréter avec prudence."*
- En dessous de 10, ne produire qu'un score brut + warning fort.
