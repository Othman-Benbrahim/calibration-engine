# Détection des biais — 6 biais récurrents et leurs signatures statistiques

Ce fichier décrit les six biais les plus fréquents dans la prédiction, leurs **signatures statistiques** (patterns repérables dans le log) et leurs **remédiations opératoires**.

---

## 1. Sur-confiance (overconfidence)

### Description

Le biais le plus documenté en psychologie de la décision (Lichtenstein & Fischhoff, 1977). Le prédicteur annonce des probabilités plus extrêmes que ce que ses performances justifient.

**Variante dominante** : sur-confiance aux probabilités hautes. Quand on dit 0.80, ça arrive 0.65 fois. Quand on dit 0.90, ça arrive 0.72 fois.

**Variante inverse** : sous-confiance aux probabilités basses (plus rare). Quand on dit 0.20, ça arrive 0.30 fois.

### Signature statistique

Dans le calibration plot :
- **Courbe systématiquement sous la diagonale** dans la zone 0.6–0.95.
- Reliability élevée (décomposition Brier).
- Log loss disproportionnellement haut sur les prédictions > 0.75.

**Test simple** : filtrer toutes les prédictions avec `probabilite > 0.75`. Si le taux d'occurrence observé est < (probabilite_moyenne - 0.10), sur-confiance probable.

### Origine

- Tendance naturelle à se souvenir des fois où on avait raison.
- Fermeture prématurée du raisonnement : une fois qu'une hypothèse est satisfaisante, on cesse de chercher les contre-arguments.
- Narrative attractor (voir biais 3) : une histoire convaincante augmente la confiance sans augmenter la base factuelle.

### Remédiation

1. **Décote systématique** : avant d'enregistrer, si la probabilité > 0.70, appliquer une réduction de 5-10 points. Tester si ça améliore le Brier.
2. **Inversion** : formuler l'argument contre l'hypothèse. Si l'argument ne coûte rien, la proba devrait baisser.
3. **Outside view** : rechercher le base rate (combien de fois ce type d'événement arrive-t-il historiquement ?). C'est souvent plus bas qu'on ne croit.
4. **Décomposition** : décomposer l'événement en sous-étapes. La probabilité conjointe est toujours inférieure à chaque étape.

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

- Disponibilité heuristique (Kahneman & Tversky, 1973) : les événements faciles à se rappeler semblent plus probables.
- Saturation informationnelle : l'information récente est disproportionnellement accessible.

### Remédiation

1. **Délai de formulation** : pour tout événement majeur, attendre 72 heures avant de formuler des prédictions dépendantes.
2. **Base rate long terme** : ancrer systématiquement sur une fenêtre historique de ≥ 10 ans.
3. **Question de contrôle** : *"Si je formulais cette prédiction il y a 6 mois, avant cet événement, quelle aurait été ma probabilité ?"*

---

## 3. Narrative attractor (biais narratif)

### Description

Propre aux outils symboliques et au raisonnement narratif. Une **histoire cohérente et satisfaisante** augmente la confiance sans augmenter la validité factuelle. Quand Miroir Trans-échelle produit une convergence forte entre archétype et signal, la satisfaction narrative peut gonfler artificiellement les probabilités OSINT.

C'est le biais le plus spécifique à l'écosystème IRIS∞ et potentiellement le plus dangereux : les outils symboliques le produisent par construction.

### Signature statistique

- **Brier systématiquement plus élevé après une lecture trans-échelle** (vs Signaux seul sur le même dossier).
- Pattern : les prédictions formulées après une P3 "à convergence forte" ont tendance à être sur-confiantes.
- Corrélation entre le nombre de convergences fortes dans une carte de résonance et la dérive de calibration sur ce dossier.

**Test** : comparer les prédictions loggées depuis *Signaux seul* vs *Miroir Trans-échelle*. Si le Brier est nettement supérieur pour Miroir, le narrative attractor est actif.

### Origine

- Kahneman (*Thinking Fast and Slow*) : le "système 1" préfère les histoires cohérentes, même factuellemement pauvres.
- "Conjunction fallacy" : un scénario détaillé et narrativement riche semble plus probable qu'un scénario général, même si probabilistiquement c'est l'inverse.

### Remédiation

1. **Règle de sécurité pour Miroir Trans-échelle** : une convergence forte ne peut augmenter une probabilité OSINT de plus de +0.10 au maximum. Si la tentation est plus forte, noter la dissonance et ne pas bouger la proba.
2. **Test de dépouillement** : reformuler la prédiction en langage plat, sans métaphore ni archétype. La proba change-t-elle ? Elle ne devrait pas.
3. **Vérifier la traçabilité factuelle** : pour toute proba > 0.65, exiger au moins 2 signaux factuels solides, indépendants du commentaire symbolique.

---

## 4. Négligence du base rate (base-rate neglect)

### Description

Le prédicteur ignore ou sous-pondère la fréquence historique de la classe d'événements (la "base rate") au profit d'informations spécifiques au cas. Résultat : sur-estimation des probabilités pour les événements rares, sous-estimation pour les événements communs.

### Signature statistique

- **Prédictions de "crises majeures" systématiquement trop hautes** (les crises sont toujours rares).
- Écart entre la fréquence prédite moyenne sur une classe d'événements et la fréquence historique de cette classe.

**Test** : pour chaque domaine (ex : "changement de régime politique"), calculer le taux prédit moyen (moyenne des probabilités formulées). Le comparer au taux historique observé sur 20 ans. Si la différence est > 10 points, base-rate neglect probable.

### Origine

- Kahneman & Tversky (1973) : la "représentativité heuristique" — on juge un cas par sa ressemblance à un prototype, pas par sa fréquence.
- Les situations nouvelles semblent toujours uniques et exceptionnelles. Elles le sont rarement.

### Remédiation

1. **Ritual d'ancrage** : pour toute nouvelle prédiction, chercher et noter explicitement la base rate avant d'ajuster.
2. **Décomposition de l'ajustement** : si base rate = 0.10 et ajustement cible = 0.60, exiger de lister explicitement les 4-5 raisons spécifiques qui justifient cet écart.
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

**Test** : comparer le Brier par domaine (`domaine` field dans le log). Un écart > 0.05 entre le meilleur et le pire domaine sur N > 20 signale un angle mort.

### Origine

- Manque d'informations spécifiques (ex : peu de sources OSINT dans ce domaine).
- Biais culturels ou disciplinaires (expertise forte dans un domaine → moins d'humilité).
- Absence de base rates solides pour ce domaine.

### Remédiation

1. **Réduire systématiquement la confiance** dans les domaines mal calibrés (appliquer un facteur correctif de -0.05 à -0.10 sur toutes les probas).
2. **Enrichir les sources** dans ces domaines.
3. **Signaler aux autres skills** : si le domaine géopolitique est mal calibré, *Signaux du Futur* doit l'intégrer dans ses avertissements de biais.

---

## Tableau récapitulatif

| Biais | Signature principale | Remédiation clé |
|-------|---------------------|-----------------|
| Sur-confiance | Courbe sous diagonale (prob > 0.70) | Décote systématique + outside view |
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
| Sur-confiance | ≥ 2 bins > 0.65 sous la diagonale de > 0.12 |
| Récence | Δ Brier (post-événement vs hors) > 0.06 |
| Narrative attractor | Δ Brier (Miroir vs Signaux seul) > 0.05 |
| Base-rate neglect | Δ taux prédit vs historique > 0.10 |
| Ancrage | Révisions effectives < 50% théorique bayésien |
| Angle mort domaine | Δ Brier inter-domaine > 0.05 sur N ≥ 15 |
