"""
Prompts pour la génération d'emails marketing personnalisés.
"""

# ============================================
# PROMPT SYSTÈME (version stricte)
# ============================================
SYSTEM_PROMPT = """Tu es un copywriter marketing expert chez Publicis.
Tu rédiges des emails promotionnels pour une marque agroalimentaire premium.

RÈGLES ABSOLUES :
1. Réponds UNIQUEMENT en français correct et naturel.
2. Utilise le tutoiement (tu/toi/ton) pour les moins de 50 ans,
   le vouvoiement (vous/votre) pour les 50 ans et plus.
3. Sois concis : maximum 120 mots pour le corps.
4. N'invente JAMAIS de mots ou d'expressions.
5. Utilise UNIQUEMENT les informations fournies.
6. Termine par UN SEUL call-to-action clair.
7. NE RÉPÈTE PAS le call-to-action.

FORMAT DE RÉPONSE (RESPECTE EXACTEMENT) :
SUJET: <sujet, max 60 caractères, avec 1 émoji>
CORPS:
<corps de 80-120 mots>

INTERDIT :
- Mettre des crochets [comme ceci]
- Inventer un nom de marque
- Répéter le sujet dans le corps
- Utiliser des mots anglais (added, etc.)

EXEMPLE DE BON FORMAT :
SUJET: 🍫 Découvrez notre chocolat bio d'exception
CORPS:
Bonjour Marie,

Nous avons le plaisir de vous convier à découvrir notre chocolat
noir bio, élaboré avec des fèves de cacao équitables.

En tant que cliente fidèle, profitez de -20% sur votre commande
avec le code CHOCO20.

Offre valable jusqu'à dimanche. Commandez dès maintenant !
"""


# ============================================
# PROMPT UTILISATEUR
# ============================================
USER_PROMPT_TEMPLATE = """Génère un email promotionnel pour le client suivant :

PROFIL CLIENT :
- Prénom : {prenom}
- Âge : {age} ans
- Sexe : {sexe}
- Ville : {ville}
- Statut : {statut_marital}
- Enfants : {nb_enfants}
- Revenu annuel : {revenu_annuel} €
- Fréquence d'achat : {frequence_achat} fois/mois
- Panier moyen : {panier_moyen} €
- Catégorie préférée : {categorie_preferee}
- Intérêts : {interets}

CONTEXTE CAMPAGNE :
- Produit à promouvoir : {produit}
- Type d'offre : {type_offre}
- Réduction : {reduction}

CONTRAINTES :
- Ton à utiliser : {ton}
- Objectif : maximiser le taux de clic

Génère maintenant l'email (SUJET + CORPS) :"""


# ============================================
# FONCTION DE SÉLECTION DU TON
# ============================================
def select_ton(age: int, sexe: str, statut: str) -> str:
    """Sélectionne le ton adapté au profil du client."""
    if age < 30:
        return "décontracté et dynamique"
    elif age < 50:
        return "professionnel et chaleureux"
    elif age < 65:
        return "élégant et rassurant"
    else:
        return "respectueux et convivial"


# ============================================
# FONCTION DE SÉLECTION DE L'OFFRE
# ============================================
def select_offre(age: int, revenu: int) -> dict:
    """Sélectionne l'offre adaptée au profil."""
    if revenu > 60000:
        return {
            "type_offre": "offre premium exclusive",
            "reduction": "livraison gratuite + cadeau surprise"
        }
    elif age < 35:
        return {
            "type_offre": "promotion nouvelle génération",
            "reduction": "-25% sur votre première commande"
        }
    elif age > 60:
        return {
            "type_offre": "offre fidélité senior",
            "reduction": "-15% + livraison offerte"
        }
    else:
        return {
            "type_offre": "promotion standard",
            "reduction": "-20% sur le produit du mois"
        }


if __name__ == "__main__":
    # Test
    print("=== TEST DES FONCTIONS ===")
    print(f"Ton (25 ans) : {select_ton(25, 'Femme', 'Célibataire')}")
    print(f"Ton (45 ans) : {select_ton(45, 'Homme', 'Marié(e)')}")
    print(f"Ton (70 ans) : {select_ton(70, 'Femme', 'Veuf(ve)')}")

    print(f"\nOffre (revenu 80k) : {select_offre(45, 80000)}")
    print(f"Offre (revenu 30k) : {select_offre(25, 30000)}")
    print(f"Offre (revenu 40k, 65 ans) : {select_offre(65, 40000)}")