import pandas as pd
import requests

pd.set_option('display.max_columns', None)  # so we can see all columns in a wide DataFrame
import time
import numpy as np

raw_api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2022-23&SeasonType=Pre%20Season&StatCategory=MIN'

headers = {
     'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
r = requests.get(url=raw_api_url, headers=headers).json()
df_cols_short = r['resultSet']['headers']

df_cols = ['Year', 'Season_type'] + df_cols_short

years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
season_types = ['Pre%20Season', 'Playoffs']

df = pd.DataFrame(columns=df_cols)

begin_loop = time.time()

for y in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=' + y + '&SeasonType=' + s + '&StatCategory=PTS'
        r = requests.get(url=api_url, headers=headers).json()
        temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=df_cols_short)
        temp_df2 = pd.DataFrame({'Year': [y for i in range(len(temp_df1))],
                                 'Season_type': [s for i in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
        df = pd.concat([df, temp_df3], axis=0)
        print(f'Finished scraping data from the {y} {s}')
        lag = np.random.uniform(low=1, high=5)
        print(f'...waiting {round(lag, 1)} seconds...')
        time.sleep(lag)
print(f'Process completed!! Total run time: {round(time.time() - begin_loop, 1)} seconds')
df.to_csv('nba_league_leaders.csv', index=False)

