import scrapy
import re
import json


class ElectionWise(scrapy.Spider):
    name = "politicalPartyMerge"

    def start_requests(self):
        yield scrapy.Request(url='http://myneta.info/ls2009/index.php?action=show_candidates&constituency_id=1',
                             callback=self.parse)

    def parse(self, response):
        json_assets = './assets.json'
        json_donations = './donation.json'
        json_output = './political_parties.json'

        with open(json_assets) as json_assets:
            assets = json.load(json_assets)
            for index, asset in enumerate(assets):
                financial_url = []
                party_id = asset['party_id']
                party_name = asset['party_name']
                party_acronym = asset['party_acronym']
                financial_year = asset['financial_year']
                asset_url = asset['financial_url']
                total_assets = asset['total_assets']
                total_liabilities = asset['total_liabilities']
                total_income = asset['total_income']
                total_expenditure = asset['total_expenditure']
                # 'total_donation': total_donation,
                # 'no_of_donors': no_of_donors,
                # 'average_donation': average_donation,
                # if index > 5:
                #     break
                file = open(json_donations, 'rb')
                donations = json.load(file)
                total_donation = 0
                no_of_donors = 0
                average_donation = 0
                donation_url = ''
                for donation in donations:
                    # print('inner for')
                    if party_id == donation['party_id']:
                        print('1st if')
                        if financial_year == donation['financial_year']:
                            print('>>>>>>>>>>>>>>>>>>>>>> {} : {} : {} : {} : {}'.format(
                                donation['party_acronym'], party_name, donation['financial_year'], donation['total_donation'], total_assets))
                            total_donation = donation['total_donation']
                            no_of_donors = donation['no_of_donors']
                            average_donation = donation['average_donation']
                            donation_url = donation['financial_url']

                with open(json_output, 'a') as output:
                    dic = ({"party_id": party_id, "party_name": party_name,
                            "party_acronym": party_acronym,
                            "financial_year": financial_year,
                            #"financial_url": "/party/index.php?action=itr&year=2016&id=1",
                            "total_assets": total_assets,
                            "total_liabilities": total_liabilities,
                            "total_income": total_income,
                            "total_expenditure": total_expenditure,
                            "asset_url": asset_url,
                            "total_donation": total_donation,
                            "no_of_donors": no_of_donors,
                            "average_donation": average_donation,
                            "donation_url": donation_url,
                            })
                    f_dic = dict(dic)
                    # values = [{'party_id': v, 'party_acronym': v}
                    #           for k, v in f_dic.items()]
                    # temp = []
                    list_key_value = [[k, v] for k, v in f_dic.items()]
                    # for key, value in f_dic.iteritems():
                    #     temp = [key, value]
                    #     dictlist.append(temp)
                    json.dump(f_dic, output)
