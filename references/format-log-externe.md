# Format du log externe — calibration-log.md

Ce fichier définit la structure complète du fichier `calibration-log.md` que l'utilisateur maintient lui-même. C'est la **référence auditable** entre sessions : même si l'environnement offre une mémoire, seul le log garantit un historique complet, daté et non modifiable a posteriori.

---

## Principes du log

1. **Un fichier unique** par utilisateur (ou par projet si plusieurs écosystèmes distincts).
2. **Append-only** par convention : on ajoute des entrées, on ne modifie pas les prédictions passées.
3. **Exception à l'append-only** : les champs `statut`, `date_resolution`, `outcome`, `brier_individuel`, `log_loss_individuel` sont mis à jour quand l'événement se résout.
4. **Format markdown + YAML** : markdown pour la lisibilité humaine, blocs YAML pour la parseabilité par l'agent.

---

## Structure globale du fichier

```markdown
# Calibration Log — IRIS∞ / [Nom du projet]

## Métadonnées
- Créé le : YYYY-MM-DD
- Propriétaire : [prénom ou pseudonyme]
- Dernier scoring : YYYY-MM-DD
- Prédictions totales : N
- Prédictions résolues : M
- Prédictions ouvertes : N-M
- Brier score global (résolu) : X.XXX
- Log loss global (résolu) : X.XXX

---

## Index des entrées

| ID | Date | Sujet | Proba | Horizon | Skill | Statut |
|----|------|-------|-------|---------|-------|--------|
| PRED-2026-05-14-001 | 2026-05-14 | Fusion X | 0.65 | 231j | signaux | ouverte |
| PRED-2026-04-02-001 | 2026-04-02 | Élection Y | 0.55 | 60j  | miroir  | résolue |
...

---

## Prédictions ouvertes

[Liste des entrées YAML avec statut = ouverte]

---

## Prédictions résolues

[Liste des entrées YAML avec statut = résolue + outcome + scores]

---

## Prédictions expirées ou non-évaluables

[Entrées dont l'horizon est dépassé sans résolution claire,
 ou non-falsifiables en retrospective]

---

## Agrégats par catégorie

[Produit par le skill lors du rapport — à mettre à jour manuellement
 ou copier depuis la sortie du rapport]

---

## Notes et observations

[Notes libres de l'utilisateur sur les patterns observés,
 les biais détectés, les ajustements de pratique]
```

---

## Structure d'une entrée ouverte

```yaml
---
id: PRED-2026-05-14-001
timestamp: 2026-05-14T16:42:00+02:00
skill_source: signaux-du-futur
domaine: économie / entreprises
sujet: "Restructuration entreprise X"
prediction: >
  X annoncera officiellement une cession majeure (>30% du capital) ou une fusion
  avec une autre cotée avant le 31 décembre 2026, vérifiable par un communiqué AMF.
probabilite: 0.65
horizon_jours: 231
date_echeance: 2026-12-31
indicateur_bascule:
  - "Approche connue d'un fonds activiste (rendu public) avant septembre"
  - "Démission ou révocation d'au moins un membre du board avant octobre"
condition_refutation: >
  Au 31/12/2026, aucun communiqué AMF de cession ou fusion publié.
hypotheses_concurrentes:
  - label: "Restructuration interne uniquement"
    probabilite: 0.20
  - label: "Aucune action majeure, statu quo"
    probabilite: 0.10
  - label: "Scandale ou enquête bloquant l'opération"
    probabilite: 0.05
base_rate_estimee: >
  [FICTIF — exemple de format] X % des entreprises du CAC40 ont connu
  cession/fusion sur horizon 24 mois, AAAA-AAAA. Source : [à documenter].
justification_extreme: null   # requis seulement si probabilite < 0.05 ou > 0.95
biais_surveilles:
  - confirmation
  - narrative_attractor
sources:
  - "Reuters 12/05/2026 — démission CFO"
  - "Les Échos 14/05/2026 — analyse sectorielle"
confiance_metacognitive: moyenne
comment_changer_avis: >
  Si aucun indicateur de bascule ne s'est déclenché à fin octobre,
  réviser la proba vers 0.40. Si le board est stable et aucun activiste
  ne s'est manifesté, réviser vers 0.30. (Révisions à calculer avec
  bayesian-updater le moment venu.)
statut: ouverte
revisions: []
---
```

---

## Structure d'une entrée avec révisions en cours

Le champ `revisions` permet de tracer les mises à jour bayésiennes :

```yaml
revisions:
  - date: 2026-07-15
    probabilite_avant: 0.65
    probabilite_apres: 0.75
    motif: >
      Démission confirmée du directeur financier le 12/07/2026.
      Indicateur de bascule 1 atteint — révision à la hausse.
    source: "Financial Times 12/07/2026"
    methode: intuitive          # ou bayesienne_formelle (voir bayesian-updater)
  - date: 2026-09-01
    probabilite_avant: 0.75
    probabilite_apres: 0.80
    motif: >
      Rumeurs de rachat par fonds P mentionnées par Reuters.
      Non confirmé — prudence maintenue.
    source: "Reuters 31/08/2026"
    methode: intuitive
```

