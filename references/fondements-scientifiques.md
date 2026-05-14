# Fondements scientifiques — Calibration prédictive

Ce fichier expose la lignée intellectuelle et les travaux empiriques sur lesquels s'appuie le Calibration Engine. Il est consulté sur demande ou quand la légitimité de la démarche est questionnée.

---

## 1. Glenn Brier (1950) — La mesure fondamentale

**Référence** : Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.

Météorologue de l'U.S. Weather Bureau, Brier introduit en 1950 le score quadratique qui porte son nom. Sa question : comment évaluer si une prévision météo probabiliste est *bonne* ? Ni le taux d'exactitude simple ni la confiance subjective ne suffisent. Il faut une métrique qui mesure simultanément la **discrimination** (distinguer les jours de pluie des jours secs) et la **calibration** (quand on dit 0.7, il pleut bien 7 fois sur 10).

Le Brier score est aujourd'hui la métrique standard de la prédiction probabiliste en météorologie, médecine, finance et renseignement. Sa propriété essentielle (*proper scoring rule*) : annoncer sa vraie probabilité est toujours la stratégie qui maximise le score attendu. On ne peut pas "tricher".

---

## 2. Murphy & Winkler (1977) — La décomposition

**Référence** : Murphy, A. H., & Winkler, R. L. (1977). Reliability of subjective probability forecasts of precipitation and temperature. *Journal of the Royal Statistical Society, Series C*, 26(1), 41-47.

Murphy affine le travail de Brier en décomposant le score en trois composantes (Reliability − Resolution + Uncertainty). Cette décomposition est opérationnelle : elle permet de savoir si un système prédictif échoue parce qu'il est mal calibré, parce qu'il ne discrimine pas, ou simplement parce que le problème est intrinsèquement difficile.

La distinction *calibration / résolution* est fondamentale pour le Calibration Engine : un système peut être parfaitement calibré (dit 0.5, et il arrive 0.5 des fois) mais sans résolution (donc sans valeur). La valeur ajoutée exige les deux.

---

## 3. Lichtenstein & Fischhoff (1977) — La sur-confiance humaine

**Référence** : Lichtenstein, S., & Fischhoff, B. (1977). Do those who know more also know more about how much they know? *Organizational Behavior and Human Performance*, 20(2), 159-183.

Première démonstration systématique que les humains sont **structurellement sur-confiants** dans leurs jugements probabilistes. Les sujets qui disent être "sûrs à 99%" ont tort environ 40% du temps. La compétence dans un domaine n'améliore pas nécessairement la calibration — parfois c'est l'inverse.

Cette découverte a un corollaire direct pour l'écosystème IRIS∞ : la sophistication des outils symboliques (Fractales, Miroir) peut *augmenter* la sur-confiance si elle n'est pas contrebalancée par une mesure explicite. Le Calibration Engine est précisément la réponse à ce risque.

---

## 4. Tversky & Kahneman (1974) — Les heuristiques et leurs biais

**Référence** : Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131.

Trois heuristiques fondamentales identifiées : *représentativité*, *disponibilité*, *ajustement-ancrage*. Chacune produit des biais systématiques en situation d'incertitude. Leur article a inauguré deux décennies de recherche en économie comportementale.

Pour le Calibration Engine, les trois biais les plus directement opératoires sont :
- **Disponibilité** → biais de récence.
- **Représentativité** → négligence du base rate.
- **Ancrage** → sous-révision des probabilités.

---

## 5. Roger Cooke (1991) — L'élicitation d'experts calibrés

**Référence** : Cooke, R. M. (1991). *Experts in Uncertainty: Opinion and Subjective Probability in Science*. Oxford University Press.

Cooke développe la méthode *Classical Model* d'élicitation d'experts probabilistes. Sa contribution centrale : les experts peuvent être évalués sur leur **calibration** (pas sur leur "prestige"), et les mieux calibrés peuvent être pondérés plus fortement dans les agrégations.

Cette idée — que la calibration mesurable est préférable à l'autorité statutaire — est l'un des fondements de la démarche de l'écosystème IRIS∞ : la qualité d'un skill se mesure, elle ne se décrète pas.

---

## 6. Philip Tetlock (2005, 2015) — La science du superforecasting

**Référence principale** : Tetlock, P. E. (2005). *Expert Political Judgment: How Good Is It? How Can We Know?* Princeton University Press.

**Référence opératoire** : Tetlock, P. E., & Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction*. Crown Publishers.

L'œuvre de Tetlock est l'étude empirique la plus rigoureuse sur la prédiction experte en sciences politiques et sociales. Résultats principaux :

