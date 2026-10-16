"""
Interface Streamlit design premium avec sélecteur de thème dynamique.
"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

import streamlit as st

sys.path.append(str(Path(__file__).parent / "src"))

from email_generator import EmailGenerator
from image_generator import ImageGenerator

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Publicis — Générateur d'emails",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data"


# ============================================
# DÉFINITION DES THÈMES
# ============================================
THEMES = {
    "🌸 Purple": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "bg": "#f5f7fa",
        "bg2": "#c3cfe2",
        "badge1": ("#ede9fe", "#6d28d9"),
        "badge2": ("#dbeafe", "#1e40af"),
        "badge3": ("#d1fae5", "#065f46"),
        "badge4": ("#fce7f3", "#9d174d"),
        "badge5": ("#fed7aa", "#9a3412"),
    },
    "🌊 Ocean": {
        "primary": "#0ea5e9",
        "secondary": "#0284c7",
        "bg": "#f0f9ff",
        "bg2": "#bae6fd",
        "badge1": ("#e0f2fe", "#075985"),
        "badge2": ("#cffafe", "#155e75"),
        "badge3": ("#d1fae5", "#065f46"),
        "badge4": ("#fef3c7", "#92400e"),
        "badge5": ("#e0e7ff", "#3730a3"),
    },
    "🌅 Sunset": {
        "primary": "#f97316",
        "secondary": "#dc2626",
        "bg": "#fff7ed",
        "bg2": "#fed7aa",
        "badge1": ("#fed7aa", "#9a3412"),
        "badge2": ("#fecaca", "#991b1b"),
        "badge3": ("#fef3c7", "#92400e"),
        "badge4": ("#fce7f3", "#9d174d"),
        "badge5": ("#fde68a", "#78350f"),
    },
    "🌲 Forest": {
        "primary": "#10b981",
        "secondary": "#059669",
        "bg": "#f0fdf4",
        "bg2": "#bbf7d0",
        "badge1": ("#d1fae5", "#065f46"),
        "badge2": ("#a7f3d0", "#047857"),
        "badge3": ("#fef3c7", "#92400e"),
        "badge4": ("#e0f2fe", "#075985"),
        "badge5": ("#fce7f3", "#9d174d"),
    },
}


# ============================================
# INITIALISATION DU THÈME EN SESSION
# ============================================
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "🌸 Purple"


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 🎨 Thème")
    theme_names = list(THEMES.keys())
    selected_theme = st.selectbox(
        "Choisis un thème",
        theme_names,
        index=theme_names.index(st.session_state.theme_name),
        label_visibility="collapsed",
        key="theme_selector",
    )
    st.session_state.theme_name = selected_theme

    st.markdown("---")

    st.markdown("### ⚙️ Configuration")

    clients = pd.read_csv(DATA_DIR / "clients.csv")
    client_options = [
        f"👤 {row['prenom']} {row['nom']} ({row['age']} ans) — {row['ville']}"
        for _, row in clients.iterrows()
    ]
    client_idx = st.selectbox(
        "Client",
        range(len(client_options)),
        format_func=lambda i: client_options[i],
        label_visibility="collapsed",
    )
    selected_client = clients.iloc[client_idx].to_dict()

    st.markdown("---")

    produits = [
        "🍫 Chocolat noir bio",
        "☕ Café premium",
        "🍷 Vin rouge AOC",
        "🧀 Fromage affiné",
        "🫒 Huile d'olive extra",
    ]
    selected_produit_display = st.selectbox(
        "Produit", produits, label_visibility="collapsed"
    )
    selected_produit = selected_produit_display.split(" ", 1)[1]

    st.markdown("---")

    generate_btn = st.button(
        "🚀  Générer l'email",
        type="primary",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown(
        f'<div style="font-size: 0.75rem; color: #6b7280; text-align: center;">'
        f'<b>Stack</b> : Ollama · Pixabay · Streamlit<br>'
        f'<b>Thème</b> : {selected_theme}<br>'
        f'<b>Modèle</b> : llama3.2:3b</div>',
        unsafe_allow_html=True,
    )


# ============================================
# APPLICATION DU THÈME
# ============================================
T = THEMES[selected_theme]

st.markdown(
    f"""<style>
