import glob
import pandas as pd
import numpy as np
from pprint import pprint
from bs4 import BeautifulSoup
import sys
from param import P

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
        df_used = df_used.rename(columns={'着順': 'OA'}) # order of arrival
        df_used.loc[:, 'race_type'] = 'G4' # 初期化
        df_used.loc[df_used['レース名'].str.contains('G3'), 'race_type'] = 'G3'
        df_used.loc[df_used['レース名'].str.contains('G2'), 'race_type'] = 'G2'
        df_used.loc[df_used['レース名'].str.contains('G1'), 'race_type'] = 'G1'
        df_used.loc[:, 'distance'] = 0 # 初期化
        # !+! 例外処理に近い
        df_used = df_used[df_used['距離'] != '']
        # !+!  
        df_used['distance'] = df_used['距離'].str.extract('([0-9]+)').astype(int)
        df_used = df_used.drop(['距離', 'レース名'], axis = 1) # 無駄列排除
        # 対象レース選択
        df_target = df_used[(P['race_range'][0] <= df_used.distance) & \
                            (df_used.distance < P['race_range'][1])].copy()
        df_target['CP'] = 0 
        df_target['GP'] = 1
        df_target.loc[df_target.race_type == 'G1', 'GP'] = P['GP_G1']
        df_target.loc[df_target.race_type == 'G2', 'GP'] = P['GP_G2']
        df_target.loc[df_target.race_type == 'G3', 'GP'] = P['GP_G3']
        df_target.loc[df_target.race_type == 'G4', 'GP'] = P['GP_G4']
        # CP振り
        df_target.loc[df_target.OA == '1', 'CP'] = P['CP_1'] 
        df_target.loc[df_target.OA == '2', 'CP'] = P['CP_2'] 
        df_target.loc[df_target.OA == '3', 'CP'] = P['CP_3'] 
        df_target.loc[df_target.OA == '4', 'CP'] = P['CP_4'] 
        df_target.loc[df_target.OA == '5', 'CP'] = P['CP_5'] 
        score = (df_target.GP*df_target.CP).sum()/len(df_target)
        if np.isnan(score):
            score = 0
        return score

    except AttributeError:
        return 0

data_path = sorted(glob.glob('./tmp_data/*'))
order = ['self.html', 'father.html', 'mother.html']
df = pd.DataFrame(columns=['num'] + order) # 空のデータフレーム
# 計算
for d in data_path:
    number = d.split('/')[-1]
    data = {'num':number, order[0]:0, order[1]:0, order[2]:0}
    for o in order:
        fp = d + '/' + o
        score = history_scraper(fp)
        data[o] = score
    df = df.append(data, ignore_index=True)

# 正規化
df['self_nrmd'] = df['self.html'] / df['self.html'].max()
df['father_nrmd'] = df['father.html'] / df['father.html'].max()
df['mother_nrmd'] = df['mother.html'] / df['mother.html'].max()
df['final_score'] = df.self_nrmd*P['w_s'] + df.father_nrmd*P['w_f'] + df.mother_nrmd*P['w_m']
# 結果
print('------------------')
print(f'レース距離:{P["race_dist"]}')
print(f'searched range:{P["race_range"]}')
print(f'weights-> w_s:{P["w_s"]}, w_f:{P["w_f"]}, w_m:{P["w_m"]}')
print(df.sort_values('final_score').to_string(index=False)) # index を表示しない
