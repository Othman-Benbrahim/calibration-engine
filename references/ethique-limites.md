# Éthique et limites — Ce que la calibration ne peut pas faire

Ce fichier expose les limites structurelles du Calibration Engine, le risque de Goodhart, les domaines non-calibrables, et les obligations d'honnêteté qui conditionnent la valeur du système.

---

## 1. Le biais de Goodhart — La limite fondamentale

### Énoncé

> *"When a measure becomes a target, it ceases to be a good measure."*
> — Charles Goodhart (1975), reformulé par Marilyn Strathern (1997)

Le biais de Goodhart s'énonce ainsi : dès qu'on optimise pour un indicateur, on finit par optimiser *l'indicateur lui-même* plutôt que la réalité qu'il est supposé mesurer.

### Application au Calibration Engine

Un utilisateur qui **optimise son Brier score** peut le faire de plusieurs façons sans améliorer sa prédictivité réelle :

1. **Sélection des prédictions enregistrées** : logger seulement les prédictions dont on est assez confiant, oublier les autres.
2. **Reformulation a posteriori** : ajuster la formulation de la prédiction après coup pour qu'elle soit "plus vraie".
3. **Ancrage sur 0.5** : dire systématiquement 0.5 sur tout. Le Brier sera modeste (0.25) mais sans valeur.
4. **Horizon courts uniquement** : les prédictions à court terme sont plus faciles à calibrer. Éviter les horizons longs maintient un bon Brier apparent.
5. **Domaines maîtrisés uniquement** : ne logger que les domaines où on est bon, ignorer les angles morts.

### Comment le Calibration Engine y répond

- **Intégrité de l'enregistrement** est non-négociable : refus de modifier des entrées passées.
- **Alerte sur la sharpness** : si toutes les prédictions gravitent autour de 0.5, le rapport signale une calibration "triviale".
- **Couverture minimale de domaines** : le rapport signale si un domaine récurrent est sous-représenté dans le log.
- **Rapport de complétude** : à terme, si l'utilisateur utilise *Signaux* 20 fois et ne log que 5 prédictions, signaler.

### La responsabilité appartient à l'utilisateur

Finalement, **aucun système ne peut forcer l'honnêteté**. Le Calibration Engine peut la rappeler, l'encourager structurellement, rendre la triche visible. Mais si l'utilisateur choisit de ne pas logger ses prédictions ratées, le système ne peut pas le détecter.

La promesse de la calibration n'a de valeur que si l'utilisateur l'honore.

---

## 2. Domaines structurellement non-calibrables

Tous les événements ne se prêtent pas à la calibration probabiliste. Le skill identifie et signale ces cas pour ne pas produire une fausse rigueur.

### 2.1 Événements de classe unique (Black Swans)

Les événements sans précédent statistique raisonnable ne peuvent être calibrés.

- Exemple : probabilité d'un tremblement de terre de magnitude > 9.5 en Europe de l'Ouest cette année.
- Exemple : probabilité qu'une IA superintelligente émerge avant 2030.

**Traitement** : logger si l'utilisateur le souhaite, mais marquer `calibration_possible: false` et ne pas inclure dans les agrégats.

### 2.2 Événements trop rares pour l'échantillon

Même si une base rate théorique existe, si l'utilisateur n'a que 2-3 prédictions dans cette catégorie, la calibration est sans sens statistique.

**Traitement** : le rapport indique explicitement les catégories avec N < 10 comme "insuffisant pour interprétation".

### 2.3 Événements intrinsèquement vagues

Si l'événement prédit est défini trop largement pour être observé sans ambiguïté, le scoring est contestable.

- Exemple flou : "La situation géopolitique va se détériorer en Europe."
- Exemple précis : "Au moins 3 des 27 États membres de l'UE déclencheront l'article 7 TUE dans les 24 mois."

**Traitement** : demander reformulation. Si l'utilisateur refuse, logger en `statut: non-evaluable` sans inclure dans les agrégats.

### 2.4 Horizons très longs (> 5 ans)

La prédiction à très long terme relève d'un autre régime analytique (scenario planning, futuribles). Les métriques de calibration courte ne s'y appliquent pas de manière significative.

**Traitement** : logger librement, mais signaler dans le rapport que les prédictions > 5 ans forment un sous-ensemble méthodologiquement distinct.

### 2.5 Prédictions sur états internes

On ne peut calibrer que des faits observables, pas des états psychologiques ou intentionnels d'un tiers.

- Non calibrable : "X est en train de perdre confiance dans son équipe."
- Calibrable : "X va remplacer au moins 2 membres de son équipe dirigeante dans les 6 mois."

---

## 3. La calibration ne crée pas la compétence

### Ce que la calibration mesure

La calibration mesure la **cohérence entre confiance et performance**. Un système parfaitement calibré et systématiquement médiocre est parfaitement calibré — il dit 0.5 tout le temps et c'est honnête.

