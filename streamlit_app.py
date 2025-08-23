import streamlit as st

# Page settings
st.set_page_config(
    page_title="Karn AI • Portfolio",
    layout="centered"
)

# Sidebar navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Projects", "About"])

# Home Page
if page == "Home":
    st.title("👋 Welcome to Karn's AI Portfolio")
    st.write("This is my personal AI portfolio powered by **Streamlit** 🚀.")
    st.info("Use the sidebar to explore different sections.")

# Projects Page
elif page == "Projects":
    st.title("🛠️ Projects")
    st.subheader("1. AI Dashboard Builder")
    st.write("A tool to generate interactive dashboards from natural language queries.")

    st.subheader("2. Vimana Prototype Research")
    st.write("Researching ancient Vedic science concepts with modern AI/engineering.")

    st.subheader("3. AI Education Platform")
    st.write("An UpGrad-like AI learning platform with auto-generated content.")

# About Page
elif page == "About":
    st.title("ℹ️ About Me")
    st.write("""
    Hi, I'm Karn — a researcher and inventor.  
    I build AI systems, experiment with ancient sciences,  
    and create future-ready platforms.  

    **Contact:**  
    - 📧 Email: yourname@example.com  
    - 🐦 Twitter: [@yourhandle](https://twitter.com)  
    - 💼 LinkedIn: [linkedin.com/in/yourhandle](https://linkedin.com)  
    """)

# ✅ Removed st.experimental_rerun() (deprecated)
# If you ever need rerun, use: from streamlit import rerun; rerun()
