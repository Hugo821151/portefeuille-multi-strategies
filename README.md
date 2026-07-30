# Portefeuille multi-stratégies — projet d'entraînement PM

Portefeuille simulé d'1 M€ construit pour m'entraîner au métier de portfolio manager.
Trois poches gérées selon des logiques distinctes : stock picking fondamental (40%),
allocation macro tactique (30%), quantitatif systématique (30%).

Ce dépôt contient le code Python du projet. Les données de prix (CSV) sont incluses
pour que les résultats soient reproductibles.

## Contenu

| Fichier | Objet |
|---|---|
| `backtest_momentum.py` | Backtest du facteur momentum sur 10 valeurs du Dow Jones |
| `beta_regression.py` | Calcul de bêta par régression sur le S&P 500 |
| `beta_portefeuille.py` | Bêta des poches et du fonds, sensibilité à un choc de marché |

## Résultats principaux

**Le backtest momentum a échoué — et le résultat est publié tel quel.**

Sélection en juillet 2025 sur le momentum 12 mois, mesure du rendement réalisé sur
les 12 mois suivants :

- Top 3 momentum : **-8,6%**
- Bottom 3 momentum : **+18,4%**
- Univers entier à poids égal : **+18,9%**

Le facteur s'est inversé, et ne rien faire aurait battu la stratégie. Aucun paramètre
n'a été modifié pour obtenir un résultat positif : ce serait de l'overfitting, le moyen
le plus fiable de produire une stratégie qui brille en backtest et perd de l'argent en
réel. La poche n'a pas été déployée.

Limites assumées : une seule date de départ, 10 titres, 3 positions par groupe, aucun
coût de transaction, biais du survivant. Statistiquement, ce test ne prouve rien — il
sert à maîtriser la mécanique, pas à valider un facteur.

**Les bêtas publiés étaient inutilisables tels quels.**

Yahoo Finance mesure le bêta des ETF obligataires contre un indice obligataire, pas
contre les actions : TLT y affiche 2,40, correct face à l'indice agrégé et absurde face
au marché actions. Recalculés par régression sur 60 observations mensuelles contre le
S&P 500 :

| Actif | Bêta | Corrélation | Volatilité |
|---|---|---|---|
| LVMH (LVMUY) | 1,123 | 0,612 | 29,1% |
| TLT (Treasuries 20+) | 0,512 | 0,563 | 14,5% |
| MTH.PA (oblig. euro 25+) | 0,342 | 0,407 | 10,4% |
| IAU (or) | 0,181 | 0,173 | 16,7% |

Les bêtas obligataires sont **positifs** : sur cette période, les obligations longues
n'ont pas couvert le risque actions. L'or est le seul diversifiant réel. Réserve
importante : mesure effectuée sur un régime dominé par l'inflation ; un retour aux chocs
de croissance pourrait restaurer la corrélation négative.

**Bêta du fonds : 0,506 courant / 0,806 cible.**

Deux mesures publiées, parce qu'un gérant décrit l'exposition qu'il détient et non celle
qu'il envisage. L'écart de 0,30 représente le risque non encore pris — 30 000 € dans une
baisse de marché de 10%.

## Pièges rencontrés

**pandas aligne sur l'index, pas sur les dates.** Deux séries de longueurs différentes
sont appariées ligne à ligne, donc mois décalés, sans aucune erreur affichée. Le bêta
d'un ETF de 30 mois calculé contre 60 mois d'indice donnait 0,186 au lieu de 0,342 —
un nombre propre et faux. Correction par `pd.merge(..., on='Date')`.

**La croissance publiée n'est pas la croissance organique.** Sur un dossier, l'écart
entre -5% publié et -1% organique venait presque entièrement du change.

## Reproduire

```bash
pip install pandas
python backtest_momentum.py
python beta_regression.py
python beta_portefeuille.py
```

## Note

Portefeuille entièrement simulé, aucun capital réel engagé. Projet d'apprentissage :
une seule thèse d'investissement sur douze est documentée en profondeur, les autres
reposent sur un travail plus léger. Les limites méthodologiques sont indiquées plutôt
que masquées.
