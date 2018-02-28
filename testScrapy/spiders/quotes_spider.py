import scrapy


class CandidateDetails(scrapy.Spider):
    name = "candidate"
    start_urls = [
        'http://myneta.info/karnataka2013/index.php?action=show_candidates&constituency_id=1',
    ]

    def parse(self, response):
        j = 2
        for quote in response.css('table#table1 tr'):
            Candidate = quote.css('td a::text').extract()
            Total_Assets = quote.css('td:nth-child(6)::text').extract()
            Total_Assets = str(Total_Assets).strip(
                '[]').strip("''")[6:].replace(',', '')
            Winner_or_looser = 'Losser'
            if quote.css('td b font::text').extract():
                Winner_or_looser = 'Winner'
            Criminal_Cases = 0
            if quote.css('td:nth-child(3) span::text').extract():
                Criminal_Cases = str(quote.css(
                    'td:nth-child(3) span::text').extract()).strip('[]').strip("''")
            if Candidate:
                yield {
                    'Candidate': str(quote.css('td a::text').extract()).strip('[]').strip("''"),
                    'Winner_or_looser': Winner_or_looser,
                    'Party': str(quote.css('td:nth-child(2)::text').extract()).strip('[]').strip("''"),
                    'Criminal_Cases': int(Criminal_Cases),
                    'Education': str(quote.css('td:nth-child(4)::text').extract()).strip('[]').strip("''"),
                    'Age': int(str(quote.css('td:nth-child(5)::text').extract()).strip('[]').strip("''")),
                    'Total_Assets': Total_Assets,
                }

        for j in range(2, 233):
            next_page = '/karnataka2013/index.php?action=show_candidates&constituency_id={}'.format(
                ++j)
            next_page = response.urljoin(next_page)
            print('next url=====>>>> {}'.format(next_page))
            yield scrapy.Request(next_page, callback=self.parse)
