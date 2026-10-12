# Fondements scientifiques — Calibration prédictive

Ce fichier expose la lignée intellectuelle et les travaux empiriques sur lesquels s'appuie le Calibration Engine. Il est consulté sur demande ou quand la légitimité de la démarche est questionnée.

---

## 1. Glenn Brier (1950) — La mesure fondamentale

**Référence** : Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.

Météorologue de l'U.S. Weather Bureau, Brier introduit en 1950 le score quadratique qui porte son nom. Sa question : comment évaluer si une prévision météo probabiliste est *bonne* ? Ni le taux d'exactitude simple ni la confiance subjective ne suffisent. Il faut une métrique qui mesure simultanément la **discrimination** (distinguer les jours de pluie des jours secs) et la **calibration** (quand on dit 0.7, il pleut bien 7 fois sur 10).

Le Brier score est aujourd'hui une métrique standard de la prédiction probabiliste en météorologie, médecine, finance et dans les tournois de prévision géopolitique. Sa propriété essentielle (règle de score *strictement propre*) : annoncer sa vraie probabilité est la stratégie qui minimise la perte attendue. Déclarer une probabilité différente de sa croyance ne peut que dégrader le score espéré.

---

## 2. Murphy (1973) — La décomposition

**Référence** : Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology*, 12(4), 595-600.

Murphy affine le travail de Brier en décomposant le score en trois composantes (Reliability − Resolution + Uncertainty).

*Note d'attribution* : l'article de Murphy & Winkler (1977, *JRSS Series C*, 26(1), 41-47) porte sur la fiabilité de prévisions subjectives de précipitations et de températures ; il n'est pas la source de la décomposition, contrairement à ce qu'indiquait la version 1.0 de ce fichier. Cette décomposition est opérationnelle : elle permet de savoir si un système prédictif échoue parce qu'il est mal calibré, parce qu'il ne discrimine pas, ou simplement parce que le problème est intrinsèquement difficile.

La distinction *calibration / résolution* est fondamentale pour le Calibration Engine : un système peut être parfaitement calibré (il annonce toujours le taux de base, et les événements surviennent bien à cette fréquence) mais sans résolution, donc sans valeur. La valeur ajoutée exige les deux.

---

## 3. Fischhoff, Slovic & Lichtenstein (1977) ; Lichtenstein & Fischhoff (1977) — La sur-confiance humaine

**Références** :
- Fischhoff, B., Slovic, P., & Lichtenstein, S. (1977). Knowing with certainty: The appropriateness of extreme confidence. *Journal of Experimental Psychology: Human Perception and Performance*, 3(4), 552-564.
- Lichtenstein, S., & Fischhoff, B. (1977). Do those who know more also know more about how much they know? *Organizational Behavior and Human Performance*, 20(2), 159-183.
- Lichtenstein, S., Fischhoff, B., & Phillips, L. D. (1982). Calibration of probabilities: The state of the art to 1980. In D. Kahneman, P. Slovic & A. Tversky (Eds.), *Judgment under Uncertainty* (pp. 306-334). Cambridge University Press.

Ces travaux comptent parmi les démonstrations les plus citées de la **sur-confiance** dans les jugements probabilistes (ils ne sont pas les premiers : la revue de 1982 recense des études dès les années 1950-1960).

Chiffre de référence (Fischhoff, Slovic & Lichtenstein, 1977, expérience 1, tableau 1) : parmi les réponses que les sujets jugeaient **certaines** (probabilité 1.00), 71,7 % à 83,1 % seulement étaient justes selon le format de question, soit environ **17 à 28 % d'erreurs** (les auteurs écrivent « environ 17 % à 30 % »). La version 1.0 de ce fichier annonçait « 40 % d'erreur à 99 % de confiance », chiffre non étayé et adossé au mauvais article.

Lichtenstein & Fischhoff (1977) examinent, eux, le lien entre niveau de connaissance et calibration ; ils documentent l'**effet difficile/facile** : sur-confiance sur les questions difficiles, tendance à la sous-confiance sur les questions faciles. La compétence ne garantit donc pas la calibration, et la difficulté de la tâche module fortement le biais.

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

L'œuvre de Tetlock compte parmi les études empiriques les plus importantes sur la prédiction experte en sciences politiques et sociales. Résultats principaux :

