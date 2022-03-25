# import undetected_chromedriver as uc
import warnings
import time
import numpy as np
import pandas as pd
import My_Functions
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------------------------------------------------------
ua = UserAgent()
useragent =   ua.data_randomize
options = Options()
options.add_argument(f'user-agent = {useragent}')

url = 'C:\Program Files\chromedriver.exe'
driver = webdriver.Chrome(url,options=options)

driver.get("https://www.gmaxequine.com/TPD/public/sectionals.aspx?ShareCode=30201512191205")
driver.implicitly_wait(10)  # Wait for 10 seconds before the window closes

WebDriverWait(driver,10).until(EC.alert_is_present())
driver.switch_to.alert.accept()

# Click on the input field or date Picker
driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").click()

# These 2 are pervious and next buttons on the calendar
previous_cal = driver.find_element(By.XPATH,"//div[@class='ajax__calendar_header']//div[@class='ajax__calendar_prev']")
next_cal = driver.find_element(By.XPATH,"//div[@class='ajax__calendar_header']//div[@class='ajax__calendar_prev']")

# We will make calendar previous button click until it reaches 2015,Dec
for i in range(75):
    previous_cal.click()

# ----------------------------------------------------------------------------------------------------------------------
for _ in range(75):

    # Find the active dates in each month
    cal_dates = driver.find_elements(
    By.XPATH,"//tbody[@id='ctl00_cphPage_rdn1_rdn_racedate_CalendarExtender_daysBody']//td[not(contains(@class,'ajax__calendar_invalid') or contains(@class,'ajax__calendar_hover') or contains(@class,'ajax__calendar_other'))]//div[@class='ajax__calendar_day']"
    )

    # Fetching the calendar title
    cal_title = driver.find_element(By.XPATH,"//div[@class='ajax__calendar_title']").text

    for date in cal_dates:
        d = date.text
        driver.find_element(By.XPATH, f"//div[@class='ajax__calendar_body']//div[text()='{d}']").click()

        # Selecting from drop down menu
        dropdown = driver.find_element(By.ID, 'ctl00_cphPage_rdn1_rdn_ddlSessions')  # Finding the dropdown webelement by ID
        select = Select(dropdown)
        options = select.options   # Select the options from dropdown menu

        for index in range(0, len(options)):
            select.select_by_index(index)
            time.sleep(5)
            select = Select(driver.find_element(By.ID, 'ctl00_cphPage_rdn1_rdn_ddlSessions'))
            options = select.options  # Select the options from dropdown menu

        # Fetching the Page heading 1 and Page heading 2 by Date in calendar and by sessions

            heading = driver.find_element(By.XPATH, "//div[@class='w50 fll tal']//h1").text
            heading2 = driver.find_element(By.XPATH, "//div[@class='w50 fll tal']//h2").text


            # Fetching all the column headings for sectionals_heading
            col_main_heading = driver.find_elements(By.XPATH, "//td[@class='RaceGridHeader DoubleLine Gate']//span[@class='RaceGridHeader']")
            col_sub_heading = driver.find_elements(By.XPATH, "//td[@class='RaceGridHeader DoubleLine Gate']//span[@class='RaceGridHeaderSub Time']")

            sectionals_heading = [i for i in range(len(col_main_heading))]
            for i in range(0, (len(col_main_heading))):
                sectionals_heading[i] = col_main_heading[i].text + "  "+ col_sub_heading[i].text


            # Now it will fetch values in each column in different list as per column
            result_values = driver.find_elements(By.XPATH, "//span[@class='RaceGridFinishPosition']")
            result_values2 = driver.find_elements(By.XPATH, "//span[@class='RaceGridFinishTime']")
            Draw1 = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackCode b']")
            Draw2 = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackVest']")
            track_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrackName b']")
            trainer_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridTrainerName']")
            rider_name = driver.find_elements(By.XPATH, "//span[@class='RaceGridRiderName']")


            # This will contain list of webelement object and not the actual text
            RaceGridTimeGrid = driver.find_elements(By.XPATH,"//td[@class='RaceGridCell Gate']//span[@class='RaceGridGateTimeMid']")
            # This will contain the actual text
            RaceGridTimeGrid2 = [float(time.text) for time in RaceGridTimeGrid]

            # This contain 2D list of sectinal values
            RaceTime = list(My_Functions.convert(RaceGridTimeGrid2,[len(col_main_heading)]*len(result_values2)))

            # These are the column values in text form
            result = [i.text + "  " +j.text for i, j in zip(result_values, result_values2)]
            draw = [i.text + " " + j.text for i, j in zip(Draw1, Draw2)]
            horse = [i.text+" "+j.text+" "+k.text for i, j, k in zip(track_name, trainer_name, rider_name)]

            # This will be our dict for pandas dataframe
            table1 = {'Date':str(d+" "+cal_title),'Session':options[index].text,'Result': result, 'No. (Draw)': draw, 'Horse Trainer Jockey': horse}
            # table2 = {'Winner':'','Least_distance':'','Long_distance':'','Fastast Sectional':''}

            # Converting them to Pandas DataFrame
            sectional_table = pd.DataFrame(RaceTime,columns=sectionals_heading)
            table1 = pd.DataFrame(table1)

            # This is the final resultig table
            df_new = pd.concat([table1,sectional_table], axis=1)

    #         df_temp = df_temp.append(df_new,ignore_index=True) # Merde df_new into df_temp vertically
    #         # df_new.to_excel(r'C:\Users\mayan\OneDrive\Desktop\Fiverr\Demo2.xlsx',index=False)
    #
    #     df_temp.to_excel(r'C:\Users\mayan\OneDrive\Desktop\Fiverr\Demo2.xlsx',index=False)
    #     exit()
    # driver.find_element(By.XPATH, "//div[@id='divNavControl']//input[contains(@class,'TPDform')]").click()
    # next_cal.click()
