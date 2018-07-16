import scrapy
import re
import json


class ElectionWise(scrapy.Spider):
    name = "politicalPartyMerge_f"

    def start_requests(self):
        json_output = './political_parties.json'

        with open(json_output) as json_assets:
            assets = json.load(json_assets)
            for index, asset in enumerate(assets):
                yield scrapy.Request(url='http://myneta.info/party/index.php?action=summary&id={}'.format(asset['party_id']),
                                     callback=self.parse)

    def parse(self, response):
        json_ = './political_parties.json'
        json_output = './political_parties_f2.json'

        party_type = str(response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div[1]/text()').extract()[2]).strip("' '")
        party_state = str(response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div[1]/text()').extract()[4]).strip("' '")
        print(party_state)
        if party_type:
            party_typeX = party_type
        else:
            party_typeX = ''
        uid = int(response.request.url.split("=")[-1])
        print('------------------------{} : {}'.format(party_type, uid))

        with open(json_) as json_:
            assets = json.load(json_)
            for index, asset in enumerate(assets):
                #print("in ================ for")
                # print("{} ========= {}".format(
                #     type(asset['party_id']), type(uid)))
                if asset['party_id'] == uid:
                    #print('in ===================if')
                    party_id = asset['party_id']
                    party_name = asset['party_name']
                    party_acronym = asset['party_acronym']
                    financial_year = asset['financial_year']
                    asset_url = asset['asset_url']
                    total_assets = asset['total_assets']
                    total_liabilities = asset['total_liabilities']
                    total_income = asset['total_income']
                    total_expenditure = asset['total_expenditure']
                    total_donation = asset['total_donation']
                    no_of_donors = asset['no_of_donors']
                    average_donation = asset['average_donation']
                    donation_url = asset['donation_url']
                    with open(json_output, 'a') as output:
                        dic = ({"party_id": party_id, "party_name": party_name,
                                "party_acronym": party_acronym,
                                "party_type": party_typeX,
                                "party_state": party_state,
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
                        json.dump(f_dic, output)
