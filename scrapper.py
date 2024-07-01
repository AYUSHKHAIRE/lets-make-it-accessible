from bs4 import BeautifulSoup
import requests as rq
from requests import ConnectionError
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


'''
a function returns the soup object , 
else returns cannot access results 
'''


def get_response(url):
    print(url)
    try:
        r = rq.get(url, headers=headers)
        time.sleep(2)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup
        else:
            return "Cannot access the results. Status code: " + str(r.status_code)
    except ConnectionError:
        return "Please check your internet connection"
    except Exception as e:
        return f"An error occurred: {str(e)}"

    

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
