# Détection des biais — 6 familles de biais et leurs signatures statistiques

Ce fichier décrit six familles de biais fréquentes dans la prédiction, leurs **signatures statistiques** (patterns repérables dans le log, calculés avec `scripts/scoring.py`) et leurs **remédiations opératoires**. Les seuils de détection sont des **conventions** du skill (voir `ethique-limites.md` §7), pas des tests statistiques.

---

## 1. Sur-confiance (overconfidence) et sous-confiance

### Description

L'un des biais les plus documentés en psychologie du jugement (Lichtenstein, Fischhoff & Phillips, 1982). Le prédicteur annonce des probabilités **plus extrêmes** que ce que ses performances justifient : trop proches de 1 pour ce qu'il croit probable, trop proches de 0 pour ce qu'il croit improbable.

**Aux probabilités hautes** : on dit 0.80, ça arrive 0.65 fois ; on dit 0.90, ça arrive 0.72 fois.

**Aux probabilités basses** : on dit 0.20, ça arrive 0.30 fois ; on dit 0.05, ça arrive 0.15 fois. *C'est aussi de la sur-confiance* (prévision trop proche de 0). La version 1.0 de ce fichier l'appelait à tort « sous-confiance ».

**Sous-confiance** (le cas inverse, plus rare chez les analystes) : prévisions **pas assez tranchées**. On dit 0.70, ça arrive 0.90 fois ; on dit 0.30, ça arrive 0.10 fois.

### Signature statistique

Dans le calibration plot (voir `metriques-scoring.md` §4) :
- Sur-confiance : courbe **plus plate** que la diagonale — sous la diagonale pour p > 0.5, au-dessus pour p < 0.5.
- Sous-confiance : courbe **plus pentue** que la diagonale.
- Reliability élevée (décomposition de Murphy).
- Log loss disproportionnellement haut sur les prédictions extrêmes (p > 0.75 ou p < 0.25).

**Test simple** : filtrer les prédictions avec `probabilite ≥ 0.70` ; si la fréquence observée est inférieure à (probabilité moyenne − 0.10), sur-confiance probable aux hautes probabilités. Symétriquement, filtrer `probabilite ≤ 0.30` ; si la fréquence observée dépasse (probabilité moyenne + 0.10), sur-confiance probable aux basses probabilités.

### Origine

- Tendance naturelle à se souvenir des fois où on avait raison.
- Fermeture prématurée du raisonnement : une fois qu'une hypothèse est satisfaisante, on cesse de chercher les contre-arguments.
- Narrative attractor (voir biais 3) : une histoire convaincante augmente la confiance sans augmenter la base factuelle.

### Remédiation

