import scrapy
import re
import json


class ElectionWise(scrapy.Spider):
    name = "acpc"

    def start_requests(self):
        yield scrapy.Request(url='http://myneta.info/ls2009/index.php?action=show_candidates&constituency_id=1',
                             callback=self.parse)

    def parse(self, response):
        json_ = 'C:/Users/LENOVO PC/Downloads/convertcsv.json'
        json_output = './ac_pc.json'
        with open(json_) as json_:
            data = json.load(json_)
            for index, state in enumerate(data):
                assemblies = state[
                    'Extent in terms of Assembly Constituencies'].split(',')
                p_constituency = state['Constituency'].strip()
                State = state['State'].strip()
                p_constituencies = state['Constituency']
                for assembly in assemblies:
                    assembly_constituencies = assembly.strip()
                    with open(json_output, 'a') as output:
                        dic = ({
                            "state": State,
                            "p_constituencies": p_constituencies,
                            "assembly_constituencies": assembly_constituencies,
                        })
                        f_dic = dict(dic)
                        json.dump(f_dic, output)
