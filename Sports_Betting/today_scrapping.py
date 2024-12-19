from bs4 import BeautifulSoup
import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_todays_teams():
    driver = webdriver.Chrome()  # You can change this to the appropriate driver for your browser

    day_class = "ScheduleDay_sd__GFE_w" #class of div for a days schedule
    name_class = "Anchor_anchor__cSc3P Link_styled__okbXW" #class of a tag containing team names
    URL = "https://www.nba.com/schedule?cal=all&region=1&season=Regular%20Season" 
    driver.get(URL)

    # Wait for the table to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, day_class)))

    # Get the updated page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    day_schedule = soup.find("div", class_=day_class) #find the first div tag (today's schedule)
    team_names = day_schedule.find_all("a", class_=name_class) #find all team names in today's schedule
    names = []
    #extract their text and put it in a list
    for item in team_names:
        names.append(item.text)

    #the home away order is flipped so have to fix that, and the games aren't in list pairs so have to fix that
    edited_names = []
    pair = []
    count = 0
    for i, name in enumerate(names):
        if count < 2:
            pair.insert(0, name)
        else:
            edited_names.append(pair)
            pair = []
            pair.insert(0, name)
            count = 0
        if i == len(names) - 1:
            edited_names.append(pair)
        count = count + 1

    #return the list to be inputted to get_team_data function
    return edited_names

def get_team_data(teams):
    #declaring variables and setting up driver 

    driver = webdriver.Chrome()  # You can change this to the appropriate driver for your browser

    table_class = "Crom_table__p1iZz" #class of table we are trying to find
    header_class = "Crom_headers__mzI_m" #class of row which contains headers that are used in the outputted csv file
    URL = "https://www.nba.com/stats/teams/traditional" 
    driver.get(URL)

    # Wait for the table to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, table_class)))

    # Get the updated page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    table_matches = soup.find("table", class_=table_class) #find our table

    #don't know if this sleep is needed, but I am keeping it
    if table_matches: 
        #extracting the headers
        tr_with_class = table_matches.find("tr", class_=header_class)

        th_elements = tr_with_class.find_all("th")
                
        # Now extracting the text content of headers and storing in a list
        header_list = [th.get_text(strip=True) for th in th_elements]

        #getting rid of all hidden headers (no idea why they exist)
        desired_length = 28
        num_to_pop = len(header_list) - desired_length
        for i in range(num_to_pop):
            header_list.pop()

        #creating home and away section and then putting them together
        H_list = ["H_" + item for item in header_list]
        A_list = ["A_" + item for item in header_list]
        full_headers = H_list + A_list


        #formatting and storing the data from the table
        rows = table_matches.find_all('tr')
        for row in rows:
            item = row.find('span')
            if item:
                name = item.text
                for matchup in teams:
                    if name in matchup:
                        index = matchup.index(name)
                        utils = []
                        cols = row.find_all('td')
                        for element in cols:
                            utils.append(element.text)
                        matchup[index] = utils
    else:
        print("error")
    print(teams)
    #appending the two team data lists together for each game
    combined_lists = [first_list + second_list for first_list, second_list in teams]

    driver.quit()
    # Close the Selenium driver

    # output all scrapped data into csv files
    df = pd.DataFrame(combined_lists, columns=full_headers)
    df.to_csv(f'today_game_data.csv', index=False)  

input = get_todays_teams()
get_team_data(input)


