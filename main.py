
import streamlit as st
import random
import json
import os
import time
from datetime import datetime




if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email.strip() == "" or password.strip() == "":
            st.error("Please enter both email and password")
        else:
            st.session_state.logged_in = True
            st.rerun()

# Show login page until logged in
if not st.session_state.logged_in:
    login_page()
    st.stop()





# ---------------------------------------------------------
# DATA PERSISTENCE
# ---------------------------------------------------------
FLASHCARD_FILE = "flashcards.json"
SCOREBOARD_FILE = "scoreboard.json"

def load_flashcards():
    """Load flashcards from JSON file or return default data"""
    default_data = [
        {
            "subject": "Math",
            "front": "➗ Quadratic Formula",
            "back": "Solution for a quadratic equation $ax^2+bx+c=0$." + r'$$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$'
        },
        {
            "subject": "Math",
            "front": "➗ Taylor Series (Maclaurin)",
            "back": "Power-series expansion of $e^x$ about 0." + r'$$e^x=\sum_{n=0}^{\infty}\frac{x^n}{n!}$$'
        },
        {
            "subject": "Math",
            "front": "➗ Fundamental Theorem of Calculus",
            "back": "Connects differentiation and integration." + r'$$\frac{d}{dx}\int_a^x f(t)\,dt=f(x)$$'
        },
        {
            "subject": "Math",
            "front": "➗ Eigenvalues & Characteristic Polynomial",
            "back": "Eigenvalues λ satisfy the determinant equation." + r'$$\det(A-\lambda I)=0$$'
        },
        {
            "subject": "Math",
            "front": "➗ Divergence Theorem",
            "back": "Relates flux to divergence." + r'$$\int_V\nabla\cdot\mathbf{F}\,dV=\oint_{\partial V}\mathbf{F}\cdot d\mathbf{S}$$'
        },
        {
            "subject": "Physics",
            "front": "🔬 Newton's Second Law",
            "back": "Force equals mass times acceleration." + r'$$\mathbf{F}=m\mathbf{a}$$'
        },
        {
            "subject": "Physics",
            "front": "🔬 Conservation of Energy",
            "back": "Total mechanical energy remains constant." + r'$$E=K+U$$'
        },
        {
            "subject": "Physics",
            "front": "🔬 Schrödinger Equation",
            "back": "Quantum wave equation." + r'$$-\frac{\hbar^2}{2m}\nabla^2\psi+V\psi=E\psi$$'
        },
        {
            "subject": "Physics",
            "front": "🔬 Lorentz Force",
            "back": "Force on a charged particle." + r'$$\mathbf{F}=q(\mathbf{E}+\mathbf{v}\times\mathbf{B})$$'
        },
        {
            "subject": "Physics",
            "front": "🔬 Simple Harmonic Oscillator",
            "back": "SHO differential equation." + r'$$m\ddot{x}+kx=0$$'
        },
        {
            "subject": "Chemistry",
            "front": "⚛️ Ideal Gas Law",
            "back": "Gas pressure-volume relation." + r'$$PV=nRT$$'
        },
        {
            "subject": "Chemistry",
            "front": "⚛️ Gibbs Free Energy",
            "back": "Energy available for work." + r'$$\Delta G=\Delta H-T\Delta S$$'
        },
        {
            "subject": "Chemistry",
            "front": "⚛️ Arrhenius Equation",
            "back": "Reaction rate temperature dependence." + r'$$k=Ae^{-E_a/(RT)}$$'
        },
        {
            "subject": "Chemistry",
            "front": "⚛️ Beer–Lambert Law",
            "back": "Absorbance relation." + r'$$A=\varepsilon c\ell$$'
        },
        {
            "subject": "Chemistry",
            "front": "⚛️ Henderson–Hasselbalch Equation",
            "back": "pH of buffer solution." + r'$$\mathrm{pH}=pK_a+\log\frac{[A^-]}{[HA]}$$'
        },
    ]

    if os.path.exists(FLASHCARD_FILE):
        try:
            with open(FLASHCARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def save_flashcards(data):
    """Save flashcards to JSON file"""
    with open(FLASHCARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Flashcard Quiz App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# SESSION STATE VARIABLES
# ---------------------------------------------------------
if "flashcards" not in st.session_state:
    st.session_state.flashcards = load_flashcards()

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False


# -------------------------
# CUSTOM SIDEBAR STYLING
# -------------------------
import streamlit as st

sidebar_css = """
<style>

[data-testid="stSidebar"] {
    background-color: #f3e8ff !important;   /* Light Purple */
    padding: 20px !important;
}

[data-testid="stSidebar"] * {
    color: #3b0764 !important;               /* Dark purple text */
    font-family: 'Segoe UI', sans-serif !important;
}

/* Sidebar radio buttons */
div[data-baseweb="radio"] > div {
    background: #ede9fe;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 0 8px rgba(120, 0, 255, 0.15);
}

div[data-baseweb="radio"] label {
    font-size: 16px;
    font-weight: 600;
}

/* Divider lines */
hr {
    border: 1px solid #ddd !important;
}

</style>
"""

st.markdown(sidebar_css, unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------


st.sidebar.title("📚 Flashcard Quiz App")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🔄 FORMULA Flashcards", "🛠️ Create Flashcards", "📋 Manage Flashcards"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Flashcards:** {len(st.session_state.flashcards)}")




# ---------------------------------------------------------
# PAGE 1: FLIP FLASHCARDS
# ---------------------------------------------------------


button_css = """
<style>

/* Make buttons blue */
div.stButton > button {
    background-color: #3b82f6 !important;   /* Blue */
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    border: none !important;
    font-size: 16px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #2563eb !important;
    transition: 0.2s;
}

/* Make dropdown ("Filter by Subject") blue */
div[data-baseweb="select"] > div {
    background-color: #dbeafe !important;  /* Light Blue background */
    border-radius: 8px !important;
}

div[data-baseweb="select"] * {
    color: #1e3a8a !important;  /* Dark Blue text */
    font-weight: 600 !important;
}

</style>
"""

st.markdown(button_css, unsafe_allow_html=True)





if page == "🔄 FORMULA Flashcards":
    st.title("🔄 FORMULA Flashcards")
    st.markdown("Click the card to flip it!")

    if len(st.session_state.flashcards) == 0:
        st.warning("No flashcards available. Create some flashcards first!")
    else:
        subjects = sorted(list(set(c["subject"] for c in st.session_state.flashcards)))
        selected_subject = st.selectbox("Filter by Subject", ["All"] + subjects)

        filtered = st.session_state.flashcards
        if selected_subject != "All":
            filtered = [c for c in filtered if c["subject"] == selected_subject]

        if len(filtered) == 0:
            st.warning("No flashcards found.")
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("◀ Previous"):
                    st.session_state.current_index = (st.session_state.current_index - 1) % len(filtered)
                    st.session_state.is_flipped = False

            with col2:
                st.markdown(
                    f"<div style='text-align:center;'><strong>Card {st.session_state.current_index + 1} of {len(filtered)}</strong></div>",
                    unsafe_allow_html=True
                )

            with col3:
                if st.button("Next ▶"):
                    st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered)
                    st.session_state.is_flipped = False

            if st.button("Answer Key"):
                st.session_state.is_flipped = not st.session_state.is_flipped

            card = filtered[st.session_state.current_index]

            if not st.session_state.is_flipped:
                st.markdown(
                    f"""
                    <div style="
                        background:#d9c4f1;
                        color:black;
                        padding:40px;
                        border-radius:15px;
                        text-align:center;
                        box-shadow:0 4px 15px rgba(0,0,0,0.5);
                        max-width:600px;
                        margin:auto;">
                        <h2>{card['front']}</h2>
                        <p style="opacity:0.7;">Click 'Answer Key' to see the solution</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.subheader("Solution:")
                st.markdown(card["back"])

            st.markdown(f"**Subject:** {card['subject']}")


            
         
            

# ---------------------------------------------------------
# PAGE 2: CREATE FLASHCARDS
# ---------------------------------------------------------
elif page == "🛠️ Create Flashcards":
    st.title("🛠️ Create Your Own Flashcards")

    with st.form("create_flashcard_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Subject", ["Math", "Physics", "Chemistry", "Biology", "Other"])
        with col2:
            if subject == "Other":
                subject = st.text_input("Enter Subject Name")

        front = st.text_input("Front (Question/Title)")
        back = st.text_area("Back (Answer/Definition)", height=150)

        submitted = st.form_submit_button("➕ Add Flashcard")

        if submitted:
            if front.strip() and back.strip():
                st.session_state.flashcards.append(
                    {"subject": subject, "front": front, "back": back}
                )
                save_flashcards(st.session_state.flashcards)
                st.success("Flashcard added!")
                st.rerun()
            else:
                st.error("Fill both front and back.")

    st.markdown("---")
    st.subheader("📋 Your Flashcards")

    if len(st.session_state.flashcards) == 0:
        st.info("No flashcards yet.")
    else:
        subjects = {}
        for c in st.session_state.flashcards:
            subjects.setdefault(c["subject"], []).append(c)

        for subject, cards in subjects.items():
            with st.expander(f"{subject} ({len(cards)} cards)"):
                for i, c in enumerate(cards):
                    st.markdown(f"**{i+1}.** {c['front']}")

# ---------------------------------------------------------
# PAGE 3: MANAGE FLASHCARDS
# ---------------------------------------------------------
elif page == "📋 Manage Flashcards":
    st.title("📋 Manage Flashcards")

    if len(st.session_state.flashcards) == 0:
        st.info("No flashcards to manage.")
    else:
        st.subheader(f"Total: {len(st.session_state.flashcards)} flashcards")

        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("Search")
        with col2:
            subject_filter = st.selectbox(
                "Filter by Subject",
                ["All"] + sorted(list(set(c["subject"] for c in st.session_state.flashcards)))
            )

        cards = st.session_state.flashcards

        if search:
            cards = [c for c in cards if search.lower() in c["front"].lower() or search.lower() in c["back"].lower()]

        if subject_filter != "All":
            cards = [c for c in cards if c["subject"] == subject_filter]

        if len(cards) == 0:
            st.warning("No matching flashcards.")
        else:
            st.write(f"Showing {len(cards)} flashcards")

            for idx, card in enumerate(cards):
                original_idx = st.session_state.flashcards.index(card)

                with st.expander(f"{card['front']} ({card['subject']})"):
                    st.markdown(f"**Front:** {card['front']}")
                    st.markdown(f"**Back:** {card['back']}")

                    if st.button("Delete", key=f"delete_{original_idx}"):
                        st.session_state.flashcards.pop(original_idx)
                        save_flashcards(st.session_state.flashcards)
                        st.success("Deleted!")
                        st.rerun()

            st.markdown("---")
            st.subheader("Bulk Actions")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete All Flashcards"):
                    st.session_state.flashcards = []
                    save_flashcards([])
                    st.success("All flashcards deleted!")
                    st.rerun()


         
         
         
         
         
         
         
         
         
         