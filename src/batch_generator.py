"""
Génération d'emails en batch (500 clients).
"""
import pandas as pd
import time
from pathlib import Path
from email_generator import EmailGenerator

# ============================================
# CONFIGURATION
# ============================================
N_CLIENTS = 5   # ⚠️ Mets 5 pour tester, puis 500
PRODUITS = [
    "Chocolat noir bio",
    "Café premium",
    "Huile d'olive extra",
    "Fromage affiné",
    "Vin rouge AOC",
]

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def main():
    print("=" * 60)
    print(f"📧 GÉNÉRATION BATCH — {N_CLIENTS} CLIENTS")
    print("=" * 60)

    # Charger les clients
    clients = pd.read_csv(DATA_DIR / "clients.csv")
    clients_subset = clients.head(N_CLIENTS)

    print(f"✅ {len(clients_subset)} clients à traiter\n")

    # Initialiser le générateur
    generator = EmailGenerator()

    # Générer les emails
    results = []
    start_time = time.time()

    for i, client in enumerate(clients_subset.to_dict("records"), 1):
        print(f"[{i}/{N_CLIENTS}] 📧 {client['prenom']} ({client['age']} ans)...")

        # Choisir un produit (rotation)
        produit = PRODUITS[i % len(PRODUITS)]

        try:
            email = generator.generate_email(client, produit)
            results.append({
                "client_id": email["client_id"],
                "prenom": email["prenom"],
                "age": client["age"],
                "email": client["email"],
                "produit": produit,
                "sujet": email["sujet"],
                "corps": email["corps"],
                "ton": email["ton"],
                "offre": email["offre"],
            })
            print(f"     ✅ Sujet : {email['sujet'][:60]}...")

        except Exception as e:
            print(f"     ❌ Erreur : {e}")

    # Sauvegarder
    OUTPUT_DIR.mkdir(exist_ok=True)
    df_results = pd.DataFrame(results)
    output_file = OUTPUT_DIR / "emails_generes.csv"
    df_results.to_csv(output_file, index=False, encoding="utf-8")

    duration = time.time() - start_time

    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"✅ {len(results)} emails générés")
    print(f"⏱️  Temps total : {duration:.1f} sec")
    print(f"⚡ Vitesse : {duration / len(results):.1f} sec / email")
    print(f"💾 Fichier : {output_file}")

    # Afficher un extrait
    print("\n📧 Exemple d'email généré :")
    if results:
        print(f"\n{'='*60}")
        print(f"À      : {results[0]['email']}")
        print(f"SUJET  : {results[0]['sujet']}")
        print(f"{'='*60}")
        print(f"{results[0]['corps']}")


if __name__ == "__main__":
    main()