"""
Générateur d'emails marketing personnalisés avec Ollama.
"""
import re
import pandas as pd
from pathlib import Path
from ollama import Client

from prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    select_ton,
    select_offre,
)


class EmailGenerator:
    """Génère des emails marketing personnalisés."""

    def __init__(self, model: str = "llama3.2:3b"):
        self.client = Client()
        self.model = model
        print(f"✅ Générateur initialisé (modèle = {model})")

    def generate_email(self, client: dict, produit: str) -> dict:
        """Génère un email pour un client donné."""
        # Sélection du ton et de l'offre
        ton = select_ton(client["age"], client["sexe"], client["statut_marital"])
        offre = select_offre(client["age"], client["revenu_annuel"])

        # Construction du prompt
        user_prompt = USER_PROMPT_TEMPLATE.format(
            prenom=client["prenom"],
            age=client["age"],
            sexe=client["sexe"],
            ville=client["ville"],
            statut_marital=client["statut_marital"],
            nb_enfants=client["nb_enfants"],
            revenu_annuel=client["revenu_annuel"],
            frequence_achat=client["frequence_achat"],
            panier_moyen=client["panier_moyen"],
            categorie_preferee=client["categorie_preferee"],
            interets=client["interets"],
            produit=produit,
            type_offre=offre["type_offre"],
            reduction=offre["reduction"],
            ton=ton,
        )

        # Appel au LLM
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 400,
            }
        )

        raw_text = response["message"]["content"].strip()

        # Parsing de la réponse
        sujet, corps = self._parse_response(raw_text)

        return {
            "client_id": client["client_id"],
            "prenom": client["prenom"],
            "sujet": sujet,
            "corps": corps,
            "ton": ton,
            "offre": offre["type_offre"],
            "raw": raw_text,
        }

    def _parse_response(self, text: str) -> tuple:
        """Parse la réponse du LLM pour extraire sujet et corps."""
        sujet = "Sujet non trouvé"
        corps = text

        # Chercher SUJET (avec ou sans espace avant :)
        sujet_match = re.search(
            r"SUJET\s*:\s*(.+?)(?:\n|CORPS)",
            text,
            re.IGNORECASE | re.DOTALL
        )
        if sujet_match:
            sujet = sujet_match.group(1).strip()

        # Chercher CORPS
        corps_match = re.search(
            r"CORPS\s*:\s*(.+)",
            text,
            re.IGNORECASE | re.DOTALL
        )
        if corps_match:
            corps = corps_match.group(1).strip()
        elif sujet_match:
            # Si pas de CORPS, prendre tout après le sujet
            corps = text[sujet_match.end():].strip()

        return sujet, corps


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    DATA_DIR = Path(__file__).parent.parent / "data"
    clients = pd.read_csv(DATA_DIR / "clients.csv")

    generator = EmailGenerator()

    # Test sur 3 clients
    print("\n" + "=" * 60)
    print("📧 TEST DE GÉNÉRATION D'EMAILS")
    print("=" * 60)

    test_clients = clients.head(3).to_dict("records")

    for i, client in enumerate(test_clients, 1):
        print(f"\n{'='*60}")
        print(f"CLIENT {i} : {client['prenom']}, {client['age']} ans")
        print(f"Intérêts : {client['interets']}")
        print("=" * 60)

        print("⏳ Génération en cours...")
        result = generator.generate_email(client, "Chocolat noir bio")

        print(f"\n📧 SUJET : {result['sujet']}")
        print(f"\n📝 CORPS :\n{result['corps']}")
        print(f"\n🎯 Ton utilisé : {result['ton']}")
        print(f"🎁 Offre : {result['offre']}")