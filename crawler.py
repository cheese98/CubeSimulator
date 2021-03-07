import requests
from bs4 import BeautifulSoup
import json

'''
Maplestory Cube Probality Crawler
thanks to: cjh980402 (found error on hats)
'''
class Table():
    def __init__(self):
        self.level = ""
        self.equip = ""
        self.opt = [{}, {}, {}]
    
    def set_title(self, level, equip):
        self.level = level
        self.equip = equip
    
    def add_option(self, line, name, rate):
        if name:
            name = name.replace('\r', '').replace('\n', '').replace('    ', '').strip()
            self.opt[line][name] = round(float(rate.replace('%', '')), 4)
    

def get_html(name):
    url = "https://maplestory.nexon.com/Guide/OtherProbability/cube/" + name
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        print(response.status_code)
        exit()

def parse_html(soup):
    cube_option = soup.select('div.contents_wrap > div.cube_option')
    cube_data = soup.select('div.contents_wrap > table.cube_data > tbody')

    for elem in cube_data:
        for br in elem.select('br'):
            br.extract()

    datas = []

    for opt, dat in zip(cube_option, cube_data):
        table = Table()
        each_opt = opt.select('span')
        table.set_title(each_opt[0].string, each_opt[1].string)

        each_dat = dat.select('tr')
        for edat in each_dat:
            edatstr = edat.select('td')
            for i in range(0, 3):
                table.add_option(i, edatstr[i*2].get_text(), edatstr[i*2+1].string)
        datas.append(table)

    return datas
        
def save_json(datas, name):
    lyst = []
    for item in datas:
        dict = {
            'level' : item.level,
            'equip' : item.equip,
            'first' : item.opt[0],
            'second' : item.opt[1],
            'third' : item.opt[2]
        }
        lyst.append(dict)

    with open(name + "_cube.json", "w", encoding="UTF-8") as json_file:
        json.dump(lyst, json_file, ensure_ascii=False)

def execute(name):
    soup = get_html(name)
    datas = parse_html(soup)
    save_json(datas, name)

if __name__ == "__main__":
    for name in ['red', 'black', 'addi']:
        execute(name)
        print(name + "_cube.json finished")
