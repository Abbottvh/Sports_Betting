from sklearn.model_selection import train_test_split
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from joblib import dump
#import data and clean it up

df_without_missing_values = pd.read_csv('edited_data.csv')

#these are actually wrong/not compatible with our data, need to change them a little
features = ['H_FGM', 'H_FGA', 
            'H_FG%', 'H_3PM', 'H_3PA', 'H_3P%', 'H_FTM', 'H_FTA', 
            'H_FT%', 'H_OREB', 'H_DREB', 'H_REB', 'H_AST', 'H_TOV', 'H_STL', 
            'H_BLK', 'H_PF', 'H_+/-', 'A_FGM', 'A_FGA', 
            'A_FG%', 'A_3PM', 'A_3PA', 'A_3P%', 'A_FTM', 'A_FTA', 
            'A_FT%', 'A_OREB', 'A_DREB', 'A_REB', 'A_AST', 'A_TOV', 'A_STL', 
            'A_BLK', 'A_PF', 'A_+/-']

# features = ['H_2PM', 'H_2PA', 
#             'H_2P%', 'H_3PM', 'H_3PA', 'H_3P%', 'H_FTM', 'H_FTA', 
#             'H_FT%', 'H_OREB', 'H_DREB', 'H_REB', 'H_AST', 'H_TOV', 'H_STL', 
#             'H_BLK', 'H_PF', 'H_+/-', 'A_2PM', 'A_2PA', 
#             'A_2P%', 'A_3PM', 'A_3PA', 'A_3P%', 'A_FTM', 'A_FTA', 
#             'A_FT%', 'A_OREB', 'A_DREB', 'A_REB', 'A_AST', 'A_TOV', 'A_STL', 
#             'A_BLK', 'A_PF', 'A_+/-']

    #old feature list   
# ['H_WIN%', 'H_PTS_PG', 'H_FGM_PG', 'H_FGA_PG', 'H_CUM_FG%', 'H_3PM_PG', 
#             'H_3PA_PG', 'H_CUM_3P%', 'H_FTM_PG', 'H_FTA_PG', 'H_CUM_FT%', 'H_OREB_PG', 
#             'H_DREB_PG', 'H_REB_PG', 'H_AST_PG', 'H_TOV_PG', 'H_STL_PG', 'H_BLK_PG', 
#             'H_BLKA_PG', 'H_PF_PG', 'H_PFD_PG', 'H_+/-_PG', 'A_WIN%', 'A_PTS_PG', 
#             'A_FGM_PG', 'A_FGA_PG', 'A_CUM_FG%', 'A_3PM_PG', 'A_3PA_PG', 'A_CUM_3P%', 
#             'A_FTM_PG', 'A_FTA_PG', 'A_CUM_FT%', 'A_OREB_PG', 'A_DREB_PG', 'A_REB_PG', 
#             'A_AST_PG', 'A_TOV_PG', 'A_STL_PG', 'A_BLK_PG', 'H_BLKA_PG2', 'A_PF_PG', 
#             'A_PFD_PG', 'A_+/-_PG']

#formatting the dataframe correctly 
columns_to_drop = ['GAME DATE', 'H_TEAM', 'H_MIN', 'H_PTS', 
                   'A_TEAM', 'A_FINAL', 'A_MIN', 'A_PTS', 'POINT_TOTAL']

new_df = df_without_missing_values.drop(columns=columns_to_drop, axis=1)

#setting target value
target = new_df['H_FINAL']

#setting variables for training
X = new_df[features]
y=target

#splitting data into batches
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#training the model
GB = RandomForestClassifier()
GB.fit(X_train, y_train)
GB_predict_Train=GB.predict(X_train)

#outputting how poorly/well the model did 
#if big difference between the two values than you overfit
#if they are really close together than you underfit

# RMSE1=sqrt(mean_squared_error(y_train,GB_predict_Train))
#print("RMSE (training) for GB:{0:10f}".format(RMSE1))
GB_predict_Test=GB.predict(X_test)
# RMSE= sqrt(mean_squared_error(y_test,GB_predict_Test))
#print("RMSE (Test Data) for GB:{0:10f}".format(RMSE))
# Calculate the accuracy of the model
# print("real results")
# print(y_test)
# print("model results")
# print(GB_predict_Test)
train_accuracy = accuracy_score(y_train, GB_predict_Train)
test_accuracy = accuracy_score(y_test, GB_predict_Test)

print(f"Training Accuracy: {train_accuracy}")
print(f"Testing Accuracy: {test_accuracy}")

# save model at the end if you like it
# dump(GB, 'moneyline.joblib')