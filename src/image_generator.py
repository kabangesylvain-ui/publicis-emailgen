"""
Récupération d'images avec Pixabay API (gratuit).
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class ImageGenerator:
    """Récupère et associe des images aux produits."""

    BASE_URL = "https://pixabay.com/api/"

    # Mapping français → anglais (pour la recherche Pixabay)
    KEYWORDS_MAP = {
        "chocolat": "chocolate",
        "café": "coffee",
        "cafe": "coffee",
        "huile": "olive oil",
        "fromage": "cheese",
        "vin": "red wine",
        "biscuit": "cookies",
        "confiture": "jam",
        "miel": "honey",
        "thé": "tea",
        "the": "tea",
        "pâtes": "pasta",
        "pates": "pasta",
        "sauce": "tomato sauce",
    }

    # Mapping produit → nom de fichier image (pour l'affichage local)
    FILENAME_MAP = {
        "chocolat": "chocolat_noir_bio.jpg",
        "café": "cafe_premium.jpg",
        "cafe": "cafe_premium.jpg",
        "vin": "vin_rouge_aoc.jpg",
        "fromage": "fromage_affine.jpg",
        "huile": "huile_olive_extra.jpg",
        "biscuit": "biscuits.jpg",
        "confiture": "confiture.jpg",
        "miel": "miel.jpg",
        "thé": "the.jpg",
        "the": "the.jpg",
        "pâtes": "pates.jpg",
        "pates": "pates.jpg",
    }

    def __init__(self, output_dir: Path = None):
        self.api_key = os.getenv("PIXABAY_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "❌ PIXABAY_API_KEY manquante dans .env\n"
                "Va sur https://pixabay.com/api/docs/ pour obtenir une clé gratuite."
            )

        self.output_dir = output_dir or Path(__file__).parent.parent / "output" / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"✅ Générateur d'images prêt (Pixabay)")
        print(f"   Dossier : {self.output_dir}")

    def _get_english_keyword(self, produit: str) -> str:
        """Convertit un mot-clé français en anglais."""
        produit_lower = produit.lower()
        for fr, en in self.KEYWORDS_MAP.items():
            if fr in produit_lower:
                return en
        return produit_lower

    def _get_filename(self, produit: str) -> str:
        """Retourne le nom de fichier fixe pour un produit."""
        produit_lower = produit.lower()
        for keyword, filename in self.FILENAME_MAP.items():
            if keyword in produit_lower:
                return filename
        # Fallback : nom générique
        return produit.lower().replace(" ", "_").replace("/", "_") + ".jpg"

    def generate_image(self, produit: str, filename: str = None) -> Path:
        """Télécharge une image via Pixabay API."""
        keyword = self._get_english_keyword(produit)
        print(f"🎨 Recherche : {produit} (keyword: {keyword})...")

        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "key": self.api_key,
                    "q": keyword,
                    "image_type": "photo",
                    "orientation": "horizontal",
                    "per_page": 3,
                    "safesearch": "true",
                },
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("hits"):
                print(f"   ❌ Aucune image trouvée pour '{keyword}'")
                return None

            # Prendre la 1ère image
            image_url = data["hits"][0]["largeImageURL"]

            if filename is None:
                filename = self._get_filename(produit)
            filepath = self.output_dir / filename

            # Télécharger
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(img_response.content)

            size_ko = len(img_response.content) // 1024
            print(f"   ✅ {filepath.name} ({size_ko} Ko)")
            return filepath

        except Exception as e:
            print(f"   ❌ Erreur : {e}")
            return None

    def get_image(self, produit: str) -> Path:
        """
        Retourne le chemin de l'image locale associée au produit.
        Cherche dans output/images/ puis assets/images/.
        Retourne None si introuvable.
        """
        filename = self._get_filename(produit)

        # Emplacements possibles
        locations = [
            self.output_dir,
            Path(__file__).parent.parent / "assets" / "images",
        ]

        for base_dir in locations:
            path = base_dir / filename
            if path.exists():
                return path

        return None

    def ensure_image(self, produit: str) -> Path:
        """
        S'assure qu'une image existe pour le produit.
        Si elle n'existe pas localement, la télécharge via Pixabay.
        """
        image = self.get_image(produit)
        if image:
            return image
        return self.generate_image(produit)


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    generator = ImageGenerator()

    produits = [
        "Chocolat noir bio",
        "Café premium",
        "Vin rouge AOC",
        "Fromage affiné",
        "Huile d'olive extra",
    ]

    print("=" * 60)
    print("🎨 TEST PIXABAY")
    print("=" * 60)

    for produit in produits:
        # Vérifier si déjà téléchargée
        existing = generator.get_image(produit)
        if existing:
            print(f"✅ {produit} → déjà présente : {existing.name}")
        else:
            print(f"⏳ {produit} → téléchargement...")
            generator.generate_image(produit)

    print("\n✅ Test terminé !")
    print("Ouvre : start output\\images")