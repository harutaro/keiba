from bs4 import BeautifulSoup
import pickle
from pprint import pprint
import re
pat = re.compile(r'[0-9]+')
P = {
    #'race_file': './nhk.html',
    'race_file': './kyoto11.html',
    'prefix_url': 'https://db.netkeiba.com/horse/', 
    'CP_1': 3,
    'CP_2': 2, 
    'CP_3': 1, 
    'CP_4': 0, 
    'CP_5': 0, 
    'CP_6': 0, 
    'GP_G1': 1.5, 
    'GP_G2': 1.3, 
    'GP_G3': 1.1, 
    'GP_G4': 1, 
    'w_s': 0.4, 
    'w_f': 0.35, 
    'w_m': 0.25
}

# 以下でレースの距離情報を取得
with open(P['race_file'], 'rb') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
distance_raw = soup.find('div', class_='RaceData01').span.string.strip()
P['race_dist'] = int(re.search(pat, distance_raw).group(0))
d = int(P['race_dist'])
if 0 <= d and d < 2800:
    P['race_range'] = [d-400, d+300]
elif 2800 <= d and d < 5000:
    P['race_range'] = [2800, 5000]
# P['race_range'] = [1400, 1801]
