import pandas as pd
import sqlite3
import re


# read the sqlite database and display in pandas dataframe print to user

def main():
    conn = sqlite3.connect('player_props.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM prizepicks''')
    prizepicks_df = pd.DataFrame(c.fetchall())
    prizepicks_df.columns = [x[0] for x in c.description]

    c.execute('''SELECT * FROM player_props''')
    player_props_df = pd.DataFrame(c.fetchall())
    player_props_df.columns = [x[0] for x in c.description]

    # make a new dataframe using a join on the player names that match

    c.execute('''SELECT * FROM prizepicks
                INNER JOIN player_props
                ON prizepicks.player_name = player_props.player_name
                ''')
    joined_df = pd.DataFrame(c.fetchall())
    joined_df.columns = [x[0] for x in c.description]   


    conn.commit()
    conn.close()
    

    # create a new column in the joined_df that is the difference between the points and the over/under

    joined_df['Line Diff'] = joined_df['points'].astype(float) - joined_df['Under'].str.extract(r'(\d+.\d+)', expand=False).astype(float)

    # create a new column for the implied probability of the over/under

    joined_df['Under Implied Prob'] = joined_df['Under'].str.extract(r'((?<=−).*)', expand=False).astype(float) / (joined_df['Under'].str.extract(r'((?<=−).*)', expand=False).astype(float) + 100)
    # any None columns are + odds
    # get logical index of which columns have None values
    null_index = joined_df['Under Implied Prob'].isnull()
    joined_df['Under Implied Prob'] = joined_df['Under Implied Prob'].fillna(100 / (joined_df['Under'][null_index].str.extract(r'((?<=\+).*)', expand=False).astype(float) + 100))

    joined_df['Over Implied Prob'] = joined_df['Over'].str.extract(r'((?<=−).*)', expand=False).astype(float) / (joined_df['Over'].str.extract(r'((?<=−).*)', expand=False).astype(float) + 100)
    null_index = joined_df['Over Implied Prob'].isnull()
    joined_df['Over Implied Prob'] = joined_df['Over Implied Prob'].fillna(100 / (joined_df['Over'][null_index].str.extract(r'((?<=\+).*)', expand=False).astype(float) + 100))

    joined_df['Book Edge'] = abs(joined_df['Over Implied Prob'] + joined_df['Under Implied Prob'] - 1)
    joined_df["Under True Prob Odds"] = joined_df['Under Implied Prob'] - joined_df['Book Edge']
    joined_df["Over True Prob Odds"] = joined_df['Over Implied Prob'] - joined_df['Book Edge']

    # create a new column for the true odds of the over/under

    # expected value is ammount won per bet * probability of winning - ammount lost per bet * probability of losing
    joined_df['Under Expected Value'] = (joined_df['Under'].str.extract(r'((?<=−).*)', expand=False).astype(float) * joined_df['Under True Prob Odds']) - (100 * (1 - joined_df['Under True Prob Odds']))
    null_index = joined_df['Under Expected Value'].isnull()
    joined_df['Under Expected Value'] = joined_df['Under Expected Value'].fillna((joined_df['Under'][null_index].str.extract(r'((?<=\+).*)', expand=False).astype(float) * joined_df['Under True Prob Odds'][null_index]) - (100 * (1 - joined_df['Under True Prob Odds'][null_index])))


    joined_df['Over Expected Value'] = (joined_df['Over'].str.extract(r'((?<=−).*)', expand=False).astype(float) * joined_df['Over True Prob Odds']) - (100 * (1 - joined_df['Over True Prob Odds']))
    null_index = joined_df['Over Expected Value'].isnull()
    joined_df['Over Expected Value'] = joined_df['Over Expected Value'].fillna((joined_df['Over'][null_index].str.extract(r'((?<=\+).*)', expand=False).astype(float) * joined_df['Over True Prob Odds'][null_index]) - (100 * (1 - joined_df['Over True Prob Odds'][null_index])))

    # sort by highest over and under expected values
    joined_df = joined_df.sort_values(by=['Over Expected Value', 'Under Expected Value'], ascending=False)
    pd.max_display_rows = 1000
    print(joined_df)
    







if __name__ == '__main__':
    main()
