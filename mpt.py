import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.optimize as sco
import scipy.interpolate as sci
import scipy.stats as scs
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.graphics.api as smg
import statsmodels.stats.api as sms
import statsmodels.tsa.stattools as smtsa
import statsmodels.tsa.seasonal as smtsa
import statsmodels.tsa.vector_ar as smtsa
import statsmodels.tsa.vector_ar.var_model as smtsa


# modern portfolio theory to identify which nba players are the best value for fantasy basketball
# import libraries


# import data from sqlite database
conn = sqlite3.connect('nba_teams.db')
c = conn.cursor()

# create a dataframe for each team
c.execute('''SELECT * FROM "Atlanta Hawks"''')
atl_df = pd.DataFrame(c.fetchall())
atl_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Boston Celtics"''')
bos_df = pd.DataFrame(c.fetchall())
bos_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Brooklyn Nets"''')
bkn_df = pd.DataFrame(c.fetchall())
bkn_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Charlotte Hornets"''')
cha_df = pd.DataFrame(c.fetchall())
cha_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Chicago Bulls"''')
chi_df = pd.DataFrame(c.fetchall())
chi_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Cleveland Cavaliers"''')
cle_df = pd.DataFrame(c.fetchall())
cle_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Dallas Mavericks"''')
dal_df = pd.DataFrame(c.fetchall())
dal_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Denver Nuggets"''')
den_df = pd.DataFrame(c.fetchall())
den_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Detroit Pistons"''')
det_df = pd.DataFrame(c.fetchall())
det_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Golden State Warriors"''')
gsw_df = pd.DataFrame(c.fetchall())
gsw_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Houston Rockets"''')
hou_df = pd.DataFrame(c.fetchall())
hou_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Indiana Pacers"''')
ind_df = pd.DataFrame(c.fetchall())
ind_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Los Angeles Clippers"''')
lac_df = pd.DataFrame(c.fetchall())
lac_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Los Angeles Lakers"''')
lal_df = pd.DataFrame(c.fetchall())
lal_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Memphis Grizzlies"''')
mem_df = pd.DataFrame(c.fetchall())
mem_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Miami Heat"''')
mia_df = pd.DataFrame(c.fetchall())
mia_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Milwaukee Bucks"''')
mil_df = pd.DataFrame(c.fetchall())
mil_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Minnesota Timberwolves"''')
min_df = pd.DataFrame(c.fetchall())
min_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "New Orleans Pelicans"''')
nop_df = pd.DataFrame(c.fetchall())
nop_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "New York Knicks"''')
nyk_df = pd.DataFrame(c.fetchall())
nyk_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Oklahoma City Thunder"''')
okc_df = pd.DataFrame(c.fetchall())
okc_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Orlando Magic"''')
orl_df = pd.DataFrame(c.fetchall())
orl_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Philadelphia 76ers"''')
phi_df = pd.DataFrame(c.fetchall())
phi_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Phoenix Suns"''')
phx_df = pd.DataFrame(c.fetchall())
phx_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Portland Trail Blazers"''')
por_df = pd.DataFrame(c.fetchall())
por_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Sacramento Kings"''')
sac_df = pd.DataFrame(c.fetchall())
sac_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "San Antonio Spurs"''')
sas_df = pd.DataFrame(c.fetchall())
sas_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Toronto Raptors"''')
tor_df = pd.DataFrame(c.fetchall())
tor_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Utah Jazz"''')
uta_df = pd.DataFrame(c.fetchall())
uta_df.columns = [x[0] for x in c.description]

c.execute('''SELECT * FROM "Washington Wizards"''')
was_df = pd.DataFrame(c.fetchall())
was_df.columns = [x[0] for x in c.description]



