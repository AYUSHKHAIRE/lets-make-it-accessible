import streamlit as st
import scrapper as sc
import pandas as pd
from gtts import gTTS
import io
import base64


# Function to generate and return the audio content as base64 string
def text_to_speech_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    return f"data:audio/mp3;base64,{b64}"


# Function to handle navigation
def nav_page(page):
    st.session_state.page = page


# Sidebar with navigation links
st.sidebar.title("Navigation")
if st.sidebar.button("Home               "):
    nav_page("Home")
if st.sidebar.button("fast-search        "):
    nav_page("fast-search")

# Define the default page
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Display content based on the selected page
if st.session_state.page == "Home":
    st.title("Welcome to My Website")

elif st.session_state.page == "fast-search":
    search = st.text_input("Search something ...")
    # Check if search term is not empty and has changed
    if search:
        search_ = search.replace(' ','+')
        # Use a spinner while fetching search results
        with st.spinner(f'Fetching search results for {search} ....'):
            response = sc.get_response(
                f'https://www.google.com/search?q={search_}')

        if isinstance(response, str):
            st.error(response)
        else:
            data_result = sc.google_search(response)
            if data_result['snippets']:
                df = pd.DataFrame(data_result)

                # Display the DataFrame with an "Announce" button for each row
                for i, row in df.iterrows():
                    st.markdown(f'### {row["providers"]}')
                    st.write(row['snippets'])
                    if st.button(f"Announce {i+1}", key=f"announce_{i}"):
                        audio_data = text_to_speech_base64(row['snippets'])
                        st.markdown(
                            f'<audio controls autoplay src="{audio_data}"></audio>',
                            unsafe_allow_html=True,
                        )
                    links_length = len(row['links'])
                    st.write(f'{links_length} links available')
                    for j, a_link in enumerate(row['links']):
                        try:
                            website = a_link.split('.')[1]
                            website = website.split('/')[-1]
                            if st.button(f"Explore link {j+1} ({website})", key=f"explore_{i}_{j}"):
                                st.write(f"[{website}]({a_link})")
                                result = sc.main_content_scrapper(a_link)
                                if st.button(f"Announce the {website} content :", key=f"Announce the {website} content :"):
                                    audio_data = text_to_speech_base64(result)
                                    st.markdown(
                                        f'<audio controls autoplay src="{audio_data}"></audio>',
                                        unsafe_allow_html=True,
                                    )
                                st.write(result)
                            st.write("---")
                        except:
                            continue
            else:
                st.warning("No results found.")


