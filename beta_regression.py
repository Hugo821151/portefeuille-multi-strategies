"""
Calcul de beta par regression sur le S&P 500.

Pourquoi recalculer plutot qu'utiliser les betas publies : Yahoo Finance mesure
le beta des ETF obligataires contre un indice OBLIGATAIRE, pas contre les actions.
TLT y affiche 2.40 - correct face a l'indice agrege, absurde face aux actions.
Melanger des betas mesures contre des references differentes produit un beta de
portefeuille denue de sens.

Fenetre : 60 observations mensuelles, aout 2021 - juillet 2026.
Prix ajustes (dividendes inclus), pour mesurer le rendement total reel.
"""

import pandas as pd


def charger(nom):
    df = pd.read_csv(nom)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date').reset_index(drop=True)


titre = charger('TLT.csv')
marche = charger('GSPC.csv')

# Rendements mensuels : r = P(t)/P(t-1) - 1
titre['r'] = titre['AdjClose'].pct_change()
marche['r'] = marche['AdjClose'].pct_change()

# Fusion sur la DATE, pas sur l'index.
# pandas aligne par defaut sur l'index : deux series de longueurs differentes
# seraient appariees ligne a ligne, donc mois a mois decales, sans aucune erreur
# affichee. Bug silencieux et resultat faux.
fusion = pd.merge(titre[['Date', 'r']], marche[['Date', 'r']],
                  on='Date', suffixes=('_titre', '_marche')).dropna()

print("observations communes:", len(fusion))

covariance = fusion['r_titre'].cov(fusion['r_marche'])
variance_marche = fusion['r_marche'].var()
beta = covariance / variance_marche
print("beta du titre vs marche:", round(beta, 3))

# Le beta ne mesure que le risque de marche. Volatilite et correlation
# completent le tableau : un titre peut avoir un beta modere et une
# volatilite elevee si l'essentiel de son risque lui est propre.
volatilite_annualisee = fusion['r_titre'].std() * (12 ** 0.5)
correlation = fusion['r_titre'].corr(fusion['r_marche'])
print("volatilite annualisee:", round(volatilite_annualisee * 100, 1), "%")
print("correlation au marche:", round(correlation, 3))

# RESULTATS
#   TLT   (Treasuries 20+)  beta +0.512 | vol 14.5% | correl 0.563
#   MTH   (oblig. euro 25+) beta +0.342 | vol 10.4% | correl 0.407  (29 obs)
#   IAU   (or)              beta +0.181 | vol 16.7% | correl 0.173
#   LVMUY (LVMH)            beta +1.123 | vol 29.1% | correl 0.612
#
# Les betas obligataires sont POSITIFS : sur cette periode, les obligations
# longues n'ont pas couvert le risque actions. L'or est le seul vrai diversifiant.
