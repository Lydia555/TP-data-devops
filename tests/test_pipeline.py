import pandas as pd
from pipeline import transformer, agreger_par_ville


def test_supprimer_doublons():
    df = pd.DataFrame({
        "ville": ["Paris", "Paris"],
        "quantite": [2, 2],
        "prix_unitaire": [10, 10],
    })
    resultat = transformer(df)
    assert len(resultat) == 1


def test_supprimer_quantite_negative():
    df = pd.DataFrame({
        "ville": ["Paris", "Lyon"],
        "quantite": [2, -1],
        "prix_unitaire": [10, 10],
    })
    resultat = transformer(df)
    assert len(resultat) == 1


def test_calcul_montant():
    df = pd.DataFrame({
        "ville": ["Paris"],
        "quantite": [3],
        "prix_unitaire": [10],
    })
    resultat = transformer(df)
    assert resultat.iloc[0]["montant"] == 30


def test_chiffre_affaires_par_ville():
    df = pd.DataFrame({
        "ville": ["Paris", "Paris", "Lyon"],
        "quantite": [2, 3, 1],
        "prix_unitaire": [10, 10, 20],
    })
    propre = transformer(df)
    resultat = agreger_par_ville(propre)
    paris = resultat[resultat["ville"] == "Paris"]
    assert paris.iloc[0]["montant"] == 50
