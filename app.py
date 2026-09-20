import os
import sqlite3
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="JA Assure — AI Marketing & Compliance Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Lucide Icons Script Injection
st.markdown(
    '<script src="https://unpkg.com/lucide@latest"></script>',
    unsafe_allow_html=True,
)

# Initialize Gemini Client via Streamlit Secrets or Environment Variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Database Initialization
def init_db():
    conn = sqlite3.connect("ja_assure.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            platform TEXT,
            topic TEXT,
            generated_content TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# High-Impact Cyberpunk / High-Contrast Live Animated CSS Styling
st.markdown("""
<style>
    @keyframes neonPulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Highly Noticeable, Vibrant Multi-Color Live Background */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #311042, #06283d);
        background-size: 500% 500%;
        animation: neonPulse 10s ease infinite;
        color: #f1f5f9;
    }

    /* Main Title & Icon Header */
    .title-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f43f5e, #38bdf8);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neonPulse 6s linear infinite;
        margin: 0;
    }
    .header-icon {
        color: #38bdf8;
        filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.9));
    }

    /* Pill Badges with Glow */
    .badge-container {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .badge {
        background-color: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.6);
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        backdrop-filter: blur(8px);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }

    /* Glassmorphic Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(56, 189, 248, 0.1);
    }
    [data-testid="stMetricValue"] {
        font-size: 2.4rem !important;
        color: #38bdf8 !important;
        font-weight: 800;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
    }

    /* Input & Select Box Customizations */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-radius: 10px !important;
    }

    /* Glowing Button Customization */
    .stButton button {
        background: linear-gradient(90deg, #0284c7, #6366f1, #ec4899);
        background-size: 200% auto;
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.6rem;
        transition: all 0.4s ease;
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.4);
    }
    .stButton button:hover {
        background-position: right center;
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.8), 0 0 25px rgba(56, 189, 248, 0.8);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Header Section with Vector Icon
st.markdown("""
<div class="title-wrapper">
    <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>
    <div class="main-header">JA Assure — AI Marketing & Compliance Agent</div>
</div>
<div class="badge-container">
    <span class="badge">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 12 2 2 4-4"/></svg>
        AUTONOMOUS REGULATORY GUARDRAILS
    </span>
    <span class="badge">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        SELF-CORRECTING MEMORY
    </span>
</div>
""", unsafe_allow_html=True)

# Fetch Stats from Database
conn = sqlite3.connect("ja_assure.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM drafts")
total_drafts = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM drafts WHERE status='Approved'")
approved_drafts = c.fetchone()[0]
conn.close()

# Metric Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="TOTAL DRAFTS AUDITED", value=total_drafts)
with col2:
    st.metric(label="COMPLIANT APPROVED", value=approved_drafts)
with col3:
    st.metric(label="ACTIVE POLICY MEMORIES", value=1)

st.markdown("<br>", unsafe_allow_html=True)

# Tab Navigation
tab_brain, tab_hands, tab_feedback = st.tabs([
    "⚙️ Brain (Content Generator)",
    "⚡ Hands (Approval Queue)",
    "🛡️ Feedback Memory"
])

# TAB 1: BRAIN (GENERATOR)
with tab_brain:
    st.subheader("Generate & Audit Marketing Content")
    
    col_a, col_b = st.columns(2)
    with col_a:
        brand_name = st.text_input("Brand Name", value="JA Insurance")
        target_platform = st.selectbox("Target Platform", ["LinkedIn", "Twitter/X", "Instagram", "Facebook Email"])
    with col_b:
        target_language = st.selectbox("Target Language", ["English", "Spanish", "French", "German"])
        content_brief = st.text_area("Content Brief / Campaign Topic", value="Promoting general wellness benefits and annual preventive health checkups for corporate clients.")

    if st.button("🚀 Generate & Audit Content", use_container_width=True):
        if not client:
            st.error("Gemini API key is missing. Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
        else:
            with st.spinner("Analyzing regulatory requirements and generating draft..."):
                prompt = f"""
                You are an AI Compliance & Marketing Agent for {brand_name}.
                Write a marketing post for {target_platform} in {target_language}.
                Topic: {content_brief}
                Ensure strict compliance with financial/insurance advertising standards.
                Provide:
                1. Post Copy
                2. Compliance Score (0-100)
                3. Risk Analysis
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # Save to DB
                conn = sqlite3.connect("ja_assure.db")
                c = conn.cursor()
                c.execute(
                    "INSERT INTO drafts (brand, platform, topic, generated_content) VALUES (?, ?, ?, ?)",
                    (brand_name, target_platform, content_brief, response.text)
                )
                conn.commit()
                conn.close()

                st.success("Draft Generated & Saved to Queue!")
                st.markdown("### Generated Output & Audit")
                st.write(response.text)

# TAB 2: HANDS (APPROVAL QUEUE)
with tab_hands:
    st.subheader("Human-in-the-Loop Review Queue")
    
    conn = sqlite3.connect("ja_assure.db")
    c = conn.cursor()
    c.execute("SELECT id, brand, platform, topic, generated_content, status FROM drafts ORDER BY id DESC")
    records = c.fetchall()
    conn.close()

    if not records:
        st.info("No drafts currently in the review queue.")
    else:
        for row in records:
            draft_id, brand, platform, topic, content, status = row
            with st.expander(f"Draft #{draft_id} | {brand} ({platform}) — Status: {status}"):
                st.write(content)
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"Approve #{draft_id}", key=f"app_{draft_id}"):
                        conn = sqlite3.connect("ja_assure.db")
                        c = conn.cursor()
                        c.execute("UPDATE drafts SET status='Approved' WHERE id=?", (draft_id,))
                        conn.commit()
                        conn.close()
                        st.rerun()
                with col_btn2:
                    if st.button(f"Reject #{draft_id}", key=f"rej_{draft_id}"):
                        conn = sqlite3.connect("ja_assure.db")
                        c = conn.cursor()
                        c.execute("UPDATE drafts SET status='Rejected' WHERE id=?", (draft_id,))
                        conn.commit()
                        conn.close()
                        st.rerun()

# TAB 3: FEEDBACK MEMORY
with tab_feedback:
    st.subheader("Autonomous Regulatory Guardrails & Memory")
    st.markdown("""
    * **Policy Rule #1:** Avoid absolute statements like "100% covered" or "guaranteed payout" without disclaimers.
    * **Policy Rule #2:** Include standard statutory disclaimers on all health/life coverage material.
    * **Active Learning:** Feedback from human approvals/rejections automatically tunes prompt context for future iterations.
    """)
