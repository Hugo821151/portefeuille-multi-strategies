"""
Backtest du facteur momentum sur 10 valeurs du Dow Jones.

Principe : on se place en juillet 2025, on classe les titres sur leur momentum
12 mois (en excluant le dernier mois, convention academique), puis on mesure ce
que le top 3 et le bottom 3 ont reellement fait sur les 12 mois suivants.

Point de methode : la fenetre de signal (-25 a -14) et la fenetre d'evaluation
(-13 a -1) ne se chevauchent pas. Sans cette separation, le backtest se predirait
lui-meme (look-ahead bias).

Donnees : prix mensuels ajustes, source Yahoo Finance.
"""

import pandas as pd


def prepare(df):
    """Convertit les dates et trie chronologiquement.

    Indispensable : sans conversion, le tri se fait alphabetiquement et
    '2021-10' passerait avant '2021-2'.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date').reset_index(drop=True)


def momentum_passe(df):
    """Momentum 12 mois mesure a la date de decision (juillet 2025)."""
    df = prepare(df)
    return (df.iloc[-14]['Close'] / df.iloc[-25]['Close']) - 1


def calculate_forward_return(df):
    """Rendement realise sur les 12 mois suivant la decision."""
    df = prepare(df)
    return (df.iloc[-1]['Close'] / df.iloc[-13]['Close']) - 1


tickers = ["AAPL", "MSFT", "JPM", "JNJ", "PG", "CAT", "HD", "KO", "DIS", "CVX"]

resultats = []
for ticker in tickers:
    df = pd.read_csv(ticker + ".csv")
    score = momentum_passe(df)
    futur = calculate_forward_return(df)
    resultats.append((ticker, score, futur))

resultats.sort(key=lambda x: -x[1])

top3 = resultats[:3]
bottom3 = resultats[-3:]

rendements_top = []
for ligne in top3:
    rendements_top.append(ligne[2])
moyenne_top = sum(rendements_top) / len(rendements_top)

rendements_bottom = []
for ligne in bottom3:
    rendements_bottom.append(ligne[2])
moyenne_bottom = sum(rendements_bottom) / len(rendements_bottom)

print("TOP 3:", [ligne[0] for ligne in top3])
print("BOTTOM 3:", [ligne[0] for ligne in bottom3])
print()
print("Rendement futur moyen TOP 3:", round(moyenne_top * 100, 1), "%")
print("Rendement futur moyen BOTTOM 3:", round(moyenne_bottom * 100, 1), "%")

# RESULTAT : top 3 -8.6% / bottom 3 +18.4%. Le facteur s'est inverse.
# L'univers entier a poids egal aurait fait +18.9%.
# Aucun parametre n'a ete modifie pour obtenir un resultat positif : ce serait
# de l'overfitting. La poche n'a pas ete deployee.
