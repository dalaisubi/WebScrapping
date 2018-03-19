import scrapy


class Loksabha(scrapy.Spider):
    name = "politicalParty"

    def start_requests(self):
        for j in range(1, 7000):
            # print(
            #     'http://myneta.info/{}/index.php?action=show_candidates&constituency_id={}'.format(j))
            yield scrapy.Request(url='http://myneta.info/party/index.php?action=summary&id={}'.format(j), callback=self.parse)

    def parse(self, response):
        party_name = str(response.css(
            '#main div div.grid_9 div.grid_9.alpha.omega div.grid_3.alpha h3::text').extract()).strip(
                '[]').strip("' '").split('(')[0].strip("' '")
        party_id = int(response.request.url.split('=')[-1])

        party_acronym = str(response.css(
            '#main div div.items b::text').extract()).strip('[]').strip("' '")

        print(party_id, party_name)

        # f_out = []
        # assets_out = []
        # donation_out = []

        for data in response.css('#table1 tr '):
            print('-------------------')
            financial_year = ''
            # for td in data.css('tr'):
            financial_year = str(
                data.css('td:nth-child(1) a::text').extract()).strip('[]').strip("' '")
            financial_url = str(
                data.css('td:nth-child(1) a::attr(href)').extract()).strip('[]').strip("' '")

            donation = []
            donation = urlcrop(financial_url)
            total_donation = 0
            # total_assets = 0
            # total_liabilities = 0
            # total_income = 0
            # total_expenditure = 0
            no_of_donors = 0
            average_donation = 0
            # list1 = [financial_year, party_acronym]
            # if financial_year not in f_out:
            #     f_out.append(list1)

            if donation == 'assets' and financial_year:
                total_donation = str(data.css(
                    'td:nth-child(2)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:]
                no_of_donors = str(data.css(
                    'td:nth-child(3)::text').extract()).strip('[]').strip("' '")
                average_donation = str(data.css(
                    'td:nth-child(4)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:]
                # d = [total_donation, no_of_donors, average_donation]
                # donation_out.append(d)

            # else:
            #     total_assets = str(data.css(
            #         'td:nth-child(2)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:-5]
            #     total_liabilities = str(data.css(
            #         'td:nth-child(3)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:-5]
            #     total_income = str(data.css(
            #         'td:nth-child(4)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:-5]
            #     total_expenditure = str(data.css(
            #         'td:nth-child(5)::text').extract()).strip('[]').strip("' '").replace(',', '')[4:-5]
            #     # a = [total_assets, total_liabilities,
            #     #      total_income, total_expenditure]
            #     # assets_out.append(a)

                if party_name:
                    yield {
                        'party_id': party_id,
                        'party_name': party_name,
                        'party_acronym': party_acronym,
                        'financial_year': financial_year,
                        'financial_url': financial_url,
                        # 'total_assets': total_assets,
                        # 'total_liabilities': total_liabilities,
                        # 'total_income': total_income,
                        # 'total_expenditure': total_expenditure,
                        'total_donation': total_donation,
                        'no_of_donors': no_of_donors,
                        'average_donation': average_donation,
                    }


def urlcrop(f_url):
    a = f_url.split('&')[0]
    if a == '/party/index.php?action=donation':
        return 'donation'
    if a == '/party/index.php?action=itr':
        return 'assets'
    return a
