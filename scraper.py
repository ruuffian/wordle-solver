"""
Author: ruuffian
Name: scraper.py
Description:
    Methods for scraping data from wordle.com, used to programmatically solve Wordle puzzles.
"""

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import time
import json


# load chromedriver
s = Service("chromedriver.exe")
driver = webdriver.Chrome()
driver.get("https://www.powerlanguage.co.uk/wordle/")
time.sleep(1)
# make sure chrome loaded website correctly
page_title = driver.title
print(page_title)
# remove annoying popup
html = driver.find_element(By.TAG_NAME, "html")
html.click()


def enter_word(word: str):
    """
    Uses selenium's send_keys method to input a word
    :param word: The word to be input
    :return: void
    """
    html.send_keys(word)
    html.send_keys(Keys.ENTER)
    time.sleep(1)


def gamestate():
    """
    Accesses wordle.com's LocalStorate with selenium's execute_script function.
    :return: json-ified data from localstorage["nyt-wordle-state]
    """
    local = driver.execute_script("return localStorage")
    state = local["nyt-wordle-state"]
    return json.loads(state)



