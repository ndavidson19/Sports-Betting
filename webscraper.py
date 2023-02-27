import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = 'https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-points'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')

player_prop_elements =  soup.find_all('div', {'class': 'sportsbook-table__body'})




player_names = []
player_odds = []
player_odds_over = []
player_odds_under = []

for tr in soup.find_all('span', {'class': 'sportsbook-row-name'}):
    player_names.append(tr.text)



for tr in soup.find_all('div', {'class': 'sportsbook-outcome-cell__body'}):
    player_odds.append(re.sub(r'\xa0', ' ', tr.text))

for odds in player_odds:
    if 'O' in odds:
        player_odds_over.append(odds)
    else:
        player_odds_under.append(odds)



print(player_names, player_odds_over, [player_odds_under])
print(len(player_names), len(player_odds_over), len(player_odds_under))

props_df = pd.DataFrame({'player_name': player_names, 'Over': player_odds_over, 'Under': player_odds_under})

# save props_df to sqlite database

conn = sqlite3.connect('player_props.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS player_props
                (player_name text, player_points_over text, player_points_under text)''')

props_df.to_sql('player_props', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