- Dans *Expert Political Judgment* (2005), les experts font en moyenne à peine mieux que des règles d'extrapolation simples ou que le hasard, et leur précision se rapproche du hasard à mesure que l'horizon s'allonge (plusieurs années).
- Dans le tournoi IARPA ACE (2011-2015), l'équipe Good Judgment a battu le groupe contrôle de plus de 50 % selon le responsable du programme IARPA ; Good Judgment affirme en outre une précision supérieure de plus de 30 % à celle d'analystes du renseignement ayant accès à des informations classifiées (affirmation institutionnelle, sans protocole publié sur la page source).
- La spécialisation sectorielle ne suffit pas : la précision dépend d'une **combinaison** d'aptitudes et de dispositions (ouverture d'esprit), de conditions (entraînement, équipe) et de pratiques (mises à jour fréquentes et graduelles, effort) (Mellers et al., 2015).
- L'entraînement a un effet mesurable mais modeste : un module de moins d'une heure améliore le Brier de **6 à 11 %** par rapport au groupe contrôle (Chang, Chen, Mellers & Tetlock, 2016).

**Les Dix commandements du superforecaster** (Tetlock & Gardner, 2015 ; liste publiée par Good Judgment) :

1. Triage : se concentrer sur les questions où l'effort paie.
2. Décomposer les problèmes apparemment insolubles en sous-problèmes traitables.
3. Trouver le bon équilibre entre vue intérieure et vue extérieure.
4. Trouver le bon équilibre entre sous-réaction et sur-réaction aux nouvelles informations.
5. Chercher les forces causales contradictoires à l'œuvre.
6. Distinguer autant de degrés d'incertitude que le problème le permet, mais pas davantage.
7. Trouver le bon équilibre entre sous-confiance et sur-confiance, entre prudence et décision.
8. Chercher les erreurs derrière ses erreurs, sans céder au biais rétrospectif.
9. Faire ressortir le meilleur des autres, et laisser les autres faire ressortir le meilleur de soi.
10. Maîtriser la « bicyclette d'équilibrage des erreurs » (pratique avec retour d'information).
(11.) Ne pas traiter les commandements comme des commandements.

*Note* : la version 1.0 de ce fichier présentait sous ce titre une liste qui n'est pas celle de Tetlock.

Le Calibration Engine sert principalement les commandements 4, 6, 7 et 10 : il rend visibles la sur- ou sous-réaction, la sur- ou sous-confiance, et fournit le retour d'information sans lequel la pratique ne s'améliore pas.

---

## 7. Mellers et al. (2014, 2015) ; Chang et al. (2016) — Le Good Judgment Project

**Références** :
- Mellers, B., Ungar, L., Baron, J., Ramos, J., Gurcay, B., Fincher, K., ... & Tetlock, P. E. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science*, 25(5), 1106-1115.
- Mellers, B., Stone, E., Atanasov, P., et al. (2015). The psychology of intelligence analysis: Drivers of prediction accuracy in world politics. *Journal of Experimental Psychology: Applied*, 21(1), 1-14.
- Chang, W., Chen, E., Mellers, B., & Tetlock, P. (2016). Developing expert political judgment: The impact of training and practice on judgmental accuracy in geopolitical forecasting tournaments. *Judgment and Decision Making*, 11(5), 509-526.

Résultats :
- Un court module d'entraînement au raisonnement probabiliste (moins d'une heure) améliore la précision ; l'effet mesuré est de **6 à 11 %** sur le Brier par rapport au contrôle (Chang et al., 2016). La version 1.0 annonçait « 10-20 % après 3-6 séances », formulation introuvable dans ces articles.
- Le travail en équipe et le suivi des meilleurs prévisionnistes (*tracking*) améliorent aussi la précision (Mellers et al., 2014).
- Des variables dispositionnelles (aptitudes cognitives, connaissances politiques, ouverture d'esprit), situationnelles (entraînement, équipe) et comportementales (temps de délibération, fréquence des mises à jour) prédisent la précision (Mellers et al., 2015).

---

## 8. Gneiting & Raftery (2007) — Les proper scoring rules

**Référence** : Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359-378.

Formalisation mathématique de la notion de *proper scoring rule* : une règle de score qui incite à annoncer sa vraie probabilité. Le Brier score et le log loss sont *strictly proper*. Une règle "impropre" permettrait de gonfler son score en trichant sur ses probabilités déclarées.

Pour l'architecture du Calibration Engine, seules des règles de score propres (Brier, log loss) servent à **évaluer** les prédictions. Les autres indicateurs du rapport (sharpness, accuracy, calibration plot) sont des diagnostics, jamais des critères de score.

## 8 bis. Gneiting, Balabdaoui & Raftery (2007) — Calibration et sharpness

**Référence** : Gneiting, T., Balabdaoui, F., & Raftery, A. E. (2007). Probabilistic forecasts, calibration and sharpness. *Journal of the Royal Statistical Society: Series B*, 69(2), 243-268.

Source du principe « maximiser la sharpness des distributions prédictives sous contrainte de calibration », repris dans `metriques-scoring.md` §5.

---

## 9. Kahneman (2011) — La théorie des deux systèmes

**Référence** : Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Synthèse grand public de la dual-process theory. Le Système 1 (intuitif, rapide) est structurellement sujet à la sur-confiance, au biais de récence et à l'ancrage. Le Système 2 (analytique, lent) peut corriger le Système 1, mais seulement s'il est *activé délibérément*.

La calibration documentée peut se lire comme un outil d'activation délibérée du Système 2 sur des prédictions produites en grande partie par le Système 1. Dans l'écosystème IRIS∞, les lectures symboliques (Fractales, Miroir) relèvent surtout de l'intuition ; le Calibration Engine impose la vérification. (Le cadre des deux systèmes est une métaphore utile, discutée dans la littérature ; il n'est pas utilisé ici comme modèle causal.)

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

Tetlock a répondu empiriquement à cette critique : dans les tournois de prévision géopolitique, certains prévisionnistes sont durablement mieux calibrés et plus discriminants que d'autres, sur des horizons courts (en général moins d'un an). La difficulté des sciences humaines est réelle — elle se traduit par des Brier scores plus élevés — mais elle ne rend pas la calibration impossible ni inutile.

Elle rend seulement **l'humilité calibrée** plus précieuse que la certitude feinte.
