"""
Génère un dataset fictif de clients et de campagnes marketing.
"""
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# ============================================
# 1. CLIENTS (500 profils)
# ============================================
n_clients = 500

prenoms_h = ["Lucas", "Hugo", "Louis", "Gabriel", "Jules", "Adam", "Raphaël",
             "Arthur", "Nathan", "Ethan", "Paul", "Tom", "Sacha", "Noah"]
prenoms_f = ["Emma", "Jade", "Louise", "Alice", "Chloé", "Lina", "Léa",
             "Rose", "Anna", "Mila", "Julia", "Inès", "Ambre", "Zoé"]

noms = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard",
        "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent",
        "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux",
        "Vincent", "Fournier", "Morel", "Girard", "André", "Mercier"]

villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes",
          "Montpellier", "Strasbourg", "Bordeaux", "Lille", "Rennes",
          "Reims", "Toulon", "Grenoble", "Dijon", "Angers"]

interets = ["Sport", "Cuisine", "Voyage", "Mode", "Technologie", "Lecture",
            "Musique", "Cinéma", "Jardinage", "Fitness", "Art", "Automobile"]

clients = []

for i in range(n_clients):
    sexe = np.random.choice(["Homme", "Femme"])
    prenom = np.random.choice(prenoms_h if sexe == "Homme" else prenoms_f)
    nom = np.random.choice(noms)

    age = int(np.random.normal(45, 15))
    age = max(18, min(85, age))

    # Revenu annuel (corrélé à l'âge)
    revenu_base = 25000 + age * 500
    revenu = int(np.random.normal(revenu_base, 15000))
    revenu = max(15000, min(150000, revenu))

    # Statut marital
    statut = np.random.choice(["Célibataire", "Marié(e)", "Divorcé(e)", "Veuf(ve)"],
                               p=[0.30, 0.45, 0.15, 0.10])

    # Nombre d'enfants (corrélé au statut)
    enfants = 0 if statut == "Célibataire" else np.random.choice([0, 1, 2, 3],
                                                                   p=[0.30, 0.35, 0.25, 0.10])

    # Fréquence d'achat (corrélée au revenu)
    freq_base = 1 + (revenu / 50000)
    freq_achat = int(np.random.poisson(freq_base))

    # Panier moyen (corrélé au revenu)
    panier = int(np.random.normal(revenu / 100, revenu / 300))
    panier = max(20, min(2000, panier))

    # Date dernière commande (nombre de jours)
    jours_derniere_cmd = int(np.random.exponential(60))
    jours_derniere_cmd = min(jours_derniere_cmd, 365)

    # Catégorie préférée
    categorie = np.random.choice([
        "Produits frais", "Épicerie fine", "Boissons", "Bio",
        "Snacks", "Surgelés", "Petit-déjeuner", "Confiserie"
    ])

    # Intérêts (2 aléatoires)
    interets_client = ", ".join(np.random.choice(interets, 2, replace=False))

    clients.append({
        "client_id": f"CLI{i+1:04d}",
        "prenom": prenom,
        "nom": nom,
        "email": f"{prenom.lower()}.{nom.lower()}@example.com",
        "sexe": sexe,
        "age": age,
        "ville": np.random.choice(villes),
        "statut_marital": statut,
        "nb_enfants": enfants,
        "revenu_annuel": revenu,
        "frequence_achat": freq_achat,
        "panier_moyen": panier,
        "jours_derniere_commande": jours_derniere_cmd,
        "categorie_preferee": categorie,
        "interets": interets_client,
    })

df_clients = pd.DataFrame(clients)

# ============================================
# 2. HISTORIQUE CAMPAGNES (50 campagnes)
# ============================================
n_campagnes = 50

produits = ["Chocolat noir bio", "Café premium", "Huile d'olive extra",
            "Fromage affiné", "Vin rouge AOC", "Biscuits artisanaux",
            "Confiture maison", "Miel de lavande", "Thé vert bio",
            "Pâtes italiennes", "Riz basmati", "Sauce tomate bio"]

themes = ["Promotion", "Nouveauté", "Fête", "Saison", "Fidélité", "VIP"]

campagnes = []

for i in range(n_campagnes):
    produit = np.random.choice(produits)
    theme = np.random.choice(themes)

    # Sujet de l'email
    sujets = [
        f"🎁 -20% sur {produit}",
        f"✨ Découvrez notre nouveau {produit}",
        f"🎉 Offre spéciale {theme}",
        f"🍫 {produit} à prix réduit",
        f"⚡ Ne manquez pas {produit}",
        f"💝 Pour vous, {produit} en exclusivité",
    ]
    sujet = np.random.choice(sujets)

    # Taux d'ouverture (corrélé au sujet)
    taux_ouverture = np.random.uniform(0.15, 0.45)

    # Taux de clic (corrélé au taux d'ouverture)
    taux_clic = taux_ouverture * np.random.uniform(0.10, 0.35)

    # Nombre d'envois
    envois = np.random.randint(5000, 50000)

    campagnes.append({
        "campagne_id": f"CAMP{i+1:03d}",
        "produit": produit,
        "theme": theme,
        "sujet_email": sujet,
        "taux_ouverture": round(taux_ouverture, 3),
        "taux_clic": round(taux_clic, 3),
        "nb_envois": envois,
        "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=i * 7),
    })

df_campagnes = pd.DataFrame(campagnes)

# ============================================
# 3. SAUVEGARDE
# ============================================
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

df_clients.to_csv(DATA_DIR / "clients.csv", index=False, encoding="utf-8")
df_campagnes.to_csv(DATA_DIR / "historique_campagnes.csv", index=False, encoding="utf-8")

print(f"✅ {len(df_clients)} clients sauvegardés dans clients.csv")
print(f"✅ {len(df_campagnes)} campagnes sauvegardées dans historique_campagnes.csv")

print("\n📊 Aperçu des clients :")
print(df_clients.head(3).to_string())

print("\n📊 Aperçu des campagnes :")
print(df_campagnes.head(3).to_string())