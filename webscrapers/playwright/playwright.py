################################################
#print("Loading docs from URLs...")
#from langchain_community.document_loaders import SpiderLoader
#urls = [
#	'https://docs.cyberark.com/conjur-cloud/latest/en/Content/Resources/_TopNav/cc_Home.htm',
#	'https://cyberark.my.site.com/s/article/Design-Recommendations-for-CyberArk-Secrets-Management-A-Comprehensive-Guide',
#]
#for url in urls:
#	docs += SpiderLoader(api_key="", url=url, mode="crawl").load()

################################################
# https://python.langchain.com/v0.1/docs/use_cases/web_scraping/
print("Scraping websites...")

import asyncio
from playwright.async_api import async_playwright, Playwright

async def scrape_with_playwright(playwright: Playwright, url_base:str, url_start: str, url_filter: str) -> list:
    # Setup priority queue and visited URLs lists
    visited_urls = []
    urls = queue.PriorityQueue()
    urls.put((0.5, url_start)) # seed the to-do list with starting URL

    webkit = playwright.webkit
    browser = await webkit.launch()
    context = await browser.new_context()
    page = await context.new_page()
    docs_corpus = []
    while not urls.empty():
        print(f"URL queue len: {len(list(urls.queue))}")
        _, current_url = urls.get()         # get the page to visit from the list
        visited_urls.append(current_url)    # mark URL as visited
        print("current_url: ", current_url)

        await page.goto(current_url)    
        page_content = await page.inner_text('div')
        docs_corpus.append((current_url, page_content))

        # get filtered link elements on page
        link_elements = []      
        link_locators = await page.locator('div').get_by_role('link').all()
        for _ in link_locators:
            href = await _.get_attribute('href')
            link_elements.append(href)

        # add link elements to to-do list
        for link_element in link_elements:
            url = link_element.split('?',1)[0].split('#',1)[0]
            print(url)
            if re.match(r"^../../", url):
                print("filter match: ", url)
                page_suffix = url.split('../../')[1]
                new_url = url_base + page_suffix
                # if the URL discovered is new
                if new_url not in visited_urls and new_url not in [item[1] for item in urls.queue]:
                    priority_score = 0.5
                    urls.put((priority_score, new_url))
    await browser.close()
    return docs_corpus

async def load_conjur_docs() -> list:
    url_base = 'https://docs.cyberark.com/conjur-cloud/latest/en/Content/'
    url_start = 'https://docs.cyberark.com/conjur-cloud/latest/en/Content/Resources/_TopNav/cc_Home.htm'
    url_filter = "r\'^..'"
    async with async_playwright() as playwright:
        docs = await scrape_with_playwright(playwright, url_base, url_start, url_filter)
    return docs

docs = asyncio.run(load_conjur_docs())
print(docs)