Règle : une révision est toujours **antérieure** à la date de résolution de la prédiction. Les révisions marquées `methode: intuitive` peuvent être auditées a posteriori par `bayesian-updater` (Mode 3 ; l'exemple de ce mode porte sur les deux révisions ci-dessus).

---

## Structure d'une entrée résolue

```yaml
---
id: PRED-2026-04-02-001
timestamp: 2026-04-02T11:00:00+02:00
skill_source: miroir-trans-echelle
domaine: géopolitique
sujet: "Élection régionale Pays Y"
prediction: >
  Le parti A obtiendra plus de 45% des voix à l'élection régionale
  du 31 mai 2026, selon les résultats officiels.
probabilite: 0.55
horizon_jours: 59
date_echeance: 2026-05-31
indicateur_bascule:
  - "Sondage ≥ 43% dans les 10 jours précédant le scrutin"
condition_refutation: "Résultat officiel ≤ 45% au 31 mai 2026"
biais_surveilles: [narrative_attractor]
sources:
  - "Rapport Miroir Trans-échelle session 02/04/2026"
statut: résolue
# ─── RÉSOLUTION ───
date_resolution: 2026-05-31
outcome: 0   # Parti A obtenu 43.2% — prédiction non réalisée
source_resolution: "Résultats officiels min. Intérieur 31/05/2026"
brier_individuel: 0.3025   # (0.55 − 0)²
log_loss_individuel: 0.799  # −log(1 − 0.55)
verdict: "Événement non réalisé ; probabilité annoncée 0.55 (score individuel, pas un diagnostic de calibration)"
lecon: >
  Hypothèse de l'utilisateur : le narrative attractor a pu jouer (la
  convergence P1+P2 dans Miroir a renforcé la confiance sans base factuelle
  supplémentaire). Une prédiction isolée ne permet pas de le démontrer :
  à vérifier sur l'ensemble des prédictions Miroir dans le prochain rapport
  avant d'adopter une correction systématique.
---
```

---

## Structure d'une entrée non-évaluable

```yaml
---
id: PRED-2026-03-15-003
[...]
statut: non-evaluable
motif_non_evaluable: >
  L'événement prédit ("renforcement de l'influence de X") n'a pas
  de seuil mesurable convenu à l'avance. Leçon : reformuler
  systématiquement les prédictions d'influence en indicateurs
  observables (votes, positions officielles, citations médiatiques).
---
```

---

## La section Agrégats

Cette section est mise à jour par le skill lors du Mode 3 (rapport). Format :

```markdown
## Agrégats par catégorie
*Dernier calcul : 2026-08-15 — 41 prédictions résolues*

### Par skill source
*Données fictives d'illustration. BSS calculé contre le baseline « toujours 0.5 » (0.25) ; le rapport donne aussi le BSS contre le taux de base.*

| Skill | N | Brier | Log Loss | BSS (vs 0.5) |
|-------|---|-------|----------|-----|
| signaux-du-futur | 22 | 0.162 | 0.491 | 0.35 |
| miroir-trans-echelle | 12 | 0.198 | 0.547 | 0.21 |
| hacking-narratif | 5  | 0.204 | 0.521 | 0.18 |
| fractales-dérivé | 2  | 0.231 | 0.612 | 0.08 |

### Par domaine
| Domaine | N | Brier |
|---------|---|-------|
| géopolitique | 18 | 0.187 |
| économie/entreprises | 15 | 0.150 |
| social/culturel | 8  | 0.228 |

### Par horizon
| Horizon | N | Brier |
|---------|---|-------|
| ≤ 90j | 19 | 0.150 |
| 91-180j | 14 | 0.190 |
| 181-365j | 8  | 0.236 |

*(Moyennes pondérées cohérentes entre ventilations : Brier global ≈ 0.181 dans les trois tableaux.)*

### Biais actifs détectés
- **Sur-confiance** : active (bins [0.7, 0.8) à [0.9, 1.0] : fréquence observée inférieure de plus de 0.12 à la probabilité moyenne)
- **Narrative attractor** : sous le seuil (Δ Brier Miroir vs Signaux = +0.036 < 0.05)
- **Dégradation au-delà de 180 j** : à confirmer (Δ Brier vs ≤ 180 j = +0.069 ; n = 8 seulement)

### Calibration plot — 41 prédictions résolues
[Copier depuis la sortie du rapport]
```

---

## Conventions de nommage des IDs

Format : `PRED-YYYY-MM-DD-NNN`

- `YYYY-MM-DD` : date d'enregistrement
- `NNN` : numéro séquentiel dans la journée (001, 002, …)

Pour les entrées multi-classes (scénarios) : `PRED-YYYY-MM-DD-NNN-MCL`

---

## Fréquence de mise à jour recommandée

| Action | Fréquence |
|--------|-----------|
| Ajout de nouvelles prédictions | À chaque session productive |
| Scoring d'entrées résolues | Hebdomadaire (ou dès qu'un événement est observé) |
| Rapport complet | Mensuel ou trimestriel |
| Révision des agrégats | Après chaque rapport |
| Lecture des leçons accumulées | En début de session (pour mémoire des biais) |

---

## Taille et gestion du fichier

Le log peut devenir long. Recommandations :

- **Archive annuelle** : début janvier, archiver les prédictions résolues de l'année passée dans `calibration-log-YYYY.md`.
- **Log actif** : garder seulement les prédictions ouvertes + les 30 dernières résolues dans `calibration-log.md`.
- **Pas de suppression** : ne jamais supprimer une entrée, même embarrassante. L'intégrité du log est sa valeur principale.
