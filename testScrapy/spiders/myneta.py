import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        elections = [
            'ap09',
            'andhra2014', 'an2004', 'an2009', 'arunachal2014', 'assam2006', 'assam2011', 'assam2016', 'bih2005',
            'bih2010', 'bihar2015', '2008Chhattisgarh', 'chhattisgarh2013', 'dl2008', 'delhi2013', 'delhi2015',
            'goa2007', 'goa2012', 'goa2017', '2007Gujarat', 'gujarat2012', 'Gujarat2017', 'hr2005', 'ha2009',
            'haryana2014', 'him2007', 'hp2012', 'HimachalPradesh2017', 'jk2008', 'jk2014', 'jarka05', 'jarka09',
            'jharkhand2014', 'karnataka2004', 'karnatka2008', 'karnataka2013', 'ker2006', 'kerala2011', 'kerala2016',
            '2008mp', 'mp2013', 'mah2004', 'mh2009', 'maharashtra2014', 'manipur07', 'manipur2012', 'manipur2017',
            '2008Meghalaya', 'meghalaya2013', 'meghalaya2018', '2008Mizoram', 'mizoram2013', '2008Nagaland',
            'nagaland2013', 'nagaland2018', 'orissa2004', 'orissa2009', 'odisha2014', 'pond2006', 'puducherry2011',
            'puducherry2016', 'pb2007', 'pb2012', 'punjab2017', 'rj2008', 'rajasthan2013', 'sikkim2004', 'sikkim2009',
            'sikkim2014', 'tn2006', 'tamilnadu2011', 'tamilnadu2016', 'telangana2014', 'tripura2008', 'tripura2013',
            'tripura2018', 'utk07', 'utt2012', 'uttarakhand2017', 'up2007', 'up2012', 'uttarpradesh2017', 'wb2006',
            'westbengal2011', 'westbengal2016'
        ]
        for election in elections:
            for j in range(1, 500):
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
            # main > div > div.items > a:nth-child(3)
            District = str(response.css(
                "#main div div.items a:nth-child(3)::text").extract()).strip('[]').strip("''")
            District_URL = str(response.css(
                "#main div div.items a:nth-child(3)::attr(href)").extract()).strip('[]').strip("''")
            # main > div > div.items > b
            Constituency = str(response.css(
                "#main div div.items b::text").extract()).strip('[]').strip("''")

            Current_URL = response.request.url
            Election_Id = Current_URL.split('/')[-2]

            State_info = str(response.css(
                '#main div div.items a:nth-child(2)::text').extract_first()).strip('[]').strip("''").strip()
            a = State_info.split(' ')[-1]
            idx = State_info.find(a) + len(a)
            State = State_info[:idx].replace(a, '').strip(' ')

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
                    'State': State,
                    'District': District.strip(),
                    'District_Id': int(District_URL.split("=")[-1]),
                    'Constituency': Constituency.strip(),
                    'Constituency_Id': int(Current_URL.split("=")[-1]),
                    'Candidate_Id': int(Candidate_URL.split("=", 1)[1]),
                    'Candidate': str(quote.css('td a::text').extract()).strip('[]').strip("''").strip(),
                    'Candidate_URL': 'http://myneta.info/{}/{}'.format(Election_Id, Candidate_URL),
                    'Winner_or_loser': Winner_or_loser,
                    'Party': str(quote.css('td:nth-child(2)::text').extract()).strip('[]').strip("''").strip(),
                    'Criminal_Cases': int(Criminal_Cases),
                    'Education': str(quote.css('td:nth-child(4)::text').extract()).strip('[]').strip("''").strip(),
                    'Age': int(str(quote.css('td:nth-child(5)::text').extract()).strip('[]').strip("''")),
                    'Total_Assets': Total_Assets,
                    'Liabilities': int(Liabilities),
                }
