import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)

data = pd.read_excel('nba_player_data.xlsx')

# //////////////////////////////// DATA CLEANING & ANALYSIS PREPARATION ///////////////////////////////

data.drop(columns=['RANK', 'EFF'], inplace=True)
data['season_start_year'] = data['Year'].str[:4].astype(int)
data['TEAM'].replace(to_replace=['NOP', 'NOH'], value='NO', inplace=True)
data['Season_type'].replace('Regular%20Season', 'RS', inplace=True)
rs_df = data[data['Season_type'] == 'RS']
playoffs_df = data[data['Season_type'] == 'Playoffs']

# ============================== First image =====================================
total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
              'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

# /////////////////////////// WHICH PLAYER STATS ARE CORRELATED WITH EACH OTHER /////////////////////////////

data_per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum().reset_index()
for col in data_per_min.columns[4:]:
    data_per_min[col] = data_per_min[col] / data_per_min['MIN']

data_per_min['FG%'] = data_per_min['FGM'] / data_per_min['FGA']
data_per_min['3PT%'] = data_per_min['FG3M'] / data_per_min['FG3A']
data_per_min['FT%'] = data_per_min['FTM'] / data_per_min['FTA']
data_per_min['FG3A%'] = data_per_min['FG3A'] / data_per_min['FGA']
data_per_min['PTS/FGA'] = data_per_min['PTS'] / data_per_min['FGA']
data_per_min['FG3M/FGM'] = data_per_min['FG3M'] / data_per_min['FGM']
data_per_min['FTA/FGA'] = data_per_min['FTA'] / data_per_min['FGA']
data_per_min['TRU%'] = 0.5 * data_per_min['PTS'] / (data_per_min['FGA'] + 0.475 * data_per_min['FTA'])
data_per_min['AST_TOV'] = data_per_min['AST'] / data_per_min['TOV']

data_per_min = data_per_min[data_per_min['MIN'] >= 50]
data_per_min.drop(columns=['PLAYER', 'PLAYER_ID', 'Year'], inplace=True)
# ================================end of first image ================================

# ================================== 4th image =======================================
# /////////////////////////// HOW HAS THE GAME CHANGED OVER THE PAST 10 YEARS /////////////////////////////
change_df = data.groupby('season_start_year')[total_cols].sum().reset_index()
change_df['POSS_est'] = change_df['FGA'] - change_df['OREB'] + change_df['TOV'] + 0.44 * change_df['FTA']
change_df[list(change_df.columns[0:2]) + ['POSS_est'] + list(change_df.columns[2:-1])]

change_df['FG%'] = change_df['FGM'] / change_df['FGA']
change_df['3PT%'] = change_df['FG3M'] / change_df['FG3A']
change_df['FT%'] = change_df['FTM'] / change_df['FTA']
change_df['AST%'] = change_df['AST'] / change_df['FGM']
change_df['FG3A%'] = change_df['FG3A'] / change_df['FGA']
change_df['PTS/FGA'] = change_df['PTS'] / change_df['FGA']
change_df['FG3M/FGM'] = change_df['FG3M'] / change_df['FGM']
change_df['FTA/FGA'] = change_df['FTA'] / change_df['FGA']
change_df['TRU%'] = 0.5 * change_df['PTS'] / (change_df['FGA'] + 0.475 * change_df['FTA'])
change_df['AST_TOV'] = change_df['AST'] / change_df['TOV']
change_per48_df = change_df.copy()
for col in change_per48_df.columns[2:18]:
    change_per48_df[col] = (change_per48_df[col] / change_per48_df['MIN']) * 48 * 5

change_per48_df.drop(columns='MIN', inplace=True)


# ====================================== end of 4th image ==================================

# ================================ 3rd image =============================
# //////////////////////////////////// HOW ARE MINUTES PLAYED DISTRIBUTED ///////////////////////////////
def hist_data(df=rs_df, min_MIN=0, min_GP=0):
    return df.loc[(df['MIN'] >= min_MIN) & (df['GP'] >= min_GP), 'PTS'] / \
           df.loc[(df['MIN'] >= min_MIN) & (df['GP'] >= min_GP), 'GP']


# =============================== end of 3rd image ===========================

# Create two plotly figures
# create the first graph ==============================
fig1 = px.imshow(data_per_min.corr())
# =====================================

# Create the second graph =============================
fig2 = px.histogram(playoffs_df, x='MIN', histnorm='percent')
# ======================================

# Create the third graph ===============================
fig3 = go.Figure()
# fig3.add_trace(go.Scatter(x=data_per_min['PTS/FGA'], y=data_per_min['TRU%'], mode='markers'))
fig3.add_trace(go.Histogram(x=hist_data(rs_df, 50, 5), histnorm='percent', name='RS',
                            xbins={'start': 0, 'end': 38, 'size': 1}))
fig3.add_trace(go.Histogram(x=hist_data(playoffs_df, 5, 1), histnorm='percent', name='playoffs',
                            xbins={'start': 0, 'end': 46, 'size': 1}))
fig3.update_layout(barmode='overlay')
fig3.update_traces(opacity=0.5)
# =======================================

# Create the 4th image =================
fig4 = go.Figure()
for col in change_per48_df.columns[1:]:
    fig4.add_trace(go.Scatter(x=change_per48_df['season_start_year'],
                              y=change_per48_df[col], name=col))
# ======================================================

# Create a subplot with three columns
fig = make_subplots(rows=2, cols=3)

# Add the three figures to the subplot
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.add_trace(fig3.data[0], row=1, col=3)
fig.add_trace(fig4.data[0], row=2, col=1)
# fig.add_traces(fig3.data, rows=[1] * len(fig3.data), cols=[3] * len(fig3.data))

# Update subplot layout
fig.update_layout(title='NBA Players Data')

# Show the subplot in the browser
fig.show()
