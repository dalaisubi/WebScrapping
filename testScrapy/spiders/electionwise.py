import scrapy
import re
import json


class ElectionWise(scrapy.Spider):
    name = "compareurl"

    def start_requests(self):
        json_f = './retest.json'
        with open(json_f) as json_file:
            data = json.load(json_file)
            # for index, candidate in enumerate(data):
            #     print(int(candidate['Total_Assets']))
            #     if index > 10:
            #         break
            #     # yield scrapy.Request(url=url, callback=self.parse)
            for index, candidate in enumerate(data):
                url1 = candidate['Candidate_URL']
                print(url1)
                yield scrapy.Request(url=url1, callback=self.parse)

    def parse(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + response.request.url)
        for quotes in response.css('table#table3 tbody tr'):
            a = quotes.css('td a::attr(href)').extract_first()
            Compare_URL = str(response.css('tr td a::attr(href)').extract()).strip(
                '[]').strip("''")
            Candidate_URL = response.request.url
            print("---------------------- " + a)

            yield {
                # 'http://myneta.info{}'.format(Compare_URL),
                'Compare_URL': a,
                'Candidate_URL': Candidate_URL,  # Candidate_URL,
            }
# table3 > tbody > tr:nth-child(5) > td > a
