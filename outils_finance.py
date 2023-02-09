""" Outils de calculs financier
Auteur : Mariano MASCELLINO

Ce module propose une série de fonctions permettant de réaliser des simulations de stratégies financières

Liste des fonctions proposées pour le calcul et l'affichage des intérêts composés :
 - calculer_interets_composes
 - afficher_graphique_simulation_interets_composes
 - afficher_rapport_simulation_interets_composes

Liste des fonctions proposées pour le calcul et l'affichage des crédits:
 - simuler_credit
 - afficher_rapport_simulation_credit
 - afficher_graphique_simulation_credit
 
 Liste des fonction proposées pour la comparaison de stratégies :
 - comparer_strategies_selon_rentabilite_et_credit
 - comparer_strategies_selon_rentabilite_inflation_credit
 - evaluer_strategies

 Fonction pour le calcul de l'inflation
 - correcteur_inflation
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def calculer_interets_composes(
    taux_rentabilite_annuel: float,
    capital_initial: float,
    apports_mensuels: float,
    duree_de_simulation_mois: int,
    taux_inflation_annuel: float = 0.0,
):
    """
    Calcule l'évolution du capital en prenant en compte les intérêts composés et l'inflation.
    Paramètres :
    - le taux de rentabilité annuel
    - le capital initial investi
    - l'apports mensuel
    - la durée de simulation en mois
    - le taux d'inflation annuel (facultatif)

    La fonction retournera :
    - array : évolution du capital
    - array : évolution des intérêts générés
    - array : numérotation des mois
    - array : les apports mensuels ramenée en valeur d'aujourd'hui corrigée de l'inflation future
    - retourne la perte en capital (capital initial + apports mensuels) liée à l'inflation
    """

    taux_rentabilite_mensuel = (1 + taux_rentabilite_annuel) ** (1 / float(12)) - 1
    coefficient_inflation_mensuel = float(
        (1 + taux_inflation_annuel) ** (1 / float(12))
    )

    interets_mensuels_cumules = []
    apports_mensuels_monnaie_actuelle = []
    capitals_mensuels = []
    labels_mois = []

    for mois in range(duree_de_simulation_mois):
        # l'apport mensuel se déprécie par rapport à l'inflation
        apports_mensuels = apports_mensuels / coefficient_inflation_mensuel
        apports_mensuels_monnaie_actuelle.append(apports_mensuels)
        if mois != 0:
            interets_du_mois_en_cours = (
                capitals_mensuels[-1] + interets_mensuels_cumules[-1]
            ) * taux_rentabilite_mensuel
            interets_mensuels_cumules.append(
                (interets_mensuels_cumules[-1] + interets_du_mois_en_cours)
                / coefficient_inflation_mensuel
            )
            capitals_mensuels.append(
                capitals_mensuels[-1] / coefficient_inflation_mensuel + apports_mensuels
            )
            labels_mois.append(mois)
        else:
            capitals_mensuels.append(
                capital_initial / coefficient_inflation_mensuel + apports_mensuels
            )
            labels_mois.append(0)
            interets_mensuels_cumules.append(0)

    # variation capital = ce qu'il nous reste en monnaie actuelle - l'effort fourni en monnaie actuelle
    # variation capital = (capital final en monnaie actuelle) - (capital initial + apports cumulés en monnaie actuelle)
    variation_capital = capitals_mensuels[-1] - (
        capital_initial + sum(apports_mensuels_monnaie_actuelle)
    )
    return (
        capitals_mensuels,
        interets_mensuels_cumules,
        labels_mois,
        apports_mensuels_monnaie_actuelle,
        variation_capital,
    )


def afficher_graphique_simulation_interets_composes(
    capitals_mensuels,
    interets_mensuels_cumules,
    labels_mois,
    taux_rentabilite_annuel,
    taux_inflation_annuel: float = 0.0,
):
    """
    Affiche sous forme d'histogramme (barres empilées), l'évolution du capital
    et des intérêts, générés par la fonction calculer_interets_composes()

    Paramètres :
     - liste des valeurs de capitals par mois
     - liste des intérêts cumulés par mois
     - liste des labels de mois
     - taux de rentabilité annuel
     - le taux d'inflation (optionnel)
    """

    width = 0.5  # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()

    ax.bar(labels_mois, capitals_mensuels, width, yerr=0, label="Capital")
    ax.bar(
        labels_mois,
        interets_mensuels_cumules,
        width,
        yerr=0,
        bottom=capitals_mensuels,
        label="Intérêts",
    )

    ax.set_ylabel("Montants")
    ax.set_xlabel("Durée (en mois)")
    ax.set_title(
        "Évolution du capital et des intérêts au cours du temps pour un taux d'intérêt"
        f" annuel de {taux_rentabilite_annuel*100}% et un taux d'inflation de"
        f" {taux_inflation_annuel*100}%"
    )
    ax.legend()

    plt.show()


# ### Rapport d'intérêts composés : afficher_rapport_simulation_interets_composes()
#


def afficher_rapport_simulation_interets_composes(
    capital_initial: int,
    capitals_mensuels: list[int],
    interets_mensuels_cumules: list[float],
    labels_mois: list[int],
    taux_rentabilite_annuel: float,
    mensualites: int,
    apports_mensuels_monnaie_actuelle: list[float],
    variation_capital: float,
    taux_inflation_annuel: float = 0,
):
    """
    Imprime un rapport sur les principaux paramètres d'intérêts composés sur une période
    calculés par la fonction calculer_interets_composes

    Paramètres :
    - liste des valeurs de capitals par mois
    - liste des intérêts cumulés par mois
    - liste des labels de mois
    - taux de rentabilité annuel
    - les mensualités définies
    - le taux d'inflation (optionnel)
    """
    print(f"Capital initial :{capital_initial}")

    print(f"Taux de rentabilité annuelle moyen : {taux_rentabilite_annuel*100:.2f}%")
    print(f"Taux d'inflation annuel moyen : {taux_inflation_annuel*100:.2f}%")

    cumul_apports = capitals_mensuels[-1]
    print(f"Capital (dont capital initial) en monnaie actuelle : {cumul_apports:.2f}")
    print(
        "Apports cumulés en monnaie actuelle :"
        f" {sum(apports_mensuels_monnaie_actuelle)}"
    )
    print(
        "Apports cumulés sans correction de l'inflation :"
        f" {(capital_initial + mensualites*len(labels_mois)):.2f}"
    )

    print(f"variation du capital (apports mensuels compris) : {variation_capital:.2f}")

    interets_cumules = interets_mensuels_cumules[-1]
    print(f"Intérets cumulés : {interets_cumules:.2f}")

    interets_dernier_mois = (
        interets_mensuels_cumules[-1] - interets_mensuels_cumules[-2]
    )
    print(f"Intérets générés le dernier mois : {interets_dernier_mois:.2f}")

    print(
        "Montant final (en monnaire d'aujourd'hui) :"
        f" {(capitals_mensuels[-1]+interets_mensuels_cumules[-1]):.2f}"
    )


def simuler_credit(
    montant_emprunte_total: float,
    nombre_mensualites: int,
    taux_annuel: float,
    taux_inflation_annuel: float = 0,
):
    """
    Simule un crédit et rapporte les mensualités et les intérêts en valeur
    actuelle si une valeur d'inflation est précisée

    Paramètres :
    - Montant du crédit emprunté
    - Nombre de mensualités du crédit
    - Taux annuel global du crédit

    Retourne :
    - Mensualités du crédit
    - Coût total du crédit
    - array : capital remboursé à chaque mois
    - array : capital restant pour le mois en cours (après le remboursement pour le mois en cours)
    - array : intérêts remboursés à chaque mois
    - array : numérotation des mois 
    note : l'index 0 correspond au montant initial du crédit moins le premier remboursement
    qui est effectué par convention dès le J0 du crédit
    """

    mensualite = 0
    cout_total_interets = 0
    capital_rembourse_par_mois = [0]
    capital_restant_par_mois = [montant_emprunte_total]
    interets_mensuels = [0]
    labels_mois = [0]

    taux_mensuel = (1 + taux_annuel) ** (1 / float(12)) - 1
    coefficient_inflation_mensuel = float(
        (1 + taux_inflation_annuel) ** (1 / float(12))
    )
    premiere_mensualite = mensualite = (
        montant_emprunte_total * taux_mensuel * (1 + taux_mensuel) ** nombre_mensualites
    ) / ((1 + taux_mensuel) ** nombre_mensualites - 1)

    # avec l'inflation les mensualités et le capital restant diminues chaque mois
    cout_total_interets = 0  # mensualite*nombre_mensualites-montant_emprunte_total

    for mois in range(nombre_mensualites):
        # mensualite = mensualite/coefficient_inflation_mensuel
        mensualite = (
            capital_restant_par_mois[-1]
            * taux_mensuel
            * (1 + taux_mensuel) ** (nombre_mensualites - mois)
            / ((1 + taux_mensuel) ** (nombre_mensualites - mois) - 1)
        )
        interet_du_mois = (
            capital_restant_par_mois[-1] * taux_mensuel / coefficient_inflation_mensuel
        )

        cout_total_interets += interet_du_mois
        capital_rembourse_du_mois = mensualite - interet_du_mois

        interets_mensuels.append(interet_du_mois)
        capital_rembourse_par_mois.append(capital_rembourse_du_mois)
        capital_restant_par_mois.append(
            capital_restant_par_mois[-1] / coefficient_inflation_mensuel
            - capital_rembourse_du_mois
        )

        labels_mois.append(mois)

    # on supprime le premier item de chaque tableau qui sert juste à initier les calculs
    capital_rembourse_par_mois.pop(0)
    capital_restant_par_mois.pop(0)
    interets_mensuels.pop(0)
    labels_mois.pop(0)

    return (
        premiere_mensualite,
        cout_total_interets,
        capital_rembourse_par_mois,
        capital_restant_par_mois,
        interets_mensuels,
        labels_mois,
    )


def afficher_rapport_simulation_credit(
    montant_emprunte_total: int,
    nombre_mensualites: int,
    taux_annuel: float,
    mensualite: int,
    cout_total_interets: float,
    taux_annuel_inflation: float = 0,
):
    """
    Affiche un rapport détaillant les caractériques d'un crédit simulé par la
    fonction simuler_credit()
    """
    print(f"Capital emprunté : {montant_emprunte_total}")
    print(f"Nombre de mensualités : {nombre_mensualites}")
    print(f"Taux d'intérêts annuel : {taux_annuel*100:.2f}%")
    print(f"Taux d'inflation annuel : {taux_annuel_inflation*100:.2f}%")
    print(f"Mensualités du crédit : {mensualite:.2f}")
    print(f"Cout total des intérêts du crédit : {cout_total_interets:.2f}")
    print(f"Capital + intérêts = {(cout_total_interets+montant_emprunte_total):.2f}")


def afficher_graphique_simulation_credit(
    capital_rembourse_par_mois: list[float],
    capital_restant_par_mois: list[float],
    interets_mensuels: list[float],
    labels_mois: list[int],
):
    """
    Affiche un graphique sous forme d'histogramme de barres empilées représentant
    une simulation de crédit retourné par simuler_credit()
    """
    width = 0.5
    fig, ax = plt.subplots()

    ax.bar(
        labels_mois,
        capital_rembourse_par_mois,
        width,
        yerr=0,
        label="Capital remboursé",
    )
    ax.bar(
        labels_mois,
        interets_mensuels,
        width,
        yerr=0,
        bottom=capital_rembourse_par_mois,
        label="Intérêts payés",
    )

    ax.twinx().plot(
        labels_mois, capital_restant_par_mois, label="Capital restant à rembourser"
    )

    ax.set_ylabel("")
    ax.set_xlabel("Durée (en mois)")
    ax.set_title("Remboursement du crédit : part du capital et des intérêts")
    ax.legend()

    plt.show()


def calculer_capital(mensualite: float, taux_annuel: float, duree_en_mois: int):
    """
    Retourne le capital disponible pour un crédit à taux fixe à partir :
    -d'une mensulaté fixe
    -un taux annuel
    -la durée du crédit
    """
    taux_mensuel = (1 + taux_annuel) ** (1 / float(12)) - 1
    capital = (
        mensualite * (1 - (1 + taux_mensuel) ** (-1 * duree_en_mois)) / taux_mensuel
    )

    return capital


def correcteur_inflation(taux_annuel: float, duree_de_simulation_en_annees: int):
    """
    Permet de corriger un montant futur de l'inflation future pour le ramener
    en valeur acutelle.
    Retourne un tableaux de coefficients, selon le mois.
    """
    coefficients = [1]
    labels_mois = [0]

    coefficient_inflation_mensuel = 2 - (1 + taux_annuel) ** (1 / float(12))

    for annee in range(duree_de_simulation_en_annees):
        for mois in range(12):
            if annee != 0 or mois != 0:
                coefficients.append(coefficients[-1] * coefficient_inflation_mensuel)
                labels_mois.append(annee * 12 + mois)

    return coefficients, labels_mois


# %% [markdown]
# # Comparateur de scenarii : evaluer_strategies()
#


# %%
def evaluer_strategies(
    mensualites: float,
    duree_de_simulation: int,
    taux_de_rentabilite_annuel_placement: float,
    taux_annuel_general_credit: float,
    afficher: bool,
    taux_annuel_inflation: float = 0,
):
    """
    Compare deux différents scénarii selon des paramètres donnés

    Le scénario 1 :
    - L'argent est placé régulièrement sur une enveloppe financière sur une DURÉE déterminée
    - L'enveloppe rapporte un TAUX D'INTÉRÊTS ANNUEL
    - Une MENSUALITE fixe est versée chaque mois
    ==> la fonction calcule les intérêts générés sur la DURÉE

    Le scénario 2 :
    - Un CAPITAL est défini par la valeur actuelle correspondant à un crédit de MENSUALITÉ, le TAUX GENERAL D'EMPRUNT et de DURÉE
    - Ce CAPITAL est investi au début de la même période que le scénario 1
    ==>la fonction calcule :
    - les intérêts générés sur la DUREE
    - le cout du crédit associé

    On demande en entrée :
    - les mensualités
    - durée de la simulation en mois
    - taux de rentabilité annuel de la bourse
    - taux général d'emprunt
    - un booléen pour afficher en option, un rapport détaillé
    - le taux annuel d'inflation (optionnel)

    Retourne :
    - le CAPITAL emprunté dans la stratégie 2
    - benefice net de la stratégie 1 = les intérêts mensuels générés dans la stratégie 1 - la perte en capital liée à l'inflation
    - benefice net de la stratégie 2 = les intérêts mensuels générés dans la stratégie 2 - (cout du crédit + la perte en capital liée à l'inflation)
    """
    # étape 1
    (
        capitals_mensuels_strat1,
        interets_mensuels_cumules_strat1,
        labels_mois_strat1,
        apport_mensuels_monnaie_actuelle_strat1,
        variation_capital_strat1,
    ) = calculer_interets_composes(
        taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
        capital_initial=0,
        apports_mensuels=mensualites,
        duree_de_simulation_mois=duree_de_simulation,
        taux_inflation_annuel=taux_annuel_inflation,
    )

    # etape 2
    capital = calculer_capital(
        mensualite=mensualites,
        taux_annuel=taux_annuel_general_credit,
        duree_en_mois=duree_de_simulation,
    )

    # etape 3
    (
        mensualite,
        cout_total_interets,
        capital_rembourse_par_mois,
        capital_restant_par_mois,
        interets_mensuels,
        labels_mois,
    ) = simuler_credit(
        montant_emprunte_total=capital,
        nombre_mensualites=duree_de_simulation,
        taux_annuel=taux_annuel_general_credit,
        taux_inflation_annuel=taux_annuel_inflation,
    )

    # etape 4
    (
        capitals_mensuels_strat2,
        interets_mensuels_cumules_strat2,
        labels_mois_strat2,
        apport_mensuels_monnaie_actuelle_strat2,
        variation_capital_strat2,
    ) = calculer_interets_composes(
        taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
        capital_initial=capital,  # capital calculé à l'étape 2
        apports_mensuels=0,
        duree_de_simulation_mois=duree_de_simulation,
        taux_inflation_annuel=taux_annuel_inflation,
    )

    # on calcule les différences
    benefice_net_strat1 = (
        interets_mensuels_cumules_strat1[-1] + variation_capital_strat1
    )
    benefice_net_strat2 = (
        interets_mensuels_cumules_strat2[-1]
        - cout_total_interets
        + variation_capital_strat2
    )

    if afficher:
        # étape 5
        # on décrit la stratégie classique (strat1)
        print("-------------------------")
        print(
            "Simulations pour un taux d'inflation de"
            f" {(taux_annuel_inflation*100):.2f}%"
        )
        print(
            f"STRATEGIE CONSISTANT À PLACER RÉGULIÈREMENT {mensualites} tous les mois à"
            f" {taux_de_rentabilite_annuel_placement*100:.2f}%"
        )
        afficher_graphique_simulation_interets_composes(
            capitals_mensuels=capitals_mensuels_strat1,
            interets_mensuels_cumules=interets_mensuels_cumules_strat1,
            labels_mois=labels_mois_strat1,
            taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
            taux_inflation_annuel=taux_annuel_inflation,
        )

        afficher_rapport_simulation_interets_composes(
            capitals_mensuels=capitals_mensuels_strat1,
            interets_mensuels_cumules=interets_mensuels_cumules_strat1,
            labels_mois=labels_mois_strat1,
            taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
            capital_initial=capital,
            mensualites=mensualites,
            taux_inflation_annuel=taux_annuel_inflation,
            apports_mensuels_monnaie_actuelle=apport_mensuels_monnaie_actuelle_strat1,
            variation_capital=variation_capital_strat1,
        )

        # on décrit les modalités de l'emprunt
        print("")
        print("STRATÉGIE CONSISTANT À PLACER L'ARGENT DU CRÉDIT")
        print("Modalités du crédit")

        afficher_rapport_simulation_credit(
            montant_emprunte_total=capital,
            nombre_mensualites=duree_de_simulation,
            taux_annuel=taux_annuel_general_credit,
            mensualite=mensualite,  # on affiche la valeur retournée par la simulation pour s'assurer qu'elle est conforme à la mensualité définie au départ
            cout_total_interets=cout_total_interets,
        )

        afficher_graphique_simulation_credit(
            capital_rembourse_par_mois=capital_rembourse_par_mois,
            capital_restant_par_mois=capital_restant_par_mois,
            interets_mensuels=interets_mensuels,
            labels_mois=labels_mois,
        )

        # on décrit les modalités de la simulation investissment en bolus initial
        print(
            "STRATEGIE CONSISTANT À PLACER RÉGULIÈREMENT UNE SEULE FOIS"
            f" {capitals_mensuels_strat2[0]} à"
            f" {taux_de_rentabilite_annuel_placement*100:.2f}%"
        )
        afficher_graphique_simulation_interets_composes(
            capitals_mensuels=capitals_mensuels_strat2,
            interets_mensuels_cumules=interets_mensuels_cumules_strat2,
            labels_mois=labels_mois_strat2,
            taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
            taux_inflation_annuel=taux_annuel_inflation,
        )

        afficher_rapport_simulation_interets_composes(
            capitals_mensuels=capitals_mensuels_strat2,
            interets_mensuels_cumules=interets_mensuels_cumules_strat2,
            labels_mois=labels_mois_strat2,
            taux_rentabilite_annuel=taux_de_rentabilite_annuel_placement,
            capital_initial=capital,
            mensualites=0,
            taux_inflation_annuel=taux_annuel_inflation,
            apports_mensuels_monnaie_actuelle=apport_mensuels_monnaie_actuelle_strat1,
            variation_capital=variation_capital_strat2,
        )

        # On rédige la synthèse des stratégies

        print("")
        print("Thomas Messias (SYNTHÈSE) de l'opération :")
        print(
            f"Stratégie 1 : Placement de {mensualites} à"
            f" {taux_de_rentabilite_annuel_placement*100:.2f}%/an pendant"
            f" {duree_de_simulation/12} ans sans apport initial."
        )
        print(
            f"Stratégie 2 : Placement d'un capital de {capital:.2f} à"
            f" {taux_de_rentabilite_annuel_placement*100:.2f}%/an pendant"
            f" {duree_de_simulation/12} ans provenant d'un crédit sur la même période à"
            f" {taux_annuel_general_credit*100}%/an d'intérêt."
        )

        print(
            "Intérêts générés par la startégie 1 :"
            f" {interets_mensuels_cumules_strat1[-1]:.2f}"
        )
        print(
            "Intérêts générés par la stratégie 2 :"
            f" {interets_mensuels_cumules_strat2[-1]:.2f}"
        )

        print(
            "Variation en capital causées par l'inflation de la stratégie 1 :"
            f" {variation_capital_strat1:.2f}"
        )
        print(
            "Variation en capital causées par l'inflation de la stratégie 1 :"
            f" {variation_capital_strat2:.2f}"
        )

        print(f"Coût du crédit, lié à la stratégie 1 : 0 ==> pas de crédit")
        print(f"Coût du crédit, lié à la stratégie 2 : {cout_total_interets:.2f}")

        print(f"Bénéfice net de la stratégie 1 : {(benefice_net_strat1):.2f}")
        print(f"Bénéfice net de la stratégie 2 : {(benefice_net_strat2):.2f}")
        print(
            "Avantage de la startégie 2 sur la stratégie 1:"
            f" {(benefice_net_strat2-benefice_net_strat1):.2f}"
        )

    return (capital, benefice_net_strat1, benefice_net_strat2)


def comparer_strategies_selon_rentabilite_et_credit(
    mensualite: int,
    duree_de_simulation: int,
    liste_taux_de_rentatibilite_annuel_placement: list[float],
    liste_taux_general_credit: list[float],
    taux_inflation_annuel: float = 0,
):
    """
    Compare deux stratégies en faisant varier les paramètres de rentabilité
    annuelle du placement ainsi que le taux du crédit

    Stratégie 1 : placement régulier sans emprunt
    Stratégie 2 : placement d'un capital obtenu par emprunt

    Retourne :
    -l'avantage de la stratégie 2 sur la stratégie 1
    -le bénéfice de la stratégie 1 (placement régulier sans emprunt)
    -le bénéfice net de la stratégie 2
    """
    avantage_strat2 = []
    benefices_nets_strat2 = (
        []
    )  # représente les intérêts générés par la strat2-le cout du crédit
    benefices_strat1 = []

    for taux_rentabilite_annuel in liste_taux_de_rentatibilite_annuel_placement:
        avantage_strat2_a_rentabilite_constante = []
        benef_net_strat2_a_rentabilite_constante = []
        benef_strat1_a_rentabilite_constante = []
        for taux_general_credit in liste_taux_general_credit:
            (capital_emprunte_strat2, benef_strat1, benef_strat2) = evaluer_strategies(
                mensualites=mensualite,
                duree_de_simulation=duree_de_simulation,
                taux_de_rentabilite_annuel_placement=taux_rentabilite_annuel,
                taux_annuel_general_credit=taux_general_credit,
                taux_annuel_inflation=taux_inflation_annuel,
                afficher=False,
            )
            avantage_strat2_a_rentabilite_constante.append(
                int(benef_strat2 - benef_strat1)
            )
            benef_net_strat2_a_rentabilite_constante.append(int(benef_strat2))
            benef_strat1_a_rentabilite_constante.append(int(benef_strat1))
        avantage_strat2.append(avantage_strat2_a_rentabilite_constante)
        benefices_nets_strat2.append(benef_net_strat2_a_rentabilite_constante)
        benefices_strat1.append(benef_strat1_a_rentabilite_constante)

    return avantage_strat2, benefices_nets_strat2, benefices_strat1


def afficher_graphique_comparaison_strategies_selon_rentabilite_et_credit(
    duree_de_simulation: int,
    mensualites: int,
    benefices_strat1: list[float],
    benefices_nets_strat2: list[float],
    avantage_strat2: list[float],
    taux_general_credit: list[float],
    taux_rentabilite_annuel_placement: list[float],
    titre_figure: str,
):
    """
    Afficheur de comparateur de stratégies explorant différents scénarios avec
    différentes taux de rentabilités et différents taux de crédit.
    """
    epargne_totale = duree_de_simulation * mensualites

    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "custom", ["royalblue", "orange", "darkred"]
    )

    max = np.max(
        [
            np.max(benefices_strat1),
            np.max(benefices_nets_strat2),
            np.max(avantage_strat2),
        ]
    )
    min = np.min(
        [
            np.min(benefices_strat1),
            np.min(benefices_nets_strat2),
            np.min(avantage_strat2),
        ]
    )

    fig, ax = plt.subplots(1, 3, sharey=False)

    # on ajoute les légendes et le contenu
    fig.suptitle(titre_figure)
    fig.supxlabel(f"Effort total : {epargne_totale}")

    ax[0].set_title("Bénéfices strat1 (en k)")
    ax[0].imshow(benefices_strat1, vmin=min, vmax=max, cmap=cmap)

    ax[1].set_title("Bénéfices strat2 (en k)")
    ax[1].imshow(benefices_nets_strat2, vmin=min, vmax=max, cmap=cmap)

    ax[2].set_title("Avantage strat2 (en k)")
    ax[2].imshow(avantage_strat2, vmin=min, vmax=max, cmap=cmap)

    # on redimensionne le graphique
    largeur = 3 * len(taux_general_credit) * 0.5 + 5
    hauteur = len(taux_rentabilite_annuel_placement) * 0.6 + 3
    ax[0].figure.set_size_inches(largeur, hauteur)

    # on ajoute les labels en abscisse
    for a in ax:
        a.set_xlabel("Taux d'emprunt (%)")
        ax[0].set_ylabel("Taux de rendement (%)")

    # on configure les axes x et y de chaque graphique
    for a in ax:
        a.get_xaxis().set_ticks(range(len(taux_general_credit)))
        a.get_xaxis().set_ticklabels(np.array(taux_general_credit) * 100)
        a.get_yaxis().set_ticks(range(len(taux_rentabilite_annuel_placement)))
        a.get_yaxis().set_ticklabels(np.array(taux_rentabilite_annuel_placement) * 100)
        a.invert_yaxis()

    # annotations dans chaque case (x3)
    for i in range(len(taux_rentabilite_annuel_placement)):
        for j in range(len(taux_general_credit)):
            text = ax[0].text(
                j,
                i,
                int(benefices_strat1[i][j] / 1000),
                ha="center",
                va="center",
                color="w",
            )

    for i in range(len(taux_rentabilite_annuel_placement)):
        for j in range(len(taux_general_credit)):
            text = ax[1].text(
                j,
                i,
                int(benefices_nets_strat2[i][j] / 1000),
                ha="center",
                va="center",
                color="w",
            )

    for i in range(len(taux_rentabilite_annuel_placement)):
        for j in range(len(taux_general_credit)):
            text = ax[2].text(
                j,
                i,
                int(avantage_strat2[i][j] / 1000),
                ha="center",
                va="center",
                color="w",
            )

    plt.show()


def comparer_strategies_selon_rentabilite_inflation_credit(
    mensualites: float,
    duree_simulation: int,  # mois
    taux_general_credit: list[float],
    taux_rentabilite_annuel: list[float],
    taux_inflation_annuel: list[float],
):
    """
    Compare deux stratégies en faisant varier les paramètres de rentabilité
    annuelle du placement, le taux du crédit ainsi que l'inflation annuelle

    Stratégie 1 : placement régulier sans emprunt
    Stratégie 2 : placement d'un capital obtenu par emprunt

    Affiche une série de tableaux
    """
    for inflation in taux_inflation_annuel:
        (
            avantage_strat2,
            benefices_nets_strat2,
            benefices_strat1,
        ) = comparer_strategies_selon_rentabilite_et_credit(
            mensualite=mensualites,
            duree_de_simulation=duree_simulation,
            liste_taux_de_rentatibilite_annuel_placement=taux_rentabilite_annuel,
            liste_taux_general_credit=taux_general_credit,
            taux_inflation_annuel=inflation,
        )

        afficher_graphique_comparaison_strategies_selon_rentabilite_et_credit(
            duree_de_simulation=duree_simulation,
            mensualites=mensualites,
            benefices_strat1=benefices_strat1,
            benefices_nets_strat2=benefices_nets_strat2,
            avantage_strat2=avantage_strat2,
            taux_rentabilite_annuel_placement=taux_rentabilite_annuel,
            taux_general_credit=taux_general_credit,
            titre_figure=(
                f"Apport mensuel de {mensualites} sur {duree_simulation/12} ans avec"
                f" une inflation de {inflation*100} %"
            ),
        )
