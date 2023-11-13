"""Importation de librairie pour le module d'affichage des valeurs boursiers."""
import json
import argparse
import datetime
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

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)
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
    affichage des valeurs boursiers.

    Returns:
        notre module produit le titre de l'action la valeur la date de debut et la date de fin et
         ensuite retourne un liste de la date puis de la valeur de cette action a la dte donner

        exemple 1:
            python phase1.py -d=2019-02-18 -f=2019-02-24 goog
            titre=goog: valeur=fermeture, début=datetime.date(2019, 2, 18), fin=
            datetime.date(2019, 2, 24)
            [(datetime.date(2019, 2, 19), 1118.56), (datetime.date(2019, 2, 20), 1113.8),
            (datetime.date(2019, 2, 21), 1096.97), (datetime.date(2019, 2, 22), 1110.37)]

        exemple 2:
            python phase1.py -v=volume -f=2019-02-22 goog
            titre=goog: valeur=volume, début=datetime.date(2019, 2, 22),
            fin=datetime.date(2019, 2, 22) [(datetime.date(2019, 2, 22),
            1049545)]

    """
    list_date=[]
    get_parameters=analyser_commande()

    reponse_finale= ""
    for elemnt_symbole in get_parameters.symbole:

        url = f'https://pax.ulaval.ca/action/{elemnt_symbole}/historique/'
        if get_parameters.début is None and get_parameters.fin is not None:
            get_parameters.début=get_parameters.fin
        # check is date de fin n'existe pas il prend today
        if  get_parameters.début is not None and get_parameters.fin is None:
            get_parameters.fin=str(datetime.date.today())
        list_date.append(datetime.datetime.strptime(get_parameters.début,'%Y-%m-%d').date())
        list_date.append(datetime.datetime.strptime(get_parameters.fin,'%Y-%m-%d').date())

        params = {
            'début': get_parameters.début,
            'fin': get_parameters.fin,
        }
        table_réponse = requests.get(url=url, params=params, timeout=60)
        table_réponse = json.loads(table_réponse.text)
        table=[]
        for key in table_réponse['historique'].keys():
            table.append((datetime.datetime.strptime(key, '%Y-%m-%d').date(),
                          table_réponse['historique'][key][get_parameters.valeur]))
        reponse= ""
        reponse= f"titre={elemnt_symbole}: valeur={get_parameters.valeur}, début="
        reponse+= f"datetime.date({list_date[0].year}, {list_date[0].month}, {list_date[0].day}), "
        reponse+= f"fin=datetime.date({list_date[1].year}, {list_date[1].month}, {list_date[1].day})"
        table.reverse()
        reponse= reponse + "\n" + str(table)
        reponse_finale= reponse_finale + "\n" + reponse
    return reponse_finale

resultat=produire_historique()
print(resultat)
