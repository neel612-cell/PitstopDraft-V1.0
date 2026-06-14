import streamlit as st
from database import initialize_database

# Initialize database on startup
initialize_database()

st.set_page_config(
    page_title="PitStop Queue Management",
    page_icon="🏎️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

.hero {
    text-align: center;
    padding: 2rem;
}

.hero h1 {
    color: #f97316;
    font-size: 3rem;
}

.hero p {
    color: white;
    font-size: 1.2rem;
}

.feature-card {
    padding: 1rem;
    border-radius: 12px;
    background-color: #1e293b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🏎️ PitStop Queue Management System</h1>
    <p>Track your turn. Reduce waiting confusion. Improve customer experience.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Problem Statement
st.subheader("Problem Statement")

st.info("""
The current buying system of PitStop (Go Karting Arena) lacks a systematic queue management system to track and display the order of participation on the track. This results in staff facing difficulties in identifying the next person in the queue, while customers are uncertain about when their turn will arrive, leading to crowding, ambiguity, and delays.
""")

st.divider()

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h3>🎟️ Token Generation</h3>
    Generate queue tokens automatically.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h3>📊 Live Queue Tracking</h3>
    Monitor queue status in real time.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>👨‍💼 Staff Dashboard</h3>
    Manage riders efficiently.
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.success("Use the sidebar to navigate between Registration, Dashboard, and Admin pages.")