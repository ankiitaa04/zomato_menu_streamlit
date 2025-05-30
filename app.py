import streamlit as st
import pandas as pd
import io
from scraper import get_menu  # Your scraper function

st.set_page_config(page_title="Zomato Menu Scraper", layout="wide")

# 💄 Custom Styling and HTML
st.markdown("""
    <style>
        /* Main Page Styling */
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

        input::placeholder {
            color: #999 !important;
            opacity: 1 !important;
        }

        [data-theme="dark"] input::placeholder {
            color: #ccc !important;
        }

        .stTextInput>div>div>input {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
        }

        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6em 1.5em;
            margin-top: 10px;
        }

        .copy-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
        }

        .copy-button:hover {
            background-color: #45a049;
        }
    </style>

    <div class="main-title">🍽️ <strong>Zomato Menu Scraper</strong></div>
    <div class="subtitle">Paste any Zomato restaurant URL below to get its full menu instantly</div>
""", unsafe_allow_html=True)

# 📥 Centered Input and Scrape Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    url = st.text_input("Enter Zomato restaurant URL", placeholder="https://www.zomato.com/...")
    if st.button("Scrape Menu"):
        url = url.strip()
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
                        st.success(f"✅ Successfully scraped **{len(data)}** menu items!")

                        # Convert to DataFrame
                        df = pd.DataFrame(data)
                        columns = ["restaurant", "category", "sub_category", "item_name", "price", "desc", "dietary_slugs"]
                        df = df[columns]

                        restaurant_name = df['restaurant'].iloc[0] if 'restaurant' in df.columns else "Restaurant"
                        st.markdown(f"### 🍴 Menu for **{restaurant_name}**")

                        st.dataframe(df, use_container_width=True)

                        # CSV string for download/copy
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        csv_data = csv_buffer.getvalue()

                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_data,
                            file_name=f"zomato_menu_{timestamp}.csv",
                            mime="text/csv"
                        )

                        # 📋 Copy All Button using JavaScript
                        st.markdown(f"""
                            <br>
                            <button class="copy-button" onclick="navigator.clipboard.writeText(`{csv_data}`)">
                                📋 Copy All
                            </button>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    st.error(f"Error: {e}")
