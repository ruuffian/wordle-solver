from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import chromedriver_binary
import time


def enter_word(word):
    # Types and enters a word
    html.send_keys(word)
    html.send_keys(Keys.ENTER)
    time.sleep(1)


def letter(index):
    return chr(95 + index)


def grab_keys():
    # Cascades through the DOM to find the key data to blacklist, yellowlist, and correctlist letters
    app = driver.find_element(By.TAG_NAME, "game-app")
    # execute script bypasses the shadow-root
    game = driver.execute_script("return arguments[0].shadowRoot.getElementById('game')", app)
    keyboard = game.find_element(By.TAG_NAME, "game-keyboard")
    keys = driver.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)
    time.sleep(1)
    keydata = {}
    rows = keys.find_elements(By.CLASS_NAME, "row")
    print(rows)
    for e in rows:
        for i in range(26):
            keydata[letter(i)] = e.find_elements(By.CSS_SELECTOR, r"#button[data-key]")
    print(keydata)
    return keydata


if __name__ == '__main__':
    s = Service(chromedriver_binary.chromedriver_filename)
    driver = webdriver.Chrome()
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    time.sleep(1)
    page_title = driver.title
    print(page_title)
    html = driver.find_element(By.TAG_NAME, "html")
    html.click()
    enter_word("Hello Wordle")
    grab_keys()
    driver.close()
