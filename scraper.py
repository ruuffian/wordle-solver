"""
Author: ruuffian
Name: scraper.py
Description:
    Methods for scraping data from wordle.com, used to programmatically solve Wordle puzzles.
"""

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import time
import json


class WebScraper:
    driver: WebDriver
    html: WebElement

    def __init__(self):
        # load chromedriver
        Service("chromedriver.exe")
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.powerlanguage.co.uk/wordle/")
        time.sleep(1)
        # make sure chrome loaded website correctly
        page_title = self.driver.title
        print(page_title)
        # remove annoying popup
        html = self.driver.find_element(By.TAG_NAME, "html")
        html.click()

    def enter_word(self, word: str) -> None:
        """
        Uses selenium's send_keys method to input a word
        :param word: The word to be input
        :return: void
        """
        self.html.send_keys(word)
        self.html.send_keys(Keys.ENTER)
        time.sleep(1)

    def gamestate(self) -> json:
        """
        Accesses wordle.com's LocalStorage with selenium's execute_script function.
        :return: json-ified data from localstorage["nyt-wordle-state]
        """
        local = self.driver.execute_script("return localStorage")
        state = local["nyt-wordle-state"]
        return json.loads(state)
