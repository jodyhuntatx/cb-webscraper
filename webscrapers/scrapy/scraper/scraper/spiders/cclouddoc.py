#!/usr/bin/python3

from pathlib import Path

import scrapy


class ConjurCloudSpider(scrapy.Spider):
    name = "cclouddoc"

    def start_requests(self):
        urls = [
            "https://docs.cyberark.com/conjur-cloud/latest/en/Content/Resources/_TopNav/cc_Home.htm",
	    "https://docs.cyberark.com/conjur-cloud/latest/en/Content/ConjurCloud/ccl-getstarted-lp.htm",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"ccloud-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
