import pandas as pd
from random import randint
from joblib import load
from math import sqrt
from sklearn.metrics import mean_squared_error

#load data
df1 = pd.read_csv('/Users/abbott_vh/Sports_Betting/Season Data (All Time)/nba_data_22-23.csv')
df2 = pd.read_csv('/Users/abbott_vh/Sports_Betting/Season Data (All Time)/nba_data_21-22.csv')
df3 = pd.read_csv('/Users/abbott_vh/Sports_Betting/Season Data (All Time)/nba_data_20-21.csv')

# Combine the DataFrames into a single DataFrame
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

#drop all empty rows
season_data = combined_df.dropna()

#get header list for future use
header_list = season_data.columns
H_list = ["H_" + item for item in header_list]
A_list = ["A_" + item for item in header_list]
full_headers = H_list + A_list

#getting a random list of 20 unique teams to matchup and test
count = 20
names = []
teams = []
while count > 0:
    rand_number = randint(0,season_data.shape[0]-1)
    if season_data.iloc[rand_number]['Team'] not in names:
        listed_team = season_data.iloc[rand_number].tolist()
        teams.append(listed_team)
        names.append(season_data.iloc[rand_number]['Team'])
        count = count - 1

#creating a data frame of random matchups
team_pairs = [teams[i] + teams[i + 1] for i in range(0, len(teams), 2)]
random_matchups = pd.DataFrame(team_pairs, columns=full_headers)

#getting actual point totals for each game
h_score = random_matchups['H_PTS'].tolist()
a_score = random_matchups['A_PTS'].tolist()
total_score = []
for i in range(len(h_score)):
    total_score.append(h_score[i]+a_score[i])

#creating a data frame of point totals (kind of unneeded but doing it anyway)
data = {'Home Points': h_score, 'Away Points': a_score, 'Total Points': total_score}
points = pd.DataFrame(data)

#dropping columns for input into model
columns_to_drop = ['H_Unnamed: 0', 'H_Team', 'H_GP', 'H_W', 'H_L', 'H_WIN%', 
                   'H_Min', 'H_PTS', 'H_BLKA', 'H_PFD', 'A_Unnamed: 0', 
                   'A_Team', 'A_GP', 'A_W', 'A_L', 'A_WIN%', 'A_Min', 
                   'A_PTS', 'A_BLKA', 'A_PFD']

test = random_matchups.drop(columns=columns_to_drop, axis=1)

#load model
model = load('model.joblib')

#predict values and put them in a data frame
GB_predict_Tonight = model.predict(test)
Test_Totals= pd.DataFrame(GB_predict_Tonight,columns=['scores'])

#get RMSE and also just easy to read data frame to analyze results and print them
RMSE= sqrt(mean_squared_error(Test_Totals,points['Total Points']))
final_data = {'Guessed Total': Test_Totals['scores'].tolist(), 'Actual Total': points['Total Points'].tolist()}
eval = pd.DataFrame(final_data)

print(eval)
print("RMSE (Test Data) for GB:{0:10f}".format(RMSE))

