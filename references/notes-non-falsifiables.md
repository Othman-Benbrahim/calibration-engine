# Notes non falsifiables — gabarit d'annexe

Ce fichier est un **gabarit**. L'utilisateur le copie à côté de son `calibration-log.md` (même dossier, même nom `notes-non-falsifiables.md`) et y consigne les énoncés prospectifs qui n'ont pas passé le test du sceptique de `protocole-enregistrement.md`.

Ces notes **n'entrent dans aucun agrégat** (Brier, log loss, calibration plot). Elles servent à deux choses :

1. Garder la mémoire d'une intuition sans la déguiser en prédiction scorable.
2. Repérer les formulations qui échouent souvent, pour apprendre à les reformuler.

---

## Règles

- Une note n'a **pas** de probabilité ni de score. Si une probabilité et un critère de résolution peuvent être fixés, l'énoncé doit être reformulé et enregistré dans le log.
- Une note peut être **promue** en prédiction plus tard, si l'utilisateur parvient à la rendre falsifiable. La promotion crée une nouvelle entrée datée du jour de la promotion ; la note d'origine reste, avec un renvoi.
- On ne score jamais une note rétrospectivement : ce serait reconstruire après coup un critère que l'on n'avait pas fixé.

---

## Format d'une note

```yaml
---
id: NOTE-AAAA-MM-JJ-NNN
date: AAAA-MM-JJ
skill_source: [skill d'origine ou "humain"]
enonce: >
  [L'énoncé tel qu'il a été formulé]
raison_non_falsifiable: >
  [Ce qui manque : événement observable ? seuil ? date ? source de résolution ?]
tentative_de_reformulation: >
  [La meilleure reformulation obtenue, et pourquoi elle reste insuffisante]
promue_en: null   # ou l'id PRED-… si la note a été rendue falsifiable plus tard
---
```

## Exemple

```yaml
---
id: NOTE-2026-05-20-001
date: 2026-05-20
skill_source: miroir-trans-echelle
enonce: >
  Le récit dominant autour de l'entreprise X va basculer.
raison_non_falsifiable: >
  « Récit dominant » et « basculer » n'ont ni indicateur ni seuil ; pas de date.
tentative_de_reformulation: >
  « Avant le 31/12/2026, plus de la moitié des titres de trois quotidiens nationaux
  consacrés à X qualifieront l'entreprise de "en difficulté" » — rejetée : la grille
  de classement des titres n'est pas définie et serait contestable à la résolution.
promue_en: null
---
```

---

## Usage dans le rapport de calibration

Le rapport du `calibration-engine` peut indiquer le **nombre** de notes par skill source sur la période, comme indicateur de discipline de formulation (un skill qui produit beaucoup de notes non falsifiables formule mal ses sorties prédictives). Aucun autre usage quantitatif n'en est fait.
