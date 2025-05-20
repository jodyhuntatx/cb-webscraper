from firecrawl import FirecrawlApp, JsonConfig
from pydantic import BaseModel, Field

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key='fc-811f02a49bce4740a7954e97cbab4101')

data = app.extract([
  'https://docs.cyberark.com/epm/latest/en/content/resources/_topnav/cc_home.htm'
], prompt='Extract all documentation content, do not include footer or navigational content.')
print(data)
