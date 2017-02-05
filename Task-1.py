import requests
from bs4 import BeautifulSoup
import re
import time

VL, D1, D2, D3, D4, D5 = [], [], [], [], [], []

MS = []


#################################################################################

# pg_crawler : URL -> LIST
# GIVEN: a URL
# RETURNS: List of URLs in the given URL that match given criteria in the task

def pg_crawler(url):
    links, links_pg = [], []
    VL.append(url)
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
            href = "https://en.wikipedia.org" + link.get('href')
            hlist = href.split('#')
            links.append(str(hlist[0]))

######################################################################
# Below code is used to download contents from the URLs
#    name = str(list_links[counter])[30:].replace('/', '-') + ".html"
#    f = open(name, 'w')
#    f.write(str(body))
#    f.close()
######################################################################

    # Remove Duplicates within page
    for i in links:
            if i not in links_pg:
                if len(i) > 1:
                    if i not in VL:
                        links_pg.append(i)

    # Add Unique links to Frontier
    for i in links_pg:
        if i not in MS:
            MS.append(i)

    return links_pg


# get_links : LIST -> URL
# GIVEN: a LIST of URLs
# RETURNS: a URL that needs to crawled next

def get_links(list):
    for i in list:
        if i not in VL:
            return i
    if list == D1:
        if len(D1) < 1000:
            return get_links(D2)
    if list == D2:
        if len(D2) < 1000:
            return get_links(D3)
    if list == D3:
        if len(D3) < 1000:
            return get_links(D4)
    if list == D4:
        if len(D4) < 1000:
            return get_links(D5)
    return "No links"


# Main function
def main_crawler(seed):
    D1.append(seed)
    MS.append(seed)

    # Crawl till we have 1000 unique links
    while len(MS) < 1000:
        # Get URL that needs to be crawled next
        pg_url = get_links(D1)

        if pg_url == "No links":
            print "No more links to crawl"
            break
        else:
            if pg_url in D1:
                d1_urls = pg_crawler(pg_url)
                for x in d1_urls:
                    D2.append(x)
            elif pg_url in D2:
                d2_urls = pg_crawler(pg_url)
                for y in d2_urls:
                    if (y not in D1) and (y not in D2):
                        D3.append(y)
            elif pg_url in D3:
                d3_urls = pg_crawler(pg_url)
                for z in d3_urls:
                    if (z not in D2) and (z not in D3):
                        D4.append(z)
            elif pg_url in D4:
                d4_urls = pg_crawler(pg_url)
                for x in d4_urls:
                    if (x not in D3) and (x not in D4):
                        D5.append(x)

    sl = 1
    f = open('Task-1-E-URLs.txt', 'w')
    for i in MS[0:1000]:
        row =  str(sl) + " " + str(i) + "\n"
        f.write(row)
        sl += 1
    f.close()

main_crawler('https://en.wikipedia.org/wiki/Sustainable_energy')


