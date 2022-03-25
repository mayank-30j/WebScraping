from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver as wd
import time


def convert(lst, var_lst):  # This function converts 1D list into 2D list
    idx = 0
    for var_len in var_lst:
        yield lst[idx: idx + var_len]
        idx += var_len


def find_longest_distance(driver):  # This function will find the winner
    longest_distance = None
    for i in range(1, 15):
        try:
            longest_distance = driver.find_element(By.XPATH, f"//tr[{i}]//div[@class='trophycontainer']//span[contains(@title,'Longest Distance')]")
        except NoSuchElementException:
            pass
        if longest_distance is not None:
            return i


def find_least_distance(driver):  # This function will find the racer with the least distance
    least_distance = None
    for i in range(1, 15):
        try:
            least_distance = driver.find_element(By.XPATH, f"//tr[{i}]//div[@class='trophycontainer']//span[contains(@title,'Least Distance')]")
        except NoSuchElementException:
            pass
        if least_distance is not None:
            return i


def fastest_sectional(driver):
    f = None
    for i in range(1, 15):
        pass
