import argparse
import requests
import json
import datetime


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

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)
    parser.add_argument(
        'symbole',
        type = str,
        nargs = "+",
        help="Nom d'un symbole boursier",
    )
    parser.add_argument(
        "-d", "--début",
        metavar="Date",
        help=" Date recherchée la plus ancienne (format: AAAA-MM-JJ)",
    )
    parser.add_argument(
        "-f", "--fin",
        metavar="Date",
        # action = 'store_true',
        help="Date recherchée la plus récente (format: AAAA-MM-JJ)",
    )
    parser.add_argument(
        '-v', '--valeur',
        metavar='{fermeture,ouverture,min,max,volume}',
        default='fermeture',
        # action = "store_true",
        help="La valeur désirée (par défaut: fermeture)",
    )
    return parser.parse_args()


def produire_historique(nom_symbole, date_debut, date_fin, valeur):


    url = f'https://pax.ulaval.ca/action/{nom_symbole}/historique/'

    params = {
        'début': date_debut,
        'fin': date_fin,
    }

    table_json = requests.get(url=url, params=params)
    table_json = json.loads(table_json.text)

    historique = table_json["historique"]
    liste = []

    for key in historique.keys():
        liste.append(( date.fromisoformat(key), historique[key][valeur]))

    print(f"titre={nom_symbole}: valeur={valeur}, début={(date_debut)}, fin={(date_fin)}")
    print(liste)
    

analyser_commande()
produire_historique(nom_symbole = "goog", date_debut = "2019-02-22", date_fin ="2019-02-22", valeur = "volume")