Ce que la calibration ne mesure pas : *pourquoi* certaines prédictions sont bonnes et d'autres mauvaises. Elle identifie les patterns, mais l'amélioration vient d'un travail analytique (meilleure collecte OSINT, hypothèses plus rigoureuses, biais identifiés et corrigés).

### La distinction calibration / résolution

Un système peut être bien calibré **sans avoir de valeur** :
- Calibration parfaite + résolution nulle = dire systématiquement le base rate. Aucune information ajoutée.
- Calibration parfaite + résolution élevée = le saint graal.

C'est pourquoi le rapport affiche toujours les deux métriques (reliability + resolution dans la décomposition de Brier). Un bon Brier global cache parfois une résolution nulle.

---

## 4. Limites de l'approche probabiliste sur les sciences humaines

### L'unicité des événements historiques

Chaque événement géopolitique ou social est en partie unique. La base rate d'un événement exactement similaire est souvent nulle. On extrapole toujours depuis des classes d'événements plus larges — ce qui introduit une incertitude structurelle.

### La réflexivité

En sciences humaines, les prédictions peuvent *influencer* l'événement prédit (prophéties auto-réalisatrices ou auto-invalidantes). Un analyste qui publie ses probabilités modifie le système qu'il analyse. Cette propriété n'existe pas en météorologie.

### La non-stationnarité

Les structures qui sous-tendent les régularités statistiques évoluent. Ce qui avait une base rate de 15% sur 2000-2020 peut avoir une base rate de 40% sur 2020-2030 si les conditions structurelles changent. Les modèles basés sur des historiques longs peuvent être en retard sur les ruptures.

### Ce que cela implique

Ces limites ne rendent pas la calibration inutile. Elles la rendent **humble**. Le rapport doit explicitement noter l'incertitude structurelle là où elle est forte, et ne pas prétendre à une précision que les données ne justifient pas.

---

## 5. Obligations éthiques d'utilisation

### 5.1 Honnêteté de l'enregistrement

L'enregistrement doit refléter la croyance réelle au moment de la prédiction, pas la croyance qu'on aimerait avoir eu. Cela implique :
- Ne pas attendre de voir si la situation "se confirme" avant de logger.
- Inclure systématiquement les prédictions ratées.
- Ne jamais modifier une entrée passée.

### 5.2 Non-utilisation des scores à des fins de persuasion trompeuse

Un Brier score de 0.17 peut impressionner un interlocuteur non-statisticien. Il ne doit pas être présenté comme "90% de taux de réussite" ou autre reformulation flatteuse. Le skill fournit le BSS et la comparaison au baseline pour contextualiser honnêtement.

### 5.3 Transparence sur les conditions

Toute communication publique d'un score de calibration doit mentionner :
- La taille de l'échantillon.
- La période couverte.
- Les domaines inclus (et exclus).
- La définition exacte des prédictions loggées.

Sans ces éléments, le score n'est pas communicable de manière honnête.

### 5.4 Usage personnel avant tout

Le Calibration Engine est conçu pour un auto-amélioration personnelle. Son usage pour évaluer ou comparer des tiers (analystes, politiques, journalistes) sans leur consentement et sans le même protocole d'enregistrement est hors scope et potentiellement trompeur.

---

## 6. Ce que le skill peut et ne peut pas promettre

| Promesse tenue | Promesse non tenue |
|----------------|-------------------|
| Mesurer la performance prédictive passée | Garantir une amélioration future |
| Identifier des biais systématiques | Éliminer ces biais automatiquement |
| Comparer les skills entre eux | Dire lequel est "objectivement meilleur" dans l'absolu |
| Rendre le progrès visible et traçable | Produire ce progrès sans effort analytique |
| Forcer la discipline de falsifiabilité | Forcer l'honnêteté de l'utilisateur |
| Signaler les domaines non-calibrables | Prédire dans ces domaines à la place |

---

## 7. Déclaration de statut épistémique

Le Calibration Engine est lui-même soumis aux limites qu'il impose aux autres skills.

- Il ne peut évaluer que ce qui lui est soumis (biais de sélection possible).
- Ses seuils de détection des biais (définis dans `detection-biais.md`) sont des conventions raisonnables, pas des vérités statistiques absolues.
- Ses recommandations d'ajustement (ex : décote de 0.08 sur les prédictions Miroir) sont des estimations à réviser au fil du log.

En d'autres termes : **le Calibration Engine lui-même doit être calibré**, par l'usage, par le retour d'expérience, et par la révision périodique de ses seuils et conventions.

---

*« La mesure honnête d'une performance médiocre vaut infiniment plus qu'une illusion de compétence. Le Calibration Engine sert ceux qui préfèrent savoir à ceux qui préfèrent croire. »*
