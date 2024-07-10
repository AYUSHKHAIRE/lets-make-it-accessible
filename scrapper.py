from bs4 import BeautifulSoup
import requests as rq
from requests import ConnectionError
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

'''
a function returns the soup object , 
else returns cannot access results 
'''

def get_response(url):
    print(url)
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless Chrome
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome( options=chrome_options)
        
        # Get the URL
        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        
        # Get the page source and close the browser
        page_source = driver.page_source
        driver.quit()
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        return soup
    except Exception as e:
        return f"An error occurred: {str(e)}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}




    

'''
a function telling top results by google 
returns a structure dictionary of 
1 . titles used by google 
2 . urls to hit for website 
3 . provider 
'''
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

'''

a function looks for heading and text

'''

def main_content_scrapper(a_link):
    soup = get_response(a_link)
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

