from bs4 import BeautifulSoup
import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools


#declaring variables and setting up driver 

driver = webdriver.Chrome()  # You can change this to the appropriate driver for your browser

table_class = "Crom_table__p1iZz" #class of table we are trying to find
dropdown_class = "DropDown_select__4pIg9" #class of dropdown for cycling through years
header_class = "Crom_headers__mzI_m" #class of row which contains headers that are used in the outputted csv file
pageflip_class = "Pagination_button__sqGoH"
URL = "https://www.nba.com/stats/teams/boxscores-traditional?Season=2022-23" 
driver.get(URL)

# Wait for the table to load (adjust the timeout as needed)
wait = WebDriverWait(driver, 15)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, table_class)))

# Find the dropdown element by its class
dropdown = driver.find_element(By.CLASS_NAME, dropdown_class)

# Get all the available options within the dropdown
options = dropdown.find_elements(By.TAG_NAME, 'option')

# Create empty lists to store the scraped data for games in the year and all year datas
year_data = []
all_data = []

year_to_loop_through = 4
#only looping through first 4 years
for option in itertools.islice(options, year_to_loop_through):
      # Select the year option
    option.click()
    
    
    #looping through the first 10 pages of game data for the year
    for i in range(10):

        # Wait for the table to reload (adjust the timeout as needed)
        try:
            load = wait.until(EC.presence_of_element_located((By.CLASS_NAME, table_class)))
        except TimeoutError:
            print("error")

        #it wasn't working without this sleep function so I am just leaving it here
        time.sleep(2)
        # Get the updated page source
        page_source = driver.page_source
        
        #get the buttons (there's 2, one for forwards, one for backwards)
        page_buttons = driver.find_elements(By.CLASS_NAME, pageflip_class)
        if page_buttons:
            #first checking to make sure buttons exist, then choosing the forwards one
            next_page = page_buttons[1]
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        table_matches = soup.find("table", class_=table_class) #find our table
        if table_matches:
            #append the page to the year data
            year_data.append(table_matches)
        else:
            #this is mainly for ongoing seasons that don't have data, but also for debugging
            print("table not found in " + str(options.index(option)))   

        try:
            #click to the next page
            next_page.click()
        except Exception as e:
             #if this doesn't work (i.e end of list or buttons aren't there)
             #we want to break out of the loop and go to the next year
             print(f"An error occurred: {e}")
             break
        
    #don't know if this sleep is needed, but I am keeping it
    time.sleep(2)
    if table_matches: 
        #extracting the headers
        tr_with_class = table_matches.find("tr", class_=header_class)

        th_elements = tr_with_class.find_all("th")
                
        # Now extracting the text content of headers and storing in a list
        header_list = [th.get_text(strip=True) for th in th_elements]


        #formatting and storing the data from the table
        data = []
        for item in year_data:
            rows = item.find_all('tr')
            for row in rows:
                utils = []
                cols = row.find_all('td')
                for element in cols:
                    utils.append(element.text)
                data.append(utils)

        all_data.append(data)

    else:
        #this is mainly for ongoing seasons that don't have data, but also for debugging
        print("table not found in " + str(options.index(option)))
    year_data = []

driver.quit()
# Close the Selenium driver

#output all scrapped data into csv files
for i, data in enumerate(all_data):
    df = pd.DataFrame(data, columns=header_list)
    df.to_csv(f'nba_data_{i}.csv', index=False)  





