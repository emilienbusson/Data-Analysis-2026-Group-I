import pandas as pd

df=pd.read_csv("listings_detailed.csv", dtype={"id":str,"host_id":str,"host_profile_id":str,"scrape_id":str})  #j'ai mis les id en string pour éviter un éventuel arrondi
print(df.shape)
df.info()
print(df.isna().sum())

#sortir toutes les colonnes vides
empty_cols=df.columns[df.isna().sum()==len(df)]
print("empty columns:",list(empty_cols))
df=df.drop(columns=empty_cols)
df=df.drop(columns=["scrape_id","host_url","host_profile_url","host_picture_url","host_about"])

df["price"] = df["price"].str.replace("$", "", regex=False)
df["price"] = df["price"].str.replace(",", "", regex=False)
df["price"] = pd.to_numeric(df["price"])
print(df["price"].describe())
#on enlève le $ pour laisser uniquement un nombre (par contre est ce qu'il faut qu'on convertisse en CHF? on peut utiliser le taux de change annualisé ça se trouve sur la BNS j'ai fais ça dans un autre cours
#vérifier si le prix est pas dans une colonne à côté
print("missing prices:", df["price"].isna().sum())
print(( df["price"].isna() & df["price_quote_price_per_night"].notna() ).sum())
df["price_quote_checkin_date"] = pd.to_datetime(df["price_quote_checkin_date"])
df["price_quote_checkout_date"] = pd.to_datetime(df["price_quote_checkout_date"])
nights = (df["price_quote_checkout_date"] - df["price_quote_checkin_date"]).dt.days
price_total = df["price_quote_total_price"] / nights
print(( df["price"].isna() & price_total.notna() ).sum())
no_price_raw = df["price_quote_raw"].str.contains('"price_per_night": null', regex=False)
print(( df["price"].isna() & df["price_quote_raw"].notna() & (no_price_raw == False) ).sum())
#on enlève les lignes où le prix est vide
n = df.shape[0]
df = df.dropna(subset=["price"])
print("rows removed (no price):", n - df.shape[0])
df = df.drop(columns=["price_quote_raw"]
