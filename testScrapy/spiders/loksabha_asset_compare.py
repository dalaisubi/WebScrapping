import scrapy
import re
import json


class ElectionWise(scrapy.Spider):
    name = "cadidateAssetsCompare"

    def start_requests(self):
        json_loksabha = "C:/scrapy/WebScrapping/testScrapy/loksabha.json"
        with open(json_loksabha) as json_loksabha:
            loksabha_urls = json.load(json_loksabha)
            for loksabha_url in loksabha_urls:
                url = loksabha_url['Candidate_URL']
                slide = '----------------------'
                # print(url, slide)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        i = 3
        for asset in response.css('#table3 tr'):
            Candidate_URL = response.request.url
            Compare_URL = str(asset.css('td a::attr(href)').extract()).strip(
                '[]').strip("''")

            if Compare_URL:
                c_url = 'http://www.myneta.info' + Compare_URL
                slide = '-----------'
                print(slide, Compare_URL)

                yield {
                    'Candidate_URL': Candidate_URL,
                    'Compare_URL': c_url,
                }
