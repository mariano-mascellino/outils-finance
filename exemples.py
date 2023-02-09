"""
Ce fichier est un exemple d'application du module outils_finance.py
AUTEUR : Mariano MASCELLINO
"""


import outils_finance as of


"""
Exemple 1 : 
Je place une somme fixe en bourse 
Je veux savoir combien les intérêts me rapportent au bout d'une certaine durée
"""

CAPITAL = 10000  # capital initial de 10000
APPORTS_MENSUELS = 0  # apports mensuels de 1000 par mois
DUREE_EN_MOIS = 10 * 12  # 12 ans soit 120 mois
TAUX_RENTABILITE_ANNUEL = 0.06  # rentabilité du placement à 6% par an
TAUX_INFLATION_ANNUEL = 0.01  # inflation de la monnaie à 1% par an

(
    evolution_mensuelle_capital,
    evolution_mensuelle_interets,
    liste_des_mois,
    apports_mensuels_en_valeur_actuelle_corrigee_inflation_future,
    perte_en_capital_liee_a_l_inflation,
) = of.calculer_interets_composes(
    taux_rentabilite_annuel=TAUX_RENTABILITE_ANNUEL,
    capital_initial=CAPITAL,
    apports_mensuels=APPORTS_MENSUELS,
    duree_de_simulation_mois=DUREE_EN_MOIS,
    taux_inflation_annuel=TAUX_INFLATION_ANNUEL,
)

# affichage du rapport écrit de la simulation
of.afficher_rapport_simulation_interets_composes(
    capital_initial=CAPITAL,
    capitals_mensuels=evolution_mensuelle_capital,
    interets_mensuels_cumules=evolution_mensuelle_interets,
    labels_mois=liste_des_mois,
    taux_rentabilite_annuel=TAUX_RENTABILITE_ANNUEL,
    mensualites=APPORTS_MENSUELS,
    apports_mensuels_monnaie_actuelle=apports_mensuels_en_valeur_actuelle_corrigee_inflation_future,
    variation_capital=perte_en_capital_liee_a_l_inflation,
    taux_inflation_annuel=TAUX_INFLATION_ANNUEL,
)

# affichage du rapport graphique de la simulation
of.afficher_graphique_simulation_interets_composes(
    capitals_mensuels=evolution_mensuelle_capital,
    interets_mensuels_cumules=evolution_mensuelle_interets,
    labels_mois=liste_des_mois,
    taux_rentabilite_annuel=TAUX_RENTABILITE_ANNUEL,
    taux_inflation_annuel=TAUX_INFLATION_ANNUEL,
)


"""
Exemple 2 : 
Je veux calculer les mensualités d'un crédit
"""

MONTANT_EMPRUNTE = 100000
NOMBRE_DE_MENSUALITES = 12 * 10  # 10 ans soit 120 mois
TAUX_GENERAL_CREDIT = 0.03  # crédit à 3% par an
TAUX_INFLATION_ANNUEL = 0.0  # 0% d'inflation

(
    mensualites,
    cout_total_credit,
    capital_rembourse_par_mois,
    capital_restant_a_rembourser_par_mois,
    interets_payes_chaque_mois,
    liste_des_mois,
) = of.simuler_credit(
    montant_emprunte_total=MONTANT_EMPRUNTE,
    nombre_mensualites=NOMBRE_DE_MENSUALITES,
    taux_annuel=TAUX_GENERAL_CREDIT,
    taux_inflation_annuel=TAUX_INFLATION_ANNUEL,
)

of.afficher_rapport_simulation_credit(
    montant_emprunte_total=MONTANT_EMPRUNTE,
    nombre_mensualites=NOMBRE_DE_MENSUALITES,
    taux_annuel=TAUX_GENERAL_CREDIT,
    mensualite=mensualites,
    cout_total_interets=sum(interets_payes_chaque_mois),
    taux_annuel_inflation=TAUX_INFLATION_ANNUEL,
)

of.afficher_graphique_simulation_credit(
    capital_rembourse_par_mois=capital_rembourse_par_mois,
    capital_restant_par_mois=capital_restant_a_rembourser_par_mois,
    interets_mensuels=interets_payes_chaque_mois,
    labels_mois=liste_des_mois,
)


"""
Exemple 3 : 
Je connaitre capital empruntable pour un crédit
"""

MENSUALITES_DU_CREDIT = 1000
TAUX_ANNUEL_CREDIT = 0.05
DUREE_EN_MOIS_DU_CREDIT = 12 * 10

capital = of.calculer_capital(
    mensualite=MENSUALITES_DU_CREDIT,
    taux_annuel=TAUX_ANNUEL_CREDIT,
    duree_en_mois=DUREE_EN_MOIS_DU_CREDIT,
)

print(f"Vous pouvez emprunter {capital:.2f}.")


"""
Exemple 4 : 
Je souhaite comparer deux stratégies de placement
Stratégie 1 : je place chaque mois un montant fixe
Stratégie 2 : je place en une fois un montant que j'ai emprunté
La comparaison fait varier les différents paramètres de rentabilité,
de taux d'intérêts du crédit et d'inflation
"""

# Effort d'épargne
MENSUALITES = 1000
DUREE_DE_SIMULATION_EN_MOIS = 10 * 12

# paramètres explorés
TAUX_DE_RENTABILITE_ANNUEL = [0.0, 0.03, 0.05, 0.08, 0.1]
TAUX_GENERAL_CREDIT = [0.001, 0.01, 0.02, 0.03, 0.04, 0.05]
TAUX_INFLATION_ANNUEL = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1]

of.comparer_strategies_selon_rentabilite_inflation_credit(
    mensualites=MENSUALITES,
    duree_simulation=DUREE_DE_SIMULATION_EN_MOIS,
    taux_general_credit=TAUX_GENERAL_CREDIT,
    taux_rentabilite_annuel=TAUX_DE_RENTABILITE_ANNUEL,
    taux_inflation_annuel=TAUX_INFLATION_ANNUEL,
)