/* ============ GLOBAL ============ */
.main {{ background: linear-gradient(135deg, {T['bg']} 0%, {T['bg2']} 100%); }}
.block-container {{ padding-top: 2rem; }}

/* ============ SIDEBAR ============ */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {T['bg']} 0%, {T['bg2']} 100%);
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown {{
    color: #1a1a1a !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSelectbox > div > div {{
    color: #1a1a1a !important;
}}

/* ============ HEADER ============ */
.main-header {{
    background: linear-gradient(135deg, {T['primary']} 0%, {T['secondary']} 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px {T['primary']}4d;
}}
.main-header h1 {{ color: white !important; font-size: 2.5rem; margin: 0; font-weight: 700; }}
.main-header p {{ color: rgba(255, 255, 255, 0.9) !important; font-size: 1.1rem; margin: 0.5rem 0 0 0; }}

/* ============ CARDS ============ */
.info-card {{
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 1rem;
    border-left: 4px solid {T['primary']};
}}
.profile-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    background: linear-gradient(90deg, {T['bg']} 0%, #ffffff 100%);
    border-radius: 10px;
    border-left: 3px solid {T['primary']};
}}
.profile-label {{ color: #6b7280 !important; font-weight: 500; font-size: 0.9rem; }}
.profile-value {{ color: #1f2937 !important; font-weight: 600; font-size: 1rem; text-align: right; }}

/* ============ BADGES ============ */
.badge {{ display: inline-block; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin: 0.2rem; }}
.badge-purple {{ background: {T['badge1'][0]}; color: {T['badge1'][1]} !important; }}
.badge-blue {{ background: {T['badge2'][0]}; color: {T['badge2'][1]} !important; }}
.badge-green {{ background: {T['badge3'][0]}; color: {T['badge3'][1]} !important; }}
.badge-pink {{ background: {T['badge4'][0]}; color: {T['badge4'][1]} !important; }}
.badge-orange {{ background: {T['badge5'][0]}; color: {T['badge5'][1]} !important; }}

/* ============ PRODUIT ============ */
.product-card {{ background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); text-align: center; }}

/* ============ EMAIL ============ */
.email-subject {{
    background: linear-gradient(135deg, {T['primary']} 0%, {T['secondary']} 100%);
    color: white !important;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    font-size: 1.15rem;
    font-weight: 600;
    margin: 1rem 0;
    box-shadow: 0 4px 15px {T['primary']}4d;
}}
.email-body {{
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    white-space: pre-wrap;
    font-family: Georgia, serif;
    font-size: 1rem;
    line-height: 1.7;
    color: #1f2937 !important;
}}

/* ============ METRICS ============ */
.metric-card {{ background: white; padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); border-top: 3px solid {T['primary']}; }}
.metric-value {{ font-size: 1.5rem; font-weight: 700; color: {T['primary']} !important; margin: 0.3rem 0 0 0; }}
.metric-label {{ font-size: 0.8rem; color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.5px; }}
</style>""",
    unsafe_allow_html=True,
)


# ============================================
# HEADER
# ============================================
st.markdown(
    '<div class="main-header"><h1>✉️ Générateur d\'emails marketing</h1>'
    '<p>Publicis — Campagnes email automatisées et personnalisées pour l\'agroalimentaire</p></div>',
    unsafe_allow_html=True,
)


# ============================================
# INITIALISATION DES GÉNÉRATEURS
# ============================================
@st.cache_resource
def init_generators():
    return EmailGenerator(), ImageGenerator()


with st.spinner("🚀 Initialisation des générateurs..."):
    email_gen, image_gen = init_generators()


# ============================================
# LAYOUT
# ============================================
col_left, col_right = st.columns([3, 2])


# ============================================
# PROFIL CLIENT
# ============================================
with col_left:
    st.markdown("### 📋 Profil du client")

    profile_items = [
        ("👤 Prénom", selected_client["prenom"]),
        ("🎂 Âge", f"{selected_client['age']} ans"),
        ("📍 Ville", selected_client["ville"]),
        ("💍 Statut", selected_client["statut_marital"]),
        ("👶 Enfants", str(selected_client["nb_enfants"])),
        ("💰 Revenu annuel", f"{selected_client['revenu_annuel']:,} €"),
        ("🛒 Fréquence d'achat", f"{selected_client['frequence_achat']}×/mois"),
        ("💳 Panier moyen", f"{selected_client['panier_moyen']} €"),
        ("❤️ Catégorie préférée", selected_client["categorie_preferee"]),
    ]

    html = '<div class="info-card">'
    for label, value in profile_items:
        html += (
            '<div class="profile-row">'
            '<span class="profile-label">' + label + '</span>'
            '<span class="profile-value">' + value + '</span>'
            '</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    # Badges intérêts
    interets = [i.strip() for i in selected_client["interets"].split(",")]
    badges_html = (
        '<div style="margin-top: 1rem;">'
        '<b style="color: #6b7280; font-size: 0.9rem;">🎯 Intérêts</b><br>'
    )
    colors = ["badge-purple", "badge-blue", "badge-green", "badge-pink", "badge-orange"]
    for i, interet in enumerate(interets):
        badges_html += (
            '<span class="badge ' + colors[i % len(colors)] + '">' + interet + "</span>"
        )
    badges_html += "</div>"
    st.markdown(badges_html, unsafe_allow_html=True)


# ============================================
# PRODUIT
# ============================================
with col_right:
    st.markdown("### 🛍️ Produit sélectionné")
    st.markdown(
        '<div class="product-card">'
        '<h3 style="color: ' + T["primary"] + '; margin-top: 0;">'
        + selected_produit_display + "</h3></div>",
        unsafe_allow_html=True,
    )

    image_path = image_gen.get_image(selected_produit)
    if image_path and image_path.exists():
        st.image(str(image_path), use_container_width=True)


# ============================================
# GÉNÉRATION
# ============================================
if generate_btn:
    with st.spinner("⏳ Génération de l'email (30-60 sec)..."):
        result = email_gen.generate_email(selected_client, selected_produit)

    st.markdown("---")
    st.markdown("### 📧 Email généré")

    st.markdown(
        '<div class="email-subject">📧 ' + result["sujet"] + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="email-body">' + result["corps"] + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Métriques")
    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.markdown(
            '<div class="metric-card">'
            '<p class="metric-label">🎯 Ton</p>'
            '<p class="metric-value" style="font-size: 1rem;">'
            + result["ton"] + "</p></div>",
            unsafe_allow_html=True,
        )

    with col_m2:
        st.markdown(
            '<div class="metric-card">'
            '<p class="metric-label">🎁 Offre</p>'
            '<p class="metric-value" style="font-size: 1rem;">'
            + result["offre"] + "</p></div>",
            unsafe_allow_html=True,
        )

    with col_m3:
        word_count = len(result["corps"].split())
        st.markdown(
            '<div class="metric-card">'
            '<p class="metric-label">📝 Longueur</p>'
            '<p class="metric-value">' + str(word_count) + " mots</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    export_data = pd.DataFrame(
        [
            {
                "client_id": result["client_id"],
                "prenom": result["prenom"],
                "email": selected_client["email"],
                "produit": selected_produit,
                "sujet": result["sujet"],
                "corps": result["corps"],
                "ton": result["ton"],
                "offre": result["offre"],
            }
        ]
    )

    csv = export_data.to_csv(index=False, encoding="utf-8")
    col_exp1, col_exp2 = st.columns([1, 3])
    with col_exp1:
        st.download_button(
            "💾 Télécharger (CSV)",
            csv,
            file_name="email_"
            + result["client_id"]
            + "_"
            + datetime.now().strftime("%Y%m%d")
            + ".csv",
            mime="text/csv",
            use_container_width=True,
        )


# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #9ca3af; font-size: 0.8rem; padding: 1rem;">'
    "Projet IA Générative — M2 Data Science · "
    "Basé sur <b>Ollama</b> (llama3.2:3b) · <b>Pixabay</b> · <b>Streamlit</b></div>",
    unsafe_allow_html=True,
)