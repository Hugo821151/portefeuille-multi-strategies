"""
Beta des poches et du fonds entier.

Le beta d'un portefeuille est la moyenne des betas ponderee par le capital.
Deux mesures sont publiees : le beta COURANT (exposition reellement detenue)
et le beta CIBLE (une fois toutes les poches deployees). Un gerant decrit ce
qu'il detient, pas ce qu'il a l'intention de detenir.
"""

positions = {
    "MSFT":   (1.13,  0.0929),
    "AAPL":   (1.10,  0.0929),
    "GS":     (1.29,  0.0500),
    "JNJ":    (0.23,  0.0929),
    "TTE.PA": (0.05,  0.1000),
    "SU.PA":  (1.15,  0.0929),
    "UL":     (0.45,  0.0500),
    "MC.PA":  (1.123, 0.0929),
    "AMZN":   (1.46,  0.0929),
    "NEE":    (0.67,  0.0929),
    "AI.PA":  (0.65,  0.1000),
    "PLD":    (1.34,  0.0503),
}

contributions_sp = []
for ticker, (beta, p) in positions.items():
    contributions_sp.append(beta * p)
beta_stock_picking = sum(contributions_sp)
print("beta poche stock picking:", round(beta_stock_picking, 3))

macro = {
    "VOO":    (1.000, 0.25),
    "IAU":    (0.181, 0.10),
    "TLT":    (0.512, 0.15),
    "IEUR":   (0.900, 0.10),
    "MTH.PA": (0.342, 0.30),
    "CASH":   (0.000, 0.10),
}

contributions = []
for ticker, (beta, p) in macro.items():
    contributions.append(beta * p)
beta_macro = sum(contributions)
print("beta poche macro:", round(beta_macro, 3))


def beta_du_fonds(beta_quant):
    """Beta du fonds pour une hypothese donnee sur la poche quant."""
    poches = {
        "Stock Picking": (beta_stock_picking, 0.40),
        "Macro":         (beta_macro,         0.30),
        "Quant":         (beta_quant,         0.30),
    }
    contributions_fonds = []
    for nom_poche, (beta, poids) in poches.items():
        contributions_fonds.append(beta * poids)
    return sum(contributions_fonds)


courant = beta_du_fonds(0.0)   # poche quant en cash : situation reelle
cible = beta_du_fonds(1.0)     # poche quant deployee en actions
ecart_beta = cible - courant

print()
print("beta courant:", round(courant, 3))
print("beta cible:", round(cible, 3))
print("risque de marche non encore pris:", round(ecart_beta, 3))

# Traduction en euros : ce que le beta signifie concretement
capital = 1000000
choc = -0.10
perte_courante = courant * choc * capital
perte_cible = cible * choc * capital
print()
print("si le marche baisse de 10%:")
print("  perte fonds courant:", round(perte_courante, 0), "EUR")
print("  perte fonds cible:  ", round(perte_cible, 0), "EUR")
