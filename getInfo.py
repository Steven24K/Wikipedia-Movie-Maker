import requests
from bs4 import BeautifulSoup
import urllib, json


def getWikiInfo(name, paragraphs_amount = 5, language = 'en'):
    url = 'https://' + language + '.wikipedia.org/wiki/' + name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('info from :: ' + url)
    soup.table.extract()
    soup.h1.extract()
    soup.find(id='siteSub').extract()
    soup.find(id='contentSub').extract()
    soup.find(id='jump-to-nav').extract()
    for i in soup.find_all('a', {'class': 'mw-jump-link'}): 
        i.extract()
        
    soup.find('div', id='toc').extract()
    
    paragraphs = soup.find_all('p')
    
    max = paragraphs_amount
    cnt = 0
    result = ''
    if max > len(paragraphs): max = len(paragraphs) - 1
    for p in paragraphs: 
        if cnt == max: return result
        result += p.get_text()
        cnt += 1
    #TODO: Remove source number from paragraphs [0]
    return result



def getGifImages(key, name, limit = 10, offset = 0, rating = 'g', lang = 'en'):
    url = 'https://api.giphy.com/v1/gifs/search?api_key={}&q={}&limit={}&offset={}&rating={}&lang={}'.format(key,name, limit, offset, rating, lang)
    response = requests.get(url)

    return list(map(lambda gif: gif['images']['original']['url'], json.loads(response.text)['data']))

