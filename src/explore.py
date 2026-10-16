import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# Chargement
clients = pd.read_csv(DATA_DIR / "clients.csv")
campagnes = pd.read_csv(DATA_DIR / "historique_campagnes.csv")

print("=" * 60)
print("📊 DATASET CLIENTS")
print("=" * 60)
print(f"Nombre de clients : {len(clients)}")
print(f"Colonnes : {list(clients.columns)}")
print(f"\nStatistiques :")
print(clients.describe().T)

print("\n" + "=" * 60)
print("📊 DATASET CAMPAGNES")
print("=" * 60)
print(f"Nombre de campagnes : {len(campagnes)}")
print(f"Taux d'ouverture moyen : {campagnes['taux_ouverture'].mean():.2%}")
print(f"Taux de clic moyen : {campagnes['taux_clic'].mean():.2%}")

print("\n🎯 Top 5 campagnes par taux de clic :")
print(campagnes.nlargest(5, "taux_clic")[["campagne_id", "sujet_email", "taux_clic"]].to_string())