import warnings
from openpyxl import Workbook
import pandas as pd
from My_Functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
warnings.filterwarnings("ignore")
# from selenium.webdriver.support import expected_conditions as EC
# from fake_useragent import UserAgent
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait

# ----------------------------------------------------------------------------------------------------------------------

# Defining a DataFrame for later use
df_temp = pd.DataFrame

url = r'C:\Program Files\msedgedriver.exe'
driver = webdriver.Edge(url)

driver.get("https://www.gmaxequine.com/TPD/public/sectionals.aspx?ShareCode=30201512191205")
driver.implicitly_wait(10)  # Wait for 10 seconds before the window closes


for year in range(2016, 2022):  # Iterates from one year to next

    for month in range(1, 13):  # Iterate from one month to next month

        for date in (1, 32):  # Iterate from one date to next date

            if year in [2017, 2018, 2019, 2021, 2022]:
                if month in [4, 7, 9, 11] and date >= 31:
                    break
                elif month == 2 and date > 28:
                    break
            elif year in [2016, 2020]:
                if month in [4, 7, 9, 11] and date >= 31:
                    break
                elif month == 2 and date > 29:
                    break

            # Click on the input field or date Picker and send the date to calendar in format yyyy-mm-dd
            driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").clear()

            driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").send_keys(f'{year}-{month}-{date}')
            driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").send_keys(Keys.ENTER)

            # Fetching the calendar title
            driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").click()
            cal_title = driver.find_element(By.XPATH, "//div[@class='ajax__calendar_title']").text

            # Selecting from drop down menu
            dropdown = driver.find_element(By.ID, 'ctl00_cphPage_rdn1_rdn_ddlSessions')  # Finding the dropdown webelement by ID
            select = Select(dropdown)
            options = select.options   # Select the options from dropdown menu

            # Creating a new Excel Workbook and entering data in it
            wb = Workbook()
            wb.save(filename=fr'C:\Users\mayan\OneDrive\Desktop\Fiverr\HorseRaceOn {cal_title}.xlsx')

            for index in range(0, len(options)):  # Iterate from one Option to Option in DropDown
                select.select_by_index(index)
                time.sleep(3)
                select = Select(driver.find_element(By.ID, 'ctl00_cphPage_rdn1_rdn_ddlSessions'))
                options = select.options  # Select the options from dropdown menu

                # Fetching the Page heading 1 and Page heading 2 by Date in calendar and by sessions
                heading = driver.find_element(By.XPATH, "//div[@class='w50 fll tal']//h1").text
                heading2 = driver.find_element(By.XPATH, "//div[@class='w50 fll tal']//h2").text

                # Fetching all the column headings for sectionals_heading
                Distance = driver.find_elements(By.XPATH, "//td[@class='RaceGridHeader DoubleLine Gate']//span[@class='RaceGridHeader']")
                Time = driver.find_elements(By.XPATH, "//td[@class='RaceGridHeader DoubleLine Gate']//span[@class='RaceGridHeaderSub Time']")

                Distance = [d.text for d in Distance]
                Time = [t.text for t in Time]

                # Now it will fetch values in each column in different list as per column
                finishPosition = driver.find_elements(By.XPATH, "//span[@class='RaceGridFinishPosition']")
                finishTime = driver.find_elements(By.XPATH, "//span[@class='RaceGridFinishTime']")
                number = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackCode b']")
                Draw = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackVest']")
                track_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackName b']")
                trainer_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrainerName']")
                rider_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridRiderName']")

                # This will contain list of webelement object and not the actual text
                RaceGridTimeGrid = driver.find_elements(By.XPATH, "//td[@class='RaceGridCell Gate']//span[@class='RaceGridGateTimeMid']")

                # This will contain the actual text and converting 1D list into 2D list
                RaceTime = list(convert([time.text for time in RaceGridTimeGrid], [len(Distance)]*len(finishTime)))

                # Defining some more lists for winner, least and longest distance
                winner = [0] * len(finishPosition)
                long = [0] * len(finishPosition)
                least = [0] * len(finishPosition)
                # fast = [0]

                # These two functions will find the index of row for longest distance and least distance rider in the table
                longDistance = find_longest_distance(driver)
                leastDistance = find_least_distance(driver)

                # Adding some more columns in table1
                for i in range(0, len(finishPosition)+2):
                    if i == 0:
                        winner[i] = 1
                    if (leastDistance-2) > 0:
                        if i == leastDistance-2:
                            least[i] = 1
                    if (longDistance-2) > 0:
                        if i == longDistance-2:
                            long[i] = 1
                    else:
                        least[0] = 1
                        long[0] = 1

                # This will be our dict for pandas dataframe
                table1 = {
                    "Race Date": f'{year}-{month}-{date}',
                    'Finish Position': [n.text for n in finishPosition],
                    'Finish Time': [f.text for f in finishTime],
                    'Number ': [i.text for i in number],
                    'Draw': [d.text for d in Draw],
                    'Track Name': [t.text for t in track_name],
                    'Trainer Name': [t.text for t in trainer_name],
                    'Horse Rider Name': [t.text for t in rider_name],
                    'Winner': winner,
                    'Least Distance': least,
                    'Longest Distance': long,
                }

                # Now converting the Table1 into data frame
                table1 = pd.DataFrame(table1)

                # table1['Fastest Sectional'] = 0

                # Converting RaceTime to Pandas DataFrame
                sectional_table = pd.DataFrame(RaceTime, columns=Distance)

                # This is the final resulting table
                df_new = pd.concat([table1, sectional_table], axis=1)

                # Enter
                with pd.ExcelWriter(fr'C:\Users\mayan\OneDrive\Desktop\Fiverr\HorseRaceOn {cal_title}.xlsx', engine="openpyxl", mode='a') as writer:
                    df_new.to_excel(writer, index=False, sheet_name=f'{date} {options[index].text}', na_rep='-')
            driver.close()
            exit()
driver.close()
