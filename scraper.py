from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import chromedriver_binary
import time
import alg
import json


def enter_word(word):
    # Types and enters a word
    html.send_keys(word)
    html.send_keys(Keys.ENTER)
    time.sleep(1)


def grab_local():
    # Pull gamestate from localstorage
    local = driver.execute_script("return localStorage")
    gamestate = local["gameState"]
    return json.loads(gamestate)


def parse_local(local, wordin, corr):
    guesses = local["boardState"]
    bl = []
    yl = []
    i = 0
    # THIS IS WRONG, NEED TO MODULARIZE THIS
    while guesses[i] != wordin and i < len(guesses):
        i += 1
    for let in wordin:
        if local["evaluations"][i] == "correct":
            corr[i] = let
        elif local["evaluations"][i] == "present":
            yl.append(let)
        else:
            bl.append(let)
    return {
        "blacklist": bl,
        "yellowlist": yl,
        "greenlist": corr,
    }


if __name__ == '__main__':
    s = Service(chromedriver_binary.chromedriver_filename)
    driver = webdriver.Chrome()
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    time.sleep(1)
    page_title = driver.title
    print(page_title)
    html = driver.find_element(By.TAG_NAME, "html")
    html.click()
    gamestate = grab_local()
    blacklist = []
    yellowlist = []
    correct = ["0", "0", "0", "0", "0"]
    count = 0
    masterlist = {
        "blacklist": blacklist,
        "yellowlist": yellowlist,
        "greenlist": correct,
        "lst": alg.load_words(),
    }
    while gamestate["gameStatus"] == "IN_PROGRESS" or count < 6:
        print("What word would you like to guess?")
        guess = input()
        # Need arg validation: no nums, special chars, exactly 5 chars long
        enter_word(guess)
        time.sleep(1)
        gamestate = grab_local()
        post_word = parse_local(gamestate, guess, correct)
        blacklist.append(post_word["blacklist"])
        yellowlist.append(post_word["yellowlist"])
        correct = post_word["greenlist"]
        masterlist = alg.lst_refine(masterlist["lst"], masterlist["blacklist"], masterlist["yellowlist"],
                                    masterlist["greenlist"])
        print("I suggest this word- " + alg.pick(masterlist))
        count += 1

    driver.close()
