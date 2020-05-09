from bs4 import BeautifulSoup
import pickle
from pprint import pprint
from param import P

# netkeiba.com の出走表を手動でダウンロードする
load_html = P['race_file']
writing_pickle = 'shusso_horse.pickle'

with open(load_html, 'rb') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
shusso_table = soup.find_all('td', class_='HorseInfo')
horses = []
for i, s in enumerate(shusso_table):
    horse_name = s.a.get('title')
    horse_url = s.a.get('href')
    horses.append([horse_name, i+1, horse_url])

with open(writing_pickle, 'wb') as f:
    pickle.dump(horses, f)

print(f'{load_html} is arranged to {writing_pickle}')
print('contents of pickle is as follows:')

with open(writing_pickle, 'rb') as f:
    pprint(pickle.load(f))



