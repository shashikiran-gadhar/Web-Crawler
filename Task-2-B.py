import requests
from bs4 import BeautifulSoup
import re
import time

VL = []


# dfs_crawler : URL -> URL
# GIVEN: URL
# RETURNS: a URL that needs to crawled next

def dfs_crawler(url, depth, key):
    if len(VL) > 1000:
        return
    if depth > 5:
        return
    if url in VL:
        return
    VL.append(url)
    links = pg_crawler(url, key)
    for i in links:
        dfs_crawler(i, depth + 1, key)
    return True


#################################################################################

# pg_crawler : URL -> LIST
# GIVEN: a URL
# RETURNS: List of URLs in the given URL that match given criteria in the task

def pg_crawler(url, key):
    links, links_pg = [], []
    s = " "
    # To Preserve Politeness Policy
    time.sleep(1)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    # Get Body from Page
    body = soup.find('div', {'id': 'mw-content-text'})

    # Remove 'References' from Page
    if len(soup.find('ol', class_='references') or ()) > 1:
        soup.find('ol', class_='references').decompose()

    # Get all links in page that match given pattern in task
    for link in body.find_all('a', {'href': re.compile("^/wiki")}):
        if ':' not in link.get('href'):
            try:
                s = str(link.text)
            except UnicodeEncodeError as e:
                error = e

            if (key.lower() in str(link.get('href')).lower()) or (key.lower() in s.lower()):
                href = "https://en.wikipedia.org" + link.get('href')
                hlist = href.split('#')
                links.append(str(hlist[0]))


    # Remove Duplicates within page
    for i in links:
        if i not in links_pg:
            if len(i) > 1:
                links_pg.append(i)

    return links_pg


# Main function

def main_crawler(seed,key):
    # Crawl URLs using DFS Algo
    dfs_crawler(seed, 1, key)
    sl = 1
    f = open('Task-2-B-URLs.txt', 'w')
    for i in VL:
        row = str(sl) + " " + str(i) + "\n"
        f.write(row)
        sl += 1
    f.close()



main_crawler('https://en.wikipedia.org/wiki/Sustainable_energy',"solar")
