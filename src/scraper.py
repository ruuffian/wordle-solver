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
from time import sleep


class WebScraper:
    driver: WebDriver
    wordle: WebElement

    def __init__(self):
        # load chromedriver
        Service("resources/chromedriver.exe")
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        sleep(1)
        # make sure chrome loaded website correctly
        page_title = self.driver.title
        print(page_title)
        # remove annoying popup
        playButton = self.driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh")
        playButton.click()
        wordle = self.driver.find_element(By.TAG_NAME, "html")
        wordle.click()

    def enter_word(self, word: str) -> None:
        """
        Uses selenium's send_keys method to input a word
        :param word: The word to be input
        :return: void
        """
        self.wordle.send_keys(word)
        self.wordle.send_keys(Keys.ENTER)
        sleep(1)

    def gamestate(self, turn: int) -> list[str]:
        """
        Accesses wordle.com's LocalStorage with selenium's execute_script function.
        :return: json-ified data from localstorage["nyt-wordle-state]
        """
        state = []
        row = self.driver.find_elements(By.CSS_SELECTOR, f"[aria-label='Row {turn}'")
        for tile in row:
            tile_data = tile.find_element(By.XPATH, ".//div[]")
            tile_state = tile_data.get_attribute("data-state")
            state += tile_state
        return state
