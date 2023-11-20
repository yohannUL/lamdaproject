"""
Générer un interpréteur de commande.

Returns:
    Un objet Namespace tel que retourné par parser.parse_args().
    Cet objet aura l'attribut «symboles» représentant la liste des
    symboles à traiter, et les attributs «début», «fin» et «valeur»
    associés aux arguments optionnels de la ligne de commande.
"""
import json#importation
import argparse#importation
from datetime import date, datetime#importation
import datetime#importation
import requests#importation



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
        nargs='+',
        # required="False",
        help='Nom d\'un symbole boursier',
    )
    parser.add_argument(
        "-d", "--début",
        metavar="Date",
        # action = 'store_true',
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


recuperer = analyser_commande()
symbole = recuperer.symbole
debut = recuperer.début
fin = recuperer.fin
valeur = recuperer.valeur


def produire_historique(symbole, debut, fin, valeur):
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    liste = []

    url = f'https://pax.ulaval.ca/action/{str(symbole[0])}/historique/'
    if debut is None and fin is not None:
        debut = fin
    if debut is not None and fin is None:
        fin = str(datetime.date.today())
    params = {
        'début': debut,
        'fin': fin,
    }
    table_json = requests.get(url=url, params=params)
    table_json = json.loads(table_json.text)
    historique = table_json["historique"]

    for key in historique.keys():
        liste.append((date.fromisoformat(key), historique[key][valeur]))
    liste.reverse()
    return liste


#print(produire_historique(symbole, début, fin, valeur))


# print(symbole)

def afficher():
    """
Générer un interpréteur de commande.

Returns:
    Un objet Namespace tel que retourné par parser.parse_args().
    Cet objet aura l'attribut «symboles» représentant la liste des
    symboles à traiter, et les attributs «début», «fin» et «valeur»
    associés aux arguments optionnels de la ligne de commande.
"""
    list_date = []
    for element_symbole in symbole:
        list_date.append(datetime.datetime.strptime(debut, '%Y-%m-%d').date())
        list_date.append(datetime.datetime.strptime(fin, '%Y-%m-%d').date())

        repon = ""
        repon = f"titre={element_symbole}: valeur={valeur}, début="
        repon += f"datetime.date({list_date[0].year}, {list_date[0].month}, {list_date[0].day}), "
        repon += f"fin=datetime.date({list_date[1].year}, {list_date[1].month}, {list_date[1].day})"

        histoire = produire_historique(list(element_symbole), debut, fin, valeur)
        #print(histoire)
        repon += "\n" + str(histoire)
        print(repon)

afficher()
#print(symbole)
