import requests
from bs4 import BeautifulSoup
import json

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
            self.opt[line][name] = rate
    

def get_html():
    url = "https://maplestory.nexon.com/Guide/OtherProbability/cube/addi"
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

    datas = []

    for opt, dat in zip(cube_option, cube_data):
        table = Table()
        each_opt = opt.select('span')
        table.set_title(each_opt[0].string, each_opt[1].string)

        each_dat = dat.select('tr')
        for edat in each_dat:
            edatstr = edat.select('td')
            for i in range(0, 3):
                table.add_option(i, edatstr[i*2].string, edatstr[i*2+1].string)
        datas.append(table)

    return datas
        
def save_json(datas):
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

    with open("addi_cube.json", "w", encoding="UTF-8") as json_file:
        json.dump(lyst, json_file, ensure_ascii=False)

if __name__ == "__main__":
    soup = get_html()
    datas = parse_html(soup)
    save_json(datas)
