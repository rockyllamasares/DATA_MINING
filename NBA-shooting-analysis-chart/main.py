import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)

data = pd.read_excel('nba_player_data.xlsx')
data.drop(columns=['RANK','EFF'], inplace=True)
data['season_start_year'] = data['Year'].str[:4].astype(int)
data['TEAM'].replace(to_replace=['NOP','NOH'], value='NO', inplace=True)
data['Season_type'].replace('Regular%20Season','RS', inplace=True)
rs_df = data[data['Season_type']=='RS']
playoffs_df = data[data['Season_type']=='Playoffs']

total_cols = ['MIN','FGM','FGA','FG3M','FG3A','FTM','FTA',
              'OREB','DREB','REB','AST','STL','BLK','TOV','PF','PTS']

data_per_min = data.groupby(['PLAYER','PLAYER_ID','Year'])[total_cols].sum().reset_index()
for col in data_per_min.columns[4:]:
    data_per_min[col] = data_per_min[col]/data_per_min['MIN']

data_per_min['FG%'] = data_per_min['FGM']/data_per_min['FGA']
data_per_min['3PT%'] = data_per_min['FG3M']/data_per_min['FG3A']
data_per_min['FT%'] = data_per_min['FTM']/data_per_min['FTA']
data_per_min['FG3A%'] = data_per_min['FG3A']/data_per_min['FGA']
data_per_min['PTS/FGA'] = data_per_min['PTS']/data_per_min['FGA']
data_per_min['FG3M/FGM'] = data_per_min['FG3M']/data_per_min['FGM']
data_per_min['FTA/FGA'] = data_per_min['FTA']/data_per_min['FGA']
data_per_min['TRU%'] = 0.5*data_per_min['PTS']/(data_per_min['FGA']+0.475*data_per_min['FTA'])
data_per_min['AST_TOV'] = data_per_min['AST']/data_per_min['TOV']

data_per_min = data_per_min[data_per_min['MIN']>=50]
data_per_min.drop(columns=['PLAYER','PLAYER_ID','Year'], inplace=True)

# Create two plotly figures
fig1 = px.imshow(data_per_min.corr())
fig2 = px.histogram(playoffs_df, x='MIN', histnorm='percent')

# Create a subplot with two columns
fig = make_subplots(rows=1, cols=2)

# Add the two figures to the subplot
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)

# Update subplot layout
fig.update_layout(title='NBA Player Data')

# Show the subplot in the browser
fig.show()