1. **Rétrécissement vers le taux de base** : si le rapport établit une sur-confiance, rapprocher les probabilités extrêmes du taux de base de la classe (baisser les hautes, **relever** les basses), d'une ampleur fondée sur l'écart observé. Vérifier ensuite que le Brier s'améliore sur les nouvelles prédictions.
2. **Inversion** : formuler l'argument contre l'hypothèse. Si l'argument ne coûte rien, la proba devrait baisser.
3. **Outside view** : rechercher le base rate (combien de fois ce type d'événement arrive-t-il historiquement ?). C'est souvent plus bas qu'on ne croit.
4. **Décomposition** : décomposer l'événement en sous-étapes nécessaires. La probabilité conjointe est inférieure ou égale à celle de chacune des étapes.

---

## 2. Biais de récence (recency bias)

### Description

Les événements récents sont surpondérés dans l'estimation de probabilité au détriment des tendances longues. Un incident médiatique récent gonfle irrationnellement la probabilité d'un scénario.

### Signature statistique

- **Dégradation du Brier sur les prédictions formulées dans les 7-10 jours suivant un événement majeur**.
- Pattern temporel : les prédictions formulées en "pic de saillance médiatique" ont un Brier significativement plus élevé que celles formulées en période calme sur le même domaine.
- Corrélation entre volume de presse sur le sujet (si tracé) et écart de calibration.

**Test** : comparer le Brier moyen des prédictions formulées dans les 14 jours suivant un événement majeur vs le reste de l'échantillon.

### Origine

- Heuristique de disponibilité (Tversky & Kahneman, 1973, *Cognitive Psychology*) : les événements faciles à se rappeler semblent plus probables.
- Saturation informationnelle : l'information récente est disproportionnellement accessible.

### Remédiation

1. **Délai de formulation** (heuristique interne) : pour tout événement majeur, attendre environ 72 heures avant de formuler des prédictions dépendantes.
2. **Base rate long terme** : ancrer systématiquement sur une fenêtre historique de ≥ 10 ans.
3. **Question de contrôle** : *"Si je formulais cette prédiction il y a 6 mois, avant cet événement, quelle aurait été ma probabilité ?"*

---

## 3. Narrative attractor (biais narratif)

### Description

Propre aux outils symboliques et au raisonnement narratif. Une **histoire cohérente et satisfaisante** augmente la confiance sans augmenter la validité factuelle. Quand Miroir Trans-échelle produit une convergence forte entre archétype et signal, la satisfaction narrative peut gonfler artificiellement les probabilités OSINT.

C'est le biais le plus spécifique à l'écosystème IRIS∞ et potentiellement le plus dangereux : les outils symboliques le produisent par construction.

### Signature statistique

- **Brier systématiquement plus élevé après une lecture trans-échelle** (vs *Signaux du Futur* seul sur le même dossier).
- Pattern : les prédictions formulées après une P3 "à convergence forte" ont tendance à être sur-confiantes.
- Corrélation entre le nombre de convergences fortes dans une carte de résonance et la dérive de calibration sur ce dossier.

**Test** : comparer les prédictions loggées depuis *Signaux seul* vs *Miroir Trans-échelle*. Si le Brier est nettement supérieur pour Miroir, le narrative attractor est un suspect. **Limite** : les deux skills ne traitent pas forcément les mêmes dossiers ; une différence de Brier peut refléter des questions plus difficiles. Comparer sur des dossiers communs, ou comparer la reliability plutôt que le Brier brut.

### Origine

- Kahneman (*Thinking, Fast and Slow*, 2011, chap. 19) : l'intuition préfère les histoires cohérentes, même factuellement pauvres.
- Erreur de conjonction (Tversky & Kahneman, 1983) : un scénario détaillé et narrativement riche semble plus probable qu'un scénario général qui le contient, alors que sa probabilité ne peut être que inférieure ou égale.

### Remédiation

1. **Règle de sécurité pour Miroir Trans-échelle** : une convergence forte ne peut augmenter une probabilité OSINT de plus de +0.10, quel que soit le prior (en termes bayésiens : BF ≤ 1.49 ; voir `interop-skills.md`). Si la tentation est plus forte, noter la dissonance et ne pas dépasser le plafond.
2. **Test de dépouillement** : reformuler la prédiction en langage plat, sans métaphore ni archétype. La proba change-t-elle ? Elle ne devrait pas.
3. **Vérifier la traçabilité factuelle** : pour toute proba > 0.65, exiger au moins 2 signaux factuels solides, indépendants du commentaire symbolique.

---

## 4. Négligence du base rate (base-rate neglect)

### Description

Le prédicteur ignore ou sous-pondère la fréquence historique de la classe d'événements (la "base rate") au profit d'informations spécifiques au cas. Résultat : sur-estimation des probabilités pour les événements rares, sous-estimation pour les événements communs.

### Signature statistique

- **Prédictions de "crises majeures" systématiquement trop hautes** (les crises sont toujours rares).
- Écart entre la fréquence prédite moyenne sur une classe d'événements et la fréquence historique de cette classe.

**Test** : pour chaque classe d'événements (ex : « changement de régime politique »), calculer le taux prédit moyen (moyenne des probabilités formulées). Le comparer au taux historique de la classe (fenêtre et source documentées). Si la différence dépasse 10 points, négligence du taux de base probable.

### Origine

- Kahneman & Tversky (1973, « On the psychology of prediction », *Psychological Review*) : l'heuristique de représentativité — on juge un cas par sa ressemblance à un prototype, en négligeant les taux de base.
- Les situations nouvelles semblent toujours uniques et exceptionnelles. Elles le sont rarement.

### Remédiation

1. **Ritual d'ancrage** : pour toute nouvelle prédiction, chercher et noter explicitement la base rate avant d'ajuster.
2. **Décomposition de l'ajustement** : si le taux de base est 0.10 et la probabilité visée 0.60, exiger de lister explicitement les raisons spécifiques qui justifient cet écart, et leur poids.
3. **Regroupement par classes** : créer des "classes de référence" pour les domaines récurrents (coups d'état, crises de gouvernance, restructurations d'entreprises, etc.) avec leurs fréquences sur 20 ans.

---

## 5. Ancrage (anchoring)

### Description

La première information reçue sur un sujet sert d'ancrage et fausse les estimations ultérieures. Même lorsque l'ancrage est connu comme arbitraire, son effet persiste.

**Version particulière au Calibration Engine** : la première prédiction formulée sur un dossier influence les prédictions ultérieures sur le même dossier, même après mise à jour bayésienne.

### Signature statistique

- **Faible dispersion des probabilités** sur les révisions d'un même dossier : les mises à jour sont trop petites au regard des nouvelles informations.
- Pattern bayésien : P(H | E) calculée manuellement est significativement différente de la proba révisée intuitivement déclarée.

**Test** : pour les prédictions ayant fait l'objet de révisions, calculer le mouvement bayésien théorique et le comparer au mouvement effectif. Si le mouvement effectif est systématiquement < 50% du mouvement théorique, ancrage actif.

### Origine

- Tversky & Kahneman (1974) : expériences canoniques avec roue de loterie. L'ancrage fonctionne même avec des ancres manifestement absurdes.
- En analyse : la première hypothèse qu'on formule structure tout le raisonnement suivant.

### Remédiation

1. **Délibérer avant de lire** : avant de lire les rapports d'autres analystes, formuler une probabilité a priori.
2. **Révisions forcées** : quand une nouvelle information majeure arrive, se forcer à recalculer la probabilité *from scratch*, sans regarder la valeur précédente.
3. **Révision bayésienne formelle** : utiliser la formule de Bayes explicitement, au lieu de réviser "à l'intuition".

---

## 6. Angle mort de domaine (domain blind spot)

### Description

Le prédicteur est systématiquement moins bien calibré dans certains domaines que d'autres, souvent sans en être conscient. Ce biais est détectable uniquement avec un historique suffisant, d'où l'importance du log.

### Signature statistique

- **Brier significativement plus élevé dans un domaine particulier** (ex : technologie, social) qu'en moyenne.
- Corrélation entre le domaine et la dégradation de calibration, stable sur plusieurs périodes.

**Test** : comparer le Brier par domaine (champ `domaine` du log). Un écart > 0.05 entre le meilleur et le pire domaine, avec au moins 15 prédictions dans chacun des deux, signale un angle mort possible. Comme pour le narrative attractor, un domaine peut simplement être plus difficile : comparer aussi la reliability, qui isole la calibration de la difficulté.

### Origine

- Manque d'informations spécifiques (ex : peu de sources OSINT dans ce domaine).
- Biais culturels ou disciplinaires (expertise forte dans un domaine → moins d'humilité).
- Absence de base rates solides pour ce domaine.

### Remédiation

1. **Réduire la confiance** dans les domaines mal calibrés : rapprocher les probabilités du taux de base du domaine (baisser les probabilités hautes **et relever les basses**). Retrancher un montant fixe à toutes les probabilités rendrait les prédictions basses plus extrêmes, donc pires.
2. **Enrichir les sources** dans ces domaines.
3. **Signaler aux autres skills** : si le domaine géopolitique est mal calibré, *Signaux du Futur* doit l'intégrer dans ses avertissements de biais.

---

## Tableau récapitulatif

| Biais | Signature principale | Remédiation clé |
|-------|---------------------|-----------------|
| Sur-confiance | Courbe plus plate que la diagonale | Rétrécissement vers le taux de base + outside view |
| Sous-confiance | Courbe plus pentue que la diagonale | Oser des probabilités plus tranchées là où le log le justifie |
| Récence | Brier dégradé post-événement majeur | Délai 72h + base rate long terme |
| Narrative attractor | Brier supérieur après lecture symbolique | Cap +0.10 sur convergence forte |
| Base-rate neglect | Taux prédit > taux historique | Ancrage obligatoire sur base rate |
| Ancrage | Révisions < théorique bayésien | Révision from scratch |
| Angle mort domaine | Brier élevé domaine spécifique | Facteur correctif + enrichir sources |

---

## Seuils de détection dans le rapport

Le Calibration Engine signale un biais comme **actif** si son pattern statistique dépasse un seuil sur un échantillon d'au moins 15 prédictions dans la catégorie concernée :

| Biais | Seuil |
|-------|-------|
| Sur-confiance (hautes p.) | ≥ 2 bins au-dessus de 0.6 dont la fréquence observée est inférieure de plus de 0.12 à la probabilité moyenne |
| Sur-confiance (basses p.) | ≥ 2 bins en dessous de 0.4 dont la fréquence observée dépasse de plus de 0.12 la probabilité moyenne |
| Récence | Δ Brier (post-événement vs hors) > 0.06 |
| Narrative attractor | Δ Brier (Miroir vs Signaux seul, mêmes dossiers) > 0.05 |
| Base-rate neglect | Δ taux prédit vs historique > 0.10 |
| Ancrage | Révisions effectives < 50% théorique bayésien |
| Angle mort domaine | Δ Brier inter-domaine > 0.05 sur N ≥ 15 |
