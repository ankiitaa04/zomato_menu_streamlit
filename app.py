import streamlit as st
import pandas as pd
import io
from scraper import get_menu

st.set_page_config(page_title="Zomato Menu Scraper", layout="wide")

# 💅 Custom CSS and Title
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }

        .main-title {
            font-family: 'Segoe UI', sans-serif;
            font-size: 3em;
            font-weight: 800;
            color: #ff4b4b;
            text-align: center;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #555;
            margin-bottom: 30px;
        }

        /* Input box customization */
        .stTextInput>div>div>input {
            background-color: #ffffff;
            color: #000000 !important;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
        }

        [data-theme="dark"] .stTextInput>div>div>input {
            background-color: #262730;
            color: #ffffff !important;
            border: 1px solid #444;
        }

        /* Placeholder styling */
        input::placeholder {
            color: #666 !important;
            opacity: 1 !important;
        }

        [data-theme="dark"] input::placeholder {
            color: #ccc !important;
        }

        /* Center-align label */
        label[for="zomato-url-input"] {
            display: block;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
        }

        /* Button styling */
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6em 1.5em;
            margin-top: 10px;
        }

        /* Scrollable table */
        .scroll-table {
            overflow-x: auto;
            white-space: nowrap;
        }
    </style>

    <div class="main-title">🍽️ Zomato Menu Scraper</div>
    <div class="subtitle">Paste any Zomato restaurant URL below to get its full menu instantly</div>
""", unsafe_allow_html=True)

# 📥 URL Input — wrapped with centered label
st.markdown('<label for="zomato-url-input">Enter Zomato restaurant URL</label>', unsafe_allow_html=True)
url = st.text_input("", placeholder="https://www.zomato.com/...", key="zomato-url-input")

# 🚀 Scrape Menu button centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Scrape Menu"):
        if not url:
            st.warning("Please enter a valid Zomato URL.")
        elif "zomato.com" not in url.lower():
            st.warning("Please enter a valid Zomato restaurant URL.")
        else:
            with st.spinner("Scraping menu..."):
                try:
                    data = get_menu(url, save=False)
                    if not data:
                        st.error("No menu found or scraping failed.")
                    else:
                        st.success(f"Scraped {len(data)} items! ✅")

                        # Convert to DataFrame and order columns
                        df = pd.DataFrame(data)
                        columns = ["restaurant", "category", "sub_category", "item_name", "price", "desc", "dietary_slugs"]
                        df = df[columns]

                        # Show scrollable table
                        st.markdown('<div class="scroll-table">', unsafe_allow_html=True)
                        st.dataframe(df, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Prepare CSV
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        csv_data = csv_buffer.getvalue()

                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_data,
                            file_name="zomato_menu.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error: {e}")
