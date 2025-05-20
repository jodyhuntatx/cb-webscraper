#!/usr/bin/python3

from io import StringIO
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Function to remove tags
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

url_list = [
"https://docs.cyberark.com/epm/latest/en/content/resources/_topnav/cc_home.htm"
]

pd = pd.DataFrame(columns=["Url","Text"])
for i in range(len(url_list)):
    read_url = url_list[i]
    req = Request(url=read_url, headers={'User-Agent': 'Mozilla/5.0'})
    mybytes = urlopen(req).read()
    mystr = mybytes.decode("utf8")
    pd.loc[i] = [read_url, remove_tags(mystr)]

pd.to_csv("./epm-outcome.csv")
