#-------------------------------------------------------------------------
# AUTHOR: Anson Ng
# FILENAME: scraper.py
# SPECIFICATION: Crawls the Circular Links section of TestingURL.dev using the
#                crawler pseudocode from Question 1 (frontier + seen). Prints the
#                <h1> text of every crawled page and, at the end, all URLs in seen.
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 1 hour 42 minutes
#-------------------------------------------------------------------------

# import libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag

# seed variables
seed = "https://testingurl.dev/scraping/links/circular"
baseURL = "https://testingurl.dev"

# create frontier
frontier = [seed]
seen = [seed]

# crawl frontier until empty
while frontier:

    url = frontier.pop(0)

    # retrieve and parse web page
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as error:
        print("Could not retrieve", url, "-", error)
        continue
    soup = BeautifulSoup(response.text, "html.parser")

    # print text in h1 element
    h1 = soup.find("h1")
    if h1 is not None:
        print(h1.get_text(strip=True))

    # extract and process hyperlinks
    links = []
    for a in soup.find_all("a", href=True):

        # conver tot absolute URL
        absolute = urljoin(url, a["href"])

        # remove fragment
        absolute = urldefrag(absolute)[0]

        # look for seedurl links
        if absolute.startswith(seed) and absolute not in links:
            links.append(absolute)

    # sortByPageId()
    links.sort()

    for link in links:
        if link not in seen:
            seen.append(link)
            frontier.append(link)

# print all URLs
for url in seen:
    print(url)
