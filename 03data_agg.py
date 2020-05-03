import glob
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
thr = 3000

def history_scraper(fp):
    try: 
        with open(fp, 'rb') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='db_h_race_results nk_tb_common')
        rows = table.find_all('tr')
        each_row = []
        for row in rows:
            row_content = []
            for cell in row.find_all(['td', 'th']):
                row_content.append(cell.get_text().strip())
            each_row.append(row_content)
        col_name = each_row[0]
        df = pd.DataFrame(each_row[1:], columns=col_name)
        # 今回は使うところのみ抜粋
        df_used = df[['レース名', '距離', '着順']].copy()
        df_used.loc[df_used['着順'] == '失', '着順'] = '100'
        df_used.loc[df_used['着順'] == '中', '着順'] = '100'
        df_used.loc[df_used['着順'] == '除', '着順'] = '100'
        df_used.loc[:, 'race_name_cvt'] = 1 # 初期化
        df_used.loc[df_used['レース名'].str.contains('G3'), 'race_name_cvt'] = 2
        df_used.loc[df_used['レース名'].str.contains('G2'), 'race_name_cvt'] = 4
        df_used.loc[df_used['レース名'].str.contains('G1'), 'race_name_cvt'] = 8
        df_used.loc[:, 'distance'] = 0 # 初期化
        df_used['distance'] = df_used['距離'].str.extract('([0-9]{4})').astype(int)
        df_used['top_point'] = df_used['着順'].astype(int)
        df_used.loc[df_used['着順'].astype(int) >= 5, 'top_point'] = 1000
        hyoka_data = df_used[df_used.distance >= thr]
        score = (1 / hyoka_data.top_point) * hyoka_data.race_name_cvt
        if len(score) == 0:
            return 0
        else:
            return score.sum()

    except AttributeError:
        return 0
    


data_path = sorted(glob.glob('./tmp_data/*'))
order = ['self.html', 'father.html', 'mother.html']
sorting = []
for d in data_path:
    print('------')
    number = d.split('/')[-1]
    ts = [] # total_score
    for o in order:
        fp = d + '/' + o
        score = history_scraper(fp)
        print(f'{o} {score}')
        ts.append(score)
    final = 0.5*ts[0] + 0.25*ts[1] + 0.25*ts[2]
    sorting.append([number, final])

pprint(sorting)
