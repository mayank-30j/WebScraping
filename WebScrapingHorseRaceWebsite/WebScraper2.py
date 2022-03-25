# Importing all the required libraries
from importlib.resources import contents
from turtle import st
import pandas as pd
import requests
import re
import time
import warnings
from pandas import ExcelWriter
from openpyxl import Workbook
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
# from Secrets import API_KEY
warnings.filterwarnings('ignore')

data_table = pd.DataFrame({}, columns=['StartTime', 'TrackName', 'col_name', 'SerialNumber', 'HorseName', 'Race',
                                       'Wins_num', 'Average DOB', 'Wins_percent', 'Average Drop', 'Average Rise',
                                       'PR Drift', 'PR Steam'])

url = "https://racingdata.info/"
option = Options()
driver_path = r'C:\Program Files\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path, options=option)
driver.get(url)

# Selecting from drop down menu
dropdown = driver.find_element(By.XPATH,'//select[contains(@class,"p-2 h-p50 w-full min-w-select")]')  # Finding the dropdown webelement by ID
select = Select(dropdown)
options = select.options  # Select the options from dropdown menu

# Iterating over the dropdown list
for index in range(0, len(options)):
    select.select_by_index(index)
    time.sleep(3)
    select = Select(driver.find_element(By.XPATH, '//select[contains(@class,"p-2 h-p50 w-full min-w-select")]'))
    options = select.options  # Select the options from dropdown menu

    button = driver.find_elements(By.XPATH, "//button[contains(@class,'flex p-0 flex-wrap w-full bg-white')]")

    # Creating a new Excel Workbook and entering data in it
    wb = Workbook()
    wb.save(filename=f'./{index}.xlsx')

    for i in range(len(button)):
        button = driver.find_elements(By.XPATH, "//button[contains(@class,'flex p-0 flex-wrap w-full bg-white')]")[i]
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        list_tags = soup.find_all('li', class_='p-3 mb-2')

        # Text on the button / track info
        for j in range(len(list_tags)):
            startTime = [list_tags[j].button][0].text
            trackname = [list_tags[j].button][2].text
            col_name = [list_tags[j].button][3].text  # I don't know this column name

            file_name = [str(i).split(' ',) for i in trackname]

            div_tags = list_tags[j].find_all('div',class_='relative')

        # Text inside the button / race info per track class = relative
            for n in range(len(div_tags)):
                serialnumber = div_tags[n].button.div.div.header.div.div[0].text
                horseName = div_tags[n].button.div.div.header.div.div[1].text
                races = div_tags[n].button.div.div.d1[0].div.dt.text
                wins_num = div_tags[n].button.div.div.d1[1].div.dt.text
                avg_dob = div_tags[n].button.div.div.d1[2].div.dt.text
                win_per =  div_tags[n].button.div.div.d1[3].div.dt.text
                avg_drop = div_tags[n].button.div.div.d1[4].div.dt.text
                avg_rise = div_tags[n].button.div.div.d1[5].div.dt.text
                pr_drift = div_tags[n].button.div.div.d1[6].div.dt.text
                pr_steam = div_tags[n].button.div.div.d1[7].div.dt.text


                data_table.loc[n,'TrackName'] = trackname
                data_table.loc[n,'StartTime'] = startTime
                data_table.loc[n,'col_name'] = col_name
                data_table.loc[n,'SerialNumber'] = serialnumber
                data_table.loc[n,'HorseName'] = horseName
                data_table.loc[n,'Race'] = races
                data_table.loc[n,'Win_num'] = wins_num
                data_table.loc[n,'Average DOB'] = avg_dob
                data_table.loc[n,'Win_percent'] = win_per
                data_table.loc[n,'Average Drop'] = avg_drop
                data_table.loc[n,'Average Rise'] = avg_rise
                data_table.loc[n,'PR Drift'] = pr_drift
                data_table.loc[n,'PR Stem'] = pr_steam

    # with pd.ExcelWriter(f'./{trackname}',engine="openpyxl", mode='a') as writer:
    #     data_table.to_excel(writer,sheet_name=f'{trackname}',na_rep='NaN',index=False)

driver.close()