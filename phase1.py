"""Module pour l'extraction des valeurs boursières historiques."""

import argparse
import datetime
import json
import requests


def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers."
    )

    parser.add_argument(
        'symbole',
        type=str,
        nargs="+",
        help="Nom d'un symbole boursier",
    )
    parser.add_argument(
        "-d", "--début",
        metavar="DATE",
        help=" Date recherchée la plus ancienne (format: AAAA-MM-JJ)",
    )
    parser.add_argument(
        "-f", "--fin",
        metavar="DATE",
        help="Date recherchée la plus récente (format: AAAA-MM-JJ)",
    )
    parser.add_argument(
        '-v', '--valeur',
        default='fermeture',
        type=str,
        choices=["fermeture", "ouverture", "min,max", "volume"],
        help="La valeur désirée (par défaut: fermeture)",
    )
    return parser.parse_args()


def produire_historique():
    """
    Afficher les valeurs boursières et leurs dates en fonction des valeurs demandées.

    Returns:
        Notre module produit le titre de l'action, la valeur, la date de début et la date de fin et
        ensuite retourne une liste de la date puis de la valeur de cette action à la date donnée.
    """
    list_date = []
    get_parameters = analyser_commande()

    reponse_finale = ""
    for symbole in get_parameters.symbole:

        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
        if get_parameters.début is None and get_parameters.fin is not None:
            get_parameters.début = get_parameters.fin
        if get_parameters.début is not None and get_parameters.fin is None:
            get_parameters.fin = str(datetime.date.today())
        list_date.append(datetime.datetime.strptime(get_parameters.début, '%Y-%m-%d').date())
        list_date.append(datetime.datetime.strptime(get_parameters.fin, '%Y-%m-%d').date())

        params = {
            'début': get_parameters.début,
            'fin': get_parameters.fin,
        }
        liste_réponse = requests.get(url=url, params=params, timeout=60)
        liste_réponse = json.loads(liste_réponse.text)
        liste = []
        for key in liste_réponse['historique'].keys():
            liste.append((datetime.datetime.strptime(key, '%Y-%m-%d').date(),
                          liste_réponse['historique'][key][get_parameters.valeur]))
        reponse = f"titre={symbole}: valeur={get_parameters.valeur}, début="
        reponse += f"datetime.date({list_date[0].year}, {list_date[0].month}, {list_date[0].day}), "
        reponse += f"fin=datetime.date({list_date[1].year}, {list_date[1].month}, {list_date[1].day})"
        liste.reverse()
        reponse += "\n" + str(liste)
        reponse_finale += "\n" + reponse
    return reponse_finale

reponse = produire_historique()
print(reponse)