import scrapy
import re
import json


class OtherElection(scrapy.Spider):
    name = "otherelection"

    def start_requests(self):
        json_f = './loksabha.json'
        with open(json_f) as json_file:
            data = json.load(json_file)
            for index, candidate in enumerate(data):
                url1 = candidate['Candidate_URL']
                print(url1)
                yield scrapy.Request(url=url1, callback=self.parse)

    def parse(self, response):
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + response.request.url)
        url_ = None
        for quotes in response.css('#table3'):
            print('Before {}'.format(response.request.url))
            Compare_URL = str(quotes.css('tr:nth-last-child(1) td a::attr(href)').extract()).strip(
                '[]').strip("''")
            last_year = str(quotes.css(
                'tr:nth-child(3) td:nth-child(1) b::text').extract()).strip(
                '[]').strip("''")
            last_year_assets = validator(str(quotes.css(
                'tr:nth-child(3) td:nth-child(2) b::text').extract()).strip(
                '[]').strip("''").replace(',', '')[2:])
            last_year_case = validator(str(quotes.css(
                'tr:nth-child(3) td:nth-child(3)::text').extract()).strip(
                '[]').strip("''"))
            secondLast_year = str(quotes.css(
                'tr:nth-child(4) td:nth-child(1) b::text').extract()).strip(
                '[]').strip("''")
            test = str(quotes.css(
                'tr:nth-child(4) td:nth-child(2) b::text').extract()).strip(
                '[]').strip("''").replace(',', '')[2:]
            print('>>>>>> {} : {}'.format(test, type(test)))

            secondLast_year_assests = validator(str(quotes.css(
                'tr:nth-child(4) td:nth-child(2) b::text').extract()).strip(
                '[]').strip("''").replace(',', '')[2:])
            secondLast_year_case = validator(str(quotes.css(
                'tr:nth-child(4) td:nth-child(3)::text').extract()).strip(
                '[]').strip("''"))
            print('after {}'.format(response.request.url))
            if Compare_URL:
                url_ = 'http://myneta.info/{}'.format(Compare_URL)
            Candidate_URL = response.request.url
            # print("---------------------- " + Compare_URL)
            if secondLast_year_assests != 0:
                percent_change_asset = round((
                    (last_year_assets - secondLast_year_assests) * 100) / secondLast_year_assests)
            else:
                percent_change_asset = 0
            if secondLast_year_case != 0:
                percent_change_criminal_case = round((
                    (last_year_case - secondLast_year_case) * 100) / secondLast_year_case)
            else:
                percent_change_criminal_case = 0

            print(last_year, last_year_assets, last_year_case)
            print(secondLast_year, secondLast_year_assests, secondLast_year_case)
            yield {
                'last_year': last_year,
                'last_year_assets': last_year_assets,
                'last_year_case': last_year_case,

                'secondLast_year': secondLast_year,
                'secondLast_year_assests': secondLast_year_assests,
                'secondLast_year_case': secondLast_year_case,

                'last_year_assets': last_year_assets,
                'secondLast_year_assests': secondLast_year_assests,
                'percent_change_asset': percent_change_asset,
                'percent_change_criminal_case': percent_change_criminal_case,

                'compare_url': url_,
                'candidate_url': Candidate_URL,
            }


def validator(data):
    if data != '':
        return typeChecker(float(data))
    return 0


def typeChecker(data):
    if data < 100:
        return int(data)
    return data
