import pandas as pd
import glob

#import data and put it into one data frame object
file_names = glob.glob('/Users/abbott_vh/Sports_Betting/Game Data (Last 3 Years)/*.csv')
data_frames = []
for file_name in file_names:
    data = pd.read_csv(file_name)
    data_frames.append(data)

df = pd.concat(data_frames, ignore_index=True)

#dropping rows with empty values (Model doesn't work with NA values)
df_without_missing_values = df.dropna()

#pairing away game data with home game data into the pairs list
#this is a better format for the model as far as I can tell
pairs = []
paired_up = []
count = 1
#finding the date of our first value and then extracting all other games that occured on that day
#to compare to see if we have the data of the team they played against
date = df_without_missing_values.iloc[0,2]
filtered_rows = df_without_missing_values[df_without_missing_values['GAME DATE'] == date]

#needed so that for loop remembers the date at edge cases (flipping to a new day)
old_length = filtered_rows.shape[0]

#this is definetly really redundant and inefficient, but it works so Im keeping it
for i in range(df_without_missing_values.shape[0]):
    #finding our date and its list
    date = df_without_missing_values.iloc[i,2]
    filtered_rows = df_without_missing_values[df_without_missing_values['GAME DATE'] == date]
    #asking to see if i loop is still on the same day
    if count > old_length:
        #if past old_length (number of games on the current day), 
        # reset the count to 1 (first game of next day) and resest paired_up to empty 
        # (list letting us know if a certain game has already been accounted for, 
        # since almost every game has two rows in the data table, one for the away team and one for the home team)
        paired_up = []
        count = 1
    #looping through all games for that day
    for j in range(filtered_rows.shape[0]):
        #asking if this is the partner row for our ith row currently being looped
        if df_without_missing_values.iloc[i,1][:3] == filtered_rows.iloc[j,1][-3:]:
            #making sure this game hasn't been accounted for yet
            if df_without_missing_values.iloc[i,0] not in paired_up:
                #pair the two games together and put them in pairs list
                pair = [df_without_missing_values.iloc[i], filtered_rows.iloc[j]]
                pairs.append(pair)

                #add the game to paired up to show that its been accounted for
                paired_up.append(filtered_rows.iloc[j,1][:3]) 

    #increase the count and change old_length
    count = count + 1
    old_length = filtered_rows.shape[0]

#set the headers for our new data frame
Headers = ['GAME DATE', 'H_TEAM', 'H_FINAL', 'H_MIN', 'H_PTS', 'H_FGM', 'H_FGA', 
            'H_FG%', 'H_3PM', 'H_3PA', 'H_3P%', 'H_FTM', 'H_FTA', 
            'H_FT%', 'H_OREB', 'H_DREB', 'H_REB', 'H_AST', 'H_TOV', 'H_STL', 
            'H_BLK', 'H_PF', 'H_+/-', 'A_TEAM', 'A_FINAL', 'A_MIN', 'A_PTS', 'A_FGM', 'A_FGA', 
            'A_FG%', 'A_3PM', 'A_3PA', 'A_3P%', 'A_FTM', 'A_FTA', 
            'A_FT%', 'A_OREB', 'A_DREB', 'A_REB', 'A_AST', 'A_TOV', 'A_STL', 
            'A_BLK', 'A_PF', 'A_+/-', 'POINT_TOTAL']

# Headers = ['GAME DATE', 'H_TEAM', 'H_FINAL', 'H_MIN', 'H_PTS', 'H_2PM', 'H_2PA', 
#             'H_2P%', 'H_3PM', 'H_3PA', 'H_3P%', 'H_FTM', 'H_FTA', 
#             'H_FT%', 'H_OREB', 'H_DREB', 'H_REB', 'H_AST', 'H_TOV', 'H_STL', 
#             'H_BLK', 'H_PF', 'H_+/-', 'A_TEAM', 'A_FINAL', 'A_MIN', 'A_PTS', 'A_2PM', 'A_2PA', 
#             'A_2P%', 'A_3PM', 'A_3PA', 'A_3P%', 'A_FTM', 'A_FTA', 
#             'A_FT%', 'A_OREB', 'A_DREB', 'A_REB', 'A_AST', 'A_TOV', 'A_STL', 
#             'A_BLK', 'A_PF', 'A_+/-', 'POINT_TOTAL']


#create a new data frame with our new headers
new_df = pd.DataFrame(columns=Headers)
for item in pairs:
    #convert the rows to list and make some important variables
    row1 = item[0].tolist()
    row2 = item[1].tolist()
    date = row1[2]
    point_total = row1[5] + row2[5]

    #figuring out which team is the away team
    if "@" in row1[1]:
        away = True
    else:
        away = False

    #delete some unneeded entries in the row
    del row1[1]
    del row1[1]
    del row2[1]
    del row2[1]

    #changing FG stats to 2P stats
    # row1[4] = row1[4] - row1[7]
    # row1[5] = row1[5] - row1[8]
    # row1[6] = round((row1[4]/row1[5])*100,1)
    # row2[4] = row2[4] - row2[7]
    # row2[5] = row2[5] - row2[8]
    # row2[6] = round((row2[4]/row2[5])*100,1)

    #changing W or L to 1 or 0
    if row1[1] == "W":
        row1[1] = 1
    else:
        row1[1] = 0

    if row2[1] == "W":
        row2[1] = 1
    else:
        row2[1] = 0
    
    #create our new rows for the data frame
    if away == True:
        new_row = [date] + row2 + row1 + [point_total]
    else:
        new_row = [date] + row1 + row2 + [point_total]

    #add the new row to our data frame
    new_df.loc[len(new_df.index)] = new_row




#export the csv file
new_df.to_csv('edited_data.csv', index=False)