- Les experts sectoriels, en moyenne, ne battent pas significativement le hasard sur les prédictions à 1-5 ans.
- Certains "superforecasters" battent les experts de 30% et les marchés prédictifs de 20%.
- Le facteur discriminant n'est pas le QI, le diplôme ou la spécialisation : c'est une **combinaison de dispositions cognitives** (pensée probabiliste, mise à jour active, recherche du contre-argument, humilité épistémique).
- Ces dispositions **s'entraînent** : les participants au Good Judgment Project s'améliorent de 10-20% après entraînement.

**Dix commandements du superforecaster** (synthèse de Tetlock) :

1. Décomposer ("tranche le problème en sous-problèmes").
2. Chercher la base rate (*outside view* avant *inside view*).
3. Ajuster depuis la base rate selon l'information spécifique.
4. Chercher activement les contre-arguments.
5. Probabiliser (éviter les équivalents de "ça va probablement arriver").
6. Distinguer l'incertitude sur l'événement de l'incertitude sur sa propre estimation.
7. Chercher la mise à jour bayésienne continue.
8. Accepter que la sur-confiance est la règle, pas l'exception.
9. Calibrer en faisant du retour sur expérience systématique.
10. Travailler en équipe pour multiplier les angles de vue.

Le Calibration Engine est une implémentation directe des commandements 5, 7, 8 et 9.

---

## 7. Mellers, Tetlock et al. (2014) — Le Good Judgment Project

**Référence** : Mellers, B., Ungar, L., Baron, J., Ramos, J., Gurcay, B., Fincher, K., ... & Tetlock, P. E. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science*, 25(5), 1106-1115.

Démontre expérimentalement que :
- La formation à la calibration améliore les scores de 10-20%.
- Les équipes sont meilleures que les individus, mais seulement si elles débattent les désaccords (pas si elles se contentent de moyenner).
- La *superforecasting mindset* peut être enseignée : c'est une compétence, pas un talent.

---

## 8. Gneiting & Raftery (2007) — Les proper scoring rules

**Référence** : Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359-378.

Formalisation mathématique de la notion de *proper scoring rule* : une règle de score qui incite à annoncer sa vraie probabilité. Le Brier score et le log loss sont *strictly proper*. Une règle "impropre" permettrait de gonfler son score en trichant sur ses probabilités déclarées.

Pour l'architecture du Calibration Engine, seules les proper scoring rules sont admises — c'est une condition d'intégrité du système.

---

## 9. Kahneman (2011) — La théorie des deux systèmes

**Référence** : Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Synthèse grand public de la dual-process theory. Le Système 1 (intuitif, rapide) est structurellement sujet à la sur-confiance, au biais de récence et à l'ancrage. Le Système 2 (analytique, lent) peut corriger le Système 1, mais seulement s'il est *activé délibérément*.

La calibration documentée est précisément un outil d'activation délibérée du Système 2 sur les prédictions produites en grande partie par le Système 1. Dans l'écosystème IRIS∞, les lectures symboliques (Fractales, Miroir) sont massivement Système 1 ; le Calibration Engine force l'intervention du Système 2.

---

## 10. Sources complémentaires

Pour approfondir :

- **Arkes, H. R.** (2001). Overconfidence in judgmental forecasting. In J. S. Armstrong (Ed.), *Principles of Forecasting*. Springer. — Revue complète de la sur-confiance.
- **Dawid, A. P.** (1982). The well-calibrated Bayesian. *Journal of the American Statistical Association*, 77, 605-610. — Fondements bayésiens de la calibration.
- **Fischhoff, B.** (1982). Debiasing. In D. Kahneman, P. Slovic, & A. Tversky (Eds.), *Judgment Under Uncertainty*. Cambridge. — Méthodes de réduction des biais.
- **Yates, J. F.** (1990). *Judgment and Decision Making*. Prentice-Hall. — Manuel complet incluant calibration et scoring.
- **Metaculus** (metaculus.com) — Plateforme de forecasting en temps réel, archive publique de calibrations.
- **Good Judgment Open** (gjopen.com) — Plateforme issue directement du projet Tetlock.

---

## Note sur la légitimité de la démarche

La critique la plus fréquente adressée à la calibration formelle est : *"les sciences humaines et sociales ne se prêtent pas au scoring probabiliste — trop de bruit, trop d'unicité des événements."*

Tetlock a répondu empiriquement à cette critique. Les superforecasters battent des experts et des marchés sur exactement ces domaines. La difficulté des sciences humaines est réelle — elle se traduit par des Brier scores plus élevés — mais elle ne rend pas la calibration impossible ni inutile.

Elle rend seulement **l'humilité calibrée** plus précieuse que la certitude feinte.
