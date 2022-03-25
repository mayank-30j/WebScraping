# Importing all essential libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import warnings
warnings.filterwarnings('ignore')


def scrape():
    path = r"C:\Users\mayan\OneDrive\Desktop\Mayank's folder\SeleniumDrivers\chromedriver.exe"
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome(path, options=option)

    driver.get('https://www.careerguide.com/career-options')
    job_categories = []
    job_subcategories = []

    # Getting job categories from carrier guide
    content = driver.find_elements(By.TAG_NAME, 'h2')

    for j in content:
        job_categories.append(j.text)

    # print(job_categories)

    # _____________________________________________________________________________________

    content = driver.find_elements(By.CLASS_NAME, 'col-md-4')
    temp_list = []

    # Getting job subcategories in a temporary list
    for jobs in content:
        temp_list.append(jobs.text)
    # print(temp_list)

    # Filtering the data in temp_list and appending to job_subcategories
    for text in temp_list:
        c = text.split('\n')
        job_subcategories.append(c)
    # print(job_subcategories)

    for i in job_subcategories:
        for j in i:
            if j in job_categories:
                i.remove(j)
    # print(job_subcategories)

    job_subcategories = [ele for ele in job_subcategories if ele != ['']]
    # print(job_subcategories)

    # Now we will make a dictionary for job_categories and job_subcategories
    job = dict()
    for i in range(len(job_categories)):
        job[job_categories[i]] = job_subcategories[i]
    # print(job)
    # print(job[job_title])
    return job
