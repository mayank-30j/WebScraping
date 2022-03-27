# Importing all the required libraries
from selenium import webdriver
from WebScraping_ATG import scrape
from selenium.webdriver.common.by import By
import warnings
warnings.filterwarnings('ignore')

# These are all the states based on which i have to scrape data from linkedin
states = ["Andhra Pradesh","Arunachal Pradesh ", "Assam", "Bihar", "Chhattisgarh","Goa","Gujarat","Haryana",
          "Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra",
          "Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
          "Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh",
          "Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]

jobs = scrape()  # This is a dictionary that contains job Categories as key and subcategories (in list form) as value
# as key : value pair

path = r"C:\Users\mayan\OneDrive\Desktop\Mayank's folder\SeleniumDrivers\chromedriver.exe"
# option = Options()
# option.add_argument('--headless')  # This prevents my browser from showing up again and again as I run the code
driver = webdriver.Chrome(path)

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# Now we will login to linked in using the username and password

# My username
username = driver.find_element(By.NAME, 'session_key')
username.send_keys("mayank30j@gmail.com")
# My Password
password = driver.find_element(By.NAME, 'session_password')
password.send_keys("***") # Password here

# Clicking the button/ login to linkedin account
login_button = driver.find_element(By.CLASS_NAME, 'login__form_action_container ')
login_button.click()

driver.get('https://www.linkedin.com/jobs/')

company_name = None
job_categories = list(jobs.keys())

for state in states:
    for job in job_categories:
        search_job = driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input')
        search_job.send_keys(job)

        search_state = driver.find_element(By.ID, 'jobs-search-box-location-id-ember31')
        search_state.send_keys(state)

        search_button = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
        search_button.click()

        search_job.send_keys('')
        search_state.send_keys('')

company_name = driver.find_elements(By.CLASS_NAME, 'job-card-container__link')

