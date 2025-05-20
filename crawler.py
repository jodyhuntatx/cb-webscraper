import requests
import queue
import re
import time
import random
import sys
from io import StringIO
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By

OUTFILE_NAME="./EPM-kb-articles.csv"
VERSION="25\\.4\\.0"
PRODUCT_NAME="epm"

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
#urls.put((0.5, "https://docs.cyberark.com/epm/latest/en/Content/Resources/_TopNav/cc_Home.htm"))
urls.put((0.5, "https://community.cyberark.com/s/article/Introducing-the-Endpoint-Privilege-Manager-Success-Path#Meet-Requirements-Centralized-Visibility"))
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
    print(f"current_url: {current_url}")
    # mark URL as visited
    visited_urls.append(current_url)

    # get text from unrendered html
    try:
        req = Request(url=current_url, headers={'User-Agent': 'Mozilla/5.0'})
        mybytes = urlopen(req).read()
    except HTTPError as e:
        # do something
        print(f"\nHTTPError: {current_url}\nError code: {e.code}\n")
        continue
    except URLError as e:
        # do something
        print(f"\nURLError: {current_url}\nURLError.reason: {e.reason}\n")
        continue

    # decode page text
    try:
      mystr = mybytes.decode("utf8")
    except UnicodeDecodeError:
      print(f"\nUnicodeDecodeError: {current_url}\n")
      continue

    # parse HTML & extract text w/o tags
    soup = BeautifulSoup(mystr, "html.parser")
    mystr_tagless = remove_tags(soup)
    pd.loc[idx] = [current_url, mystr_tagless]
    idx += 1

    # render page to get links in dynamic js content
    driver.get(current_url) 
    time.sleep(3)

    # get all links on page
    link_elements = driver.find_elements(By.XPATH, "//a[@href]")

    for link_element in link_elements:
        url = link_element.get_attribute("href").split('?',1)[0].split('#',1)[0]

        # if the URL is relative to docs.cyberark.com/CYBR_PRODUCT or
        # any of its subdomains
        #version_pattern=f"^https://docs\.cyberark\.com/{PRODUCT_NAME}/{VERSION}/en"
        #latest_pattern=f"^https://docs\.cyberark\.com/{PRODUCT_NAME}/latest/en"
        latest_pattern="^https://community.cyberark.com/s/article/EPM"
        if (re.match(latest_pattern, url)
            and not re.match(r"png$", url)):
            # if the URL discovered is new
            if url not in visited_urls and url not in [item[1] for item in urls.queue]:
                # low priority
                priority_score = 1
                # if it is a pagination page
                if re.match(rf"^https://docs\.cyberark\.com/{PRODUCT_NAME}/?$", url):
                    # high priority
                    priority_score = 0.5
                urls.put((priority_score, url))

    # pause the script for a random delay
    # between 1 and 3 seconds
    time.sleep(random.uniform(1, 3)) 

pd.to_csv(OUTFILE_NAME)
