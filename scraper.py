"""
Author: ruuffian
Name: scraper.py
Description:
    This is the python file that interacts with wordle.com using selenium
"""

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import time
import alg
import json
import refine
from alg import WordList
from heapq import nlargest


def enter_word(word):
    """
    Uses selenium's send_keys method to input a word
    :param word: The word to be input
    :return: void
    """
    html.send_keys(word)
    html.send_keys(Keys.ENTER)
    time.sleep(1)


def grab_gamestate():
    """
    Uses javascript and the execute_script method to gain access to Wordle's local storage
    :return: json-ified data from localstorage, specifically gameState
    """
    local = driver.execute_script("return localStorage")
    state = local["nyt-wordle-state"]
    return json.loads(state)


def check_wordle(localstate: dict, wordin: str, master: WordList) -> dict:
    """
    Checks the result from the current guess, parsing letters into the black, yellow, and
    greenlists where appropriate
    :param localstate: json-ified string from localstorage[gamestate]
    :param wordin: The current guess
    :param master: The master WordList
    :return: New black/yellow/green lists based on the guessed word
    """
    guesses = localstate["boardState"]
    curr = wordin
    i = 0

    # iterates up to the latest guess
    while curr != guesses[i] and i < 5:
        i += 1
    bl = []
    yl = master.yellowlist
    corr = master.greenlist
    j = 0

    # checks each letter's result and adds them to the correct list
    for let in wordin:
        if localstate["evaluations"][i][j] == "correct":
            corr[j] = let
        elif localstate["evaluations"][i][j] == "present":
            yl[j].append(let)
        else:
            bl.append(let)
        j += 1
    return {
        "blacklist": bl,
        "yellowlist": yl,
        "greenlist": corr,
    }


if __name__ == '__main__':

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

    # intialize variables
    gamestate = grab_gamestate()

    count = 0
    masterlist = alg.WordList()
    masterlist.refine_list(alg.load_words())

    # loop until game is won or lost
    suggestion = ""
    while gamestate["gameStatus"] == "IN_PROGRESS" and count < 6:
        print("What word would you like to guess?")
        guess = input()

        # Need arg validation: no nums, special chars, exactly 5 chars long
        enter_word(guess)
        time.sleep(1)
        gamestate = grab_gamestate()
        word_results = check_wordle(gamestate, guess, masterlist)

        # update blacklist, yellowlist, and greenlist
        masterlist.update_lists(word_results["blacklist"], word_results["yellowlist"], word_results["greenlist"])

        # update wordpool
        masterlist.master = refine.lst_refine(masterlist)

        # pick a word and suggest it, loop for next guess
        suggestions = alg.pick(masterlist)
        if gamestate["gameStatus"] == "IN_PROGRESS":
            print("Here are the 5 highest scoring words left in the wordpool:: \n" + str(suggestions))
            count += 1

    if gamestate["gameStatus"] == "WIN":
        print("Congrats (to me), you got the word right!" + "\n" + suggestion + " was the big ticket winner! GG!")

    else:
        print("dang you gotta get better at not making typos")
    print("Finished?")
    input()
    driver.close()
    exit(0)