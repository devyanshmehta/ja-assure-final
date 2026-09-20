import os
import streamlit as st
from google import genai

# 1. Page Configuration (Cyber-Neon Theme)
st.set_page_config(
    page_title="JA Assure",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Cyber-Neon CSS Injection
st.markdown("""
<style>
    /* Dark Theme Grid Background */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(#1f293d 1px, transparent 1px);
        background-size: 24px 24px;
        color: #e2e8f0;
    }
    
    /* Neon Headers */
    h1, h2, h3 {
        color: #00f0ff !important;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }
    
    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(8px);
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #39ff14 !important;
        font-size: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Secure API Key Retrieval
# Checks Streamlit Secrets first, then local environment variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is not configured! Please set it in Streamlit Cloud Secrets or your .env file.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# 4. App UI & Logic
st.title("🛡️ JA Assure — Executive Metrics & Agent")

# Metrics Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="System Status", value="ACTIVE", delta="100% Operational")
with col2:
    st.metric(label="Threat Index", value="LOW", delta="-12%", delta_color="inverse")
with col3:
    st.metric(label="Human-in-Loop Reviews", value="14 Pending", delta="Requires Action")

st.divider()

# Interactive Prompt Input
st.subheader("🤖 Brain Agent Control")
user_input = st.text_area("Enter input for analysis or task generation:", placeholder="Type here...")

if st.button("Run Brain Agent"):
    if user_input.strip():
        with st.spinner("Processing request through Gemini agent..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_input,
                )
                st.success("Analysis Complete")
                st.markdown("### Agent Response")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error executing agent task: {e}")
    else:
        st.warning("Please enter a prompt before running the agent.")