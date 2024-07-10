from bs4 import BeautifulSoup
import requests
from requests import ConnectionError
import streamlit as st
import time

def get_response(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            return f"Cannot access the results. Status code: {response.status_code}"
    except ConnectionError:
        return "Please check your internet connection"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def google_search(soup):
    results = soup.find_all('div', {'class': 'g'})
    dict_to_return = {
        'snippets': [],
        'links': [],
        'providers': [],
    }
    for r in results:
        # results snippet
        snippet = r.find('div', {'class': 'kb0PBd cvP2Ce A9Y9g'})
        snippet2 = r.find('span', {'class': 'hgKElc'})
        final_snp_to_ret = None
        if snippet:
            final_snp_to_ret = snippet.get_text()
        if snippet2:
            final_snp_to_ret = snippet2.get_text()
        # links
        links_results = []
        a_s = r.find_all('a')
        for a in a_s:
            if 'search' in a['href']:
                continue
            else:
                links_results.append(a['href'])
        # provider
        snippet3 = r.find('span', {'class': 'VuuXrf'})
        if snippet3:
            snippet3 = snippet3.get_text()
            dict_to_return['snippets'].append(final_snp_to_ret)
            dict_to_return['links'].append(links_results)
            dict_to_return['providers'].append(snippet3)

    return dict_to_return

def main_content_scrapper(a_link):
    soup = get_response(a_link)
    if isinstance(soup, str):
        return soup

    # Remove unwanted sections like navigation and footer
    for tag in soup(['nav', 'footer', 'script', 'style']):
        tag.decompose()

    markdown_content = ""

    # Extract headers, paragraphs, and other relevant content
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'div']):
        match element.name:
            case 'h1':
                markdown_content += f"# {element.text}\n\n"
            case 'h2':
                markdown_content += f"## {element.text}\n\n"
            case 'h3':
                markdown_content += f"### {element.text}\n\n"
            case 'h4':
                if len(element.text.split(' ')) > 2:
                    markdown_content += f"#### {element.text}\n\n"
            case 'h5':
                if len(element.text.split(' ')) > 2:
                    markdown_content += f"##### {element.text}\n\n"
            case 'h6':
                if len(element.text.split(' ')) > 2:
                    markdown_content += f"###### {element.text}\n\n"
            case 'p':
                if len(element.text.split(' ')) > 7:
                    markdown_content += f"{element.text}\n\n"
            case 'ul':
                for li in element.find_all('li'):
                    markdown_content += f"- {li.text}\n"
                markdown_content += "\n"
            case 'ol':
                for i, li in enumerate(element.find_all('li'), 1):
                    markdown_content += f"{i}. {li.text}\n"
                markdown_content += "\n"
            case 'div':
                if len(element.text.split(' ')) > 7 and len(element.text) > 10:
                    markdown_content += f"{element.text}\n\n"

    return markdown_content

# Streamlit interface
st.title("Selenium and BeautifulSoup with Streamlit")

url = st.text_input("Enter URL:", "https://example.com")
if st.button("Fetch Data"):
    response = get_response(url)
    if isinstance(response, BeautifulSoup):
        st.write(response.prettify())  # Print the prettified HTML
    else:
        st.write(response)
