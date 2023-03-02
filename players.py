from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.static import teams
import pandas as pd
import sqlite3



### Create a SQLLite database to store all nba player stats
# Only want data from 2023 season


# Create a list of all teams using the nba_api
nba_teams = teams.get_teams()

# Create a list of all players using the nba_api
nba_players = players.get_players()


# Use dictionary comprehension to create a dataframe for each team with their consituent players and their stats for the 2022-23 season

# Create a connection to the database
conn = sqlite3.connect('nba_teams.db')
c = conn.cursor()

# first create a dataframe for each players career stats by matching their player_ids



for player in nba_players:
    # We only want to get the stats for the 2022-23 season
    player_career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
    # only get if the player has played in the 2022-23 season
    if any(player_career_stats.get_data_frames()[0]['SEASON_ID'] != '2022-23'):
        # go on to next player 
        continue
    else:
        player_name = player['full_name']
        player_career_stats_df = player_career_stats.get_data_frames()[0]
        player_career_stats_df['id'] = player_name
        # Change dataframe column id column to be name
        player_career_stats_df.rename(columns={'id': 'Name'}, inplace=True)
        
        

# Save the changes to the database

conn.commit()
conn.close()

# display the dataframes

