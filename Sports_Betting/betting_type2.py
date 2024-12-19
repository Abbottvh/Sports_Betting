import pandas as pd
from joblib import load

#scrapped data of most up-to-date stats for the two teams
file_name="today_game_data.csv"
bet = pd.read_csv(file_name)

columns_to_drop = ['H_', 'H_Team', 'H_GP', 'H_W', 'H_L', 'H_WIN%', 
                   'H_Min', 'H_PTS', 'H_BLKA', 'H_PFD', 'A_', 
                   'A_Team', 'A_GP', 'A_W', 'A_L', 'A_WIN%', 'A_Min', 
                   'A_PTS', 'A_BLKA', 'A_PFD']

new_bet = bet.drop(columns=columns_to_drop, axis=1)


#do some shenanigans to make the "Bet" in 
# same format as training data (i.e. drop empties, make coloumns match)

#import model
model = load('moneyline.joblib')

#predict values 

GB_predict_Tonight = model.predict(new_bet)
Tonights_Totals= pd.DataFrame(GB_predict_Tonight,columns=['scores'])
print(Tonights_Totals.to_string(index=False))

# make money $$$