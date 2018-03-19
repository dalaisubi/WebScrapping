import scrapy


class Loksabha(scrapy.Spider):
    name = "loksabha"

    def start_requests(self):
        elections = [
            'loksabha2004',
            'ls2009', 'ls2014',
        ]
        for election in elections:
            for j in range(1, 700):
                print(
                    'http://myneta.info/{}/index.php?action=show_candidates&constituency_id={}'.format(election, j))
                yield scrapy.Request(url='http://myneta.info/{}/index.php?action=show_candidates&constituency_id={}'.format(election, j), callback=self.parse)

    def parse(self, response):
        for quote in response.css('table#table1 tr'):
            Candidate = quote.css('td a::text').extract()
            Candidate_URL = str(quote.css('td a::attr(href)').extract()).strip(
                '[]').strip("''")
            Total_Assets = quote.css('td:nth-child(6)::text').extract()
            Total_Assets = str(Total_Assets).strip(
                '[]').strip("''")[6:].replace(',', '')
            Liabilities = str(
                quote.css("td:nth-child(7)::text").extract()).strip('[]').strip("''")[6:].replace(',', '')
            Constituency = str(response.css(
                "#main div div.items b::text").extract()).strip('[]').strip("''")

            Current_URL = response.request.url
            Election_Id = Current_URL.split('/')[-2]
            State_info = str(response.css(
                '#main div div.items a:nth-child(3)::text').extract_first()).strip('[]').strip("''").strip()
            Winner_or_loser = 'Loser'
            if quote.css('td b font::text').extract():
                Winner_or_loser = 'Winner'
            Criminal_Cases = 0
            if quote.css('td:nth-child(3) span::text').extract():
                Criminal_Cases = str(quote.css(
                    'td:nth-child(3) span::text').extract()).strip('[]').strip("''")

            if Candidate:
                yield {
                    'election_id': Election_Id,
                    'State': State_info,
                    'Constituency': Constituency.strip(),
                    'Constituency_Id': int(Current_URL.split("=")[-1]),
                    'Candidate_Id': int(Candidate_URL.split("=", 1)[1]),
                    'Candidate': str(quote.css('td a::text').extract()).strip(
                        '[]').strip("''").strip(),
                    'Candidate_URL': 'http://myneta.info/{}/{}'.format(
                        Election_Id, Candidate_URL),
                    'Winner_or_loser': Winner_or_loser,
                    'Party': str(quote.css('td:nth-child(2)::text').extract()
                                 ).strip('[]').strip("''").strip(),
                    'Criminal_Cases': int(Criminal_Cases),
                    'Education': str(quote.css('td:nth-child(4)::text').extract()
                                     ).strip('[]').strip("''").strip(),
                    'Age': int(str(quote.css('td:nth-child(5)::text').extract()
                                   ).strip('[]').strip("''")),
                    'Total_Assets': float(Total_Assets),
                    'Liabilities': int(Liabilities),
                }
