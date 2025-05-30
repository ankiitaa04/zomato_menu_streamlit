import streamlit as st
import pandas as pd
import io
from scraper import get_menu

st.set_page_config(page_title="Zomato Menu Scraper", layout="wide")

# 💅 Custom CSS and Title + input/button flex styling
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
            padding: 10px;
            border-radius: 10px 0 0 10px; /* rounded left corners */
            border-right: none;
        }

        [data-theme="dark"] .stTextInput>div>div>input {
            background-color: #262730;
            color: #ffffff !important;
            border: 1px solid #444;
            border-right: none;
        }

        input::placeholder {
            color: #666 !important;
            opacity: 1 !important;
        }

        [data-theme="dark"] input::placeholder {
            color: #ccc !important;
        }

        label[for="zomato-url-input"] {
            display: block;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 5px;
        }

        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 0 10px 10px 0; /* rounded right corners */
            padding: 0.6em 1.5em;
            border-left: none;
            cursor: pointer;
        }

        /* Flex container for input and button */
        .input-button-row {
            display: flex;
            justify-content: center;
            gap: 0;
            max-width: 700px;
            margin: 0 auto 20px auto;
        }

        .input-button-row > div {
            flex: 1;
        }

        /* Wider scrollable table */
        .scroll-table {
            overflow-x: auto;
            white-space: nowrap;
            max-width: 100%;
        }
    </style>

    <div class="main-title">🍽️ <strong>Zomato Menu Scraper</strong></div>
    <div class="subtitle">Paste any Zomato restaurant URL below to get its full menu instantly</div>
""", unsafe_allow_html=True)

# Label for input
st.markdown('<label for="zomato-url-input">Enter Zomato restaurant URL</label>', unsafe_allow_html=True)

# Input and button side by side
st.markdown('<div class="input-button-row">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    url = st.text_input("", placeholder="https://www.zomato.com/...", key="zomato-url-input", label_visibility="collapsed")

with col2:
    scrape = st.button("Scrape Menu")

st.markdown('</div>', unsafe_allow_html=True)

# 🚀 Scrape Logic
if scrape:
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

                    # Convert to DataFrame
                    df = pd.DataFrame(data)
                    columns = ["restaurant", "category", "sub_category", "item_name", "price", "desc", "dietary_slugs"]
                    df = df[columns]

                    # Wider scrollable table
                    st.markdown('<div class="scroll-table">', unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download CSV
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
