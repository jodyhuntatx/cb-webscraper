import requests
import queue
import re
import time
import random
import sys
from io import StringIO
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By

# Function to remove tags
def remove_tags(soup):
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    return ' '.join(soup.stripped_strings)

# to store the URLs discovered to visit
# in a specific order
urls = queue.PriorityQueue()
# high priority
urls.put((0.5, "https://docs.cyberark.com/conjur-cloud/latest/en/Content/Resources/_TopNav/cc_Home.htm"))

# to store the pages already visited
visited_urls = []

pd = pd.DataFrame(columns=["Url","Text"])
idx = 0

# Pass the defined options objects to initialize the web driver 
driver = webdriver.Chrome()
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

# until all pages have been visited
while not urls.empty():
    print(f"URL queue len: {len(list(urls.queue))}")

    # get the page to visit from the list
    _, current_url = urls.get()
    # mark URL as visited
    visited_urls.append(current_url)

    # render page
    driver.get(current_url) 
    time.sleep(10)

    # get page source
    page_html = driver.page_source

    # remove html tags and safe to dataframe
    soup = BeautifulSoup(page_html, "html.parser")
    pd.loc[idx] = [current_url, remove_tags(soup)]
    idx += 1

    # get all links on page
    link_elements = driver.find_elements(By.XPATH, "//a[@href]")

    for link_element in link_elements:
        url = link_element.get_attribute("href").split('?',1)[0].split('#',1)[0]

        # if the URL is relative to docs.cyberark.com/conjur-cloud or
        # any of its subdomains
        if re.match(r"^https://docs\.cyberark\.com/conjur-cloud", url):
            # if the URL discovered is new
            if url not in visited_urls and url not in [item[1] for item in urls.queue]:
                # low priority
                priority_score = 1
                # if it is a pagination page
                if re.match(r"^https://docs\.cyberark\.com/conjur-cloud/?$", url):
                    # high priority
                    priority_score = 0.5
                urls.put((priority_score, url))

    # pause the script for a random delay
    # between 1 and 3 seconds
    time.sleep(random.uniform(1, 3)) 

pd.to_csv("./ConjurCloudDocs.csv")
