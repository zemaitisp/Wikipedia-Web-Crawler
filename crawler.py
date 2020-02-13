from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

#will download a given webpage and return the tags and text if avaliable
def get_page_content(url):
    try:
        html_response_text = urlopen(url).read()
        page_content = html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None

#take special characters out of a string
def clean_title(title):
    invalid_characters = ['>', '<', ':', '"', '/', '\\', '|', '?', '*']
    for c in invalid_characters:
        title = title.replace(c, '')
    return title

#will try to find any links on a given webpage with tags
def get_urls(soup):
    links = soup.find_all('a')
    urls = []
    for link in links:
        urls.append(link.get('href'))
    return urls

#will determind if the link works and matches the criteria we wish
def is_valid_url(url):
    if url is None:
        return False
    if re.search('#', url):
        return False
    if re.search('/User', url):
        return False
    if re.search('/Special', url):
        return False
    if re.search('/Talk', url):
        return False
    match = re.search('^/wiki/', url)
    if match:
        return True
    else:
        return False

#formate the taken url into something usable
def reformat_url(url):
    match = re.search('^/wiki/', url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url

#will write the text to a given file at the path
def save(count, text, url, path):
    f = open(path, 'a', encoding = 'utf-8', errors = 'ignore')
    f.write(str(count) + ':' + text + ' ' + url +'\n')
    f.close()


try:
    _create_unverified_https_context = ssl._create_default_https_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#topic is fish and sealife
relatedTerms = ['fish', 'trout', 'shark', 'gills', 'hook', 'bass', 'fly', 'invertebrate', 'flatfish', 'sushi']
queue = ['https://en.wikipedia.org/wiki/Fish', 'https://en.wikipedia.org/wiki/Rainbow_trout' ]
visitedURL = ['https://en.wikipedia.org/wiki/Fish', 'https://en.wikipedia.org/wiki/Rainbow_trout']
pageCount = 1
savedURL = []


while len(queue) != 0:
    #get the next item in the queue
    url = queue.pop(0)
    pageContent = get_page_content(url)
    #if the page is empty go to the next url
    if pageContent is None:
        continue
    termCounter = 0
    #will take all the text out of the webpage and save it as a lower string
    pageMainText = BeautifulSoup(pageContent, 'html.parser').get_text().lower()
    #for every term that the page matches add one to term counter
    for term in relatedTerms:
        if re.search(term, pageMainText):
            termCounter = termCounter + 1
            #if the termcoutner is 2 or more save it to the savedURL string and increment page count
            if termCounter >= 2:
                pageTitle = BeautifulSoup(pageContent, 'html.parser').title.string
                print(pageTitle)
                save(pageCount, pageTitle, url, 'Pages/page.txt')
                savedURL.append(url)
                pageCount = pageCount + 1
                print(pageCount, ": ", url)
                #get out of the loop
                break
    #if the pages gone to and saved exceeds 500 stop
    if pageCount >= 500:
        break
    #get urls from the saved page
    outGoingURLs = get_urls(BeautifulSoup(pageContent, 'html.parser'))

    #if the url found is valid and not visited before, add it to the queue
    for outGoingURL in outGoingURLs:
        if (outGoingURL not in visitedURL) and is_valid_url(outGoingURL):
            visitedURL.append(outGoingURL)
            outGoingURL = reformat_url(outGoingURL)
            queue.append(outGoingURL)



