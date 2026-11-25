from pathlib import Path
import pandas as pd


def extraire(chemin):
    return pd.read_csv(chemin)


def transformer(df):
    df = df.drop_duplicates()
    df = df.dropna(subset=["quantite", "prix_unitaire"])
    df = df[df["quantite"] > 0].copy()
    df["ville"] = df["ville"].str.strip().str.title()
    df["montant"] = df["quantite"] * df["prix_unitaire"]
    return df


def agreger_par_ville(df):
    resultat = df.groupby("ville", as_index=False)["montant"].sum()
    return resultat.sort_values("montant", ascending=False)


def agreger_par_categorie(df):
    resultat = df.groupby("categorie", as_index=False)["montant"].sum()
    return resultat.sort_values("montant", ascending=False)


def charger(df, chemin):
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False)


def main():
    brut = extraire("data/ventes.csv")
    propre = transformer(brut)

    par_ville = agreger_par_ville(propre)
    par_categorie = agreger_par_categorie(propre)

    charger(propre, "output/ventes_propres.csv")
    charger(par_ville, "output/ca_par_ville.csv")
    charger(par_categorie, "output/ca_par_categorie.csv")

    print("Pipeline terminé !")
    print(par_ville)
    print(par_categorie)


if __name__ == "__main__":
    main()
