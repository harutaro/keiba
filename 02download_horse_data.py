import pickle
import requests
import sys
import os
import shutil
import glob
# from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pprint import pprint

load_pickle = './shusso_horse.pickle'
save_path = './tmp_data/'
# headers = {'User-Agent': UserAgent().chrome}
prefix = 'https://db.netkeiba.com/horse/'

files = glob.glob(save_path + '*')
if len(files) > 0 :
    print(f'There are some files in {save_path}. Do you remove?(y, n)')
    cmd = input('>>>')
    if cmd == 'y':
        shutil.rmtree(save_path)
        os.mkdir(save_path)
    else:
        print('Files are not removed.')
        sys.exit()

print('Downloading...')
with open(load_pickle, 'rb') as f:
    horse_list = pickle.load(f)
pprint(horse_list)

for h in horse_list:
    num = str(h[1]).zfill(2)
    print('-'*20)
    print(num)
    os.mkdir(save_path + num)
    h_save_dir = save_path + num
    # その馬自身のデータ取得
    r = requests.get(h[2]) 
    r.encoding = r.apparent_encoding
    with open(h_save_dir + '/' + 'self.html', 'w', encoding=r.encoding) as f:
        f.write(r.text)
    html = r.text
    # その馬の父母を取得
    soup = BeautifulSoup(html, 'html.parser')
    basic_data = soup.find('table', class_='blood_table')
    parents = basic_data.find_all('td', rowspan='2')
    father = parents[0].find('a').string
    father_id = parents[0].find('a').get('href').split('/')[-2]
    father_link = prefix + father_id
    mother = parents[1].find('a').string
    mother_id = parents[1].find('a').get('href').split('/')[-2]
    mother_link = prefix + mother_id
    # father データ取得
    r_f = requests.get(father_link)
    r_f.encoding = r_f.apparent_encoding
    with open(h_save_dir + '/' + 'father.html', 'w', encoding=r.encoding) as f:
        f.write(r_f.text)
    # mother データ取得
    r_m = requests.get(mother_link)
    r_m.encoding = r_m.apparent_encoding
    with open(h_save_dir + '/' + 'mother.html', 'w', encoding=r.encoding) as f:
        f.write(r_m.text)


