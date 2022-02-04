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


# NEED TO CHANGE FROM DOUBLE ITERATE TO PASSING A COUNT THROUGH METHOD SIG
def parse_local(local, wordin, corr):
    guesses = local["boardState"]
    curr = wordin
    i = 0
    while curr != guesses[i]:
        i += 1
    bl = []
    yl = []
    j = 0
    # THIS IS WRONG, NEED TO MODULARIZE THIS
    for let in wordin:
        if local["evaluations"][i][j] == "correct":
            corr[j] = let
        elif local["evaluations"][i][j] == "present":
            yl.append(let)
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
    s = Service(chromedriver_binary.chromedriver_filename)
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
    # loop until game is won or lost
    while gamestate["gameStatus"] == "IN_PROGRESS" and count < 6:
        print("What word would you like to guess?")
        guess = input()
        # Need arg validation: no nums, special chars, exactly 5 chars long
        enter_word(guess)
        time.sleep(1)
        # grab localstorage
        gamestate = grab_local()
        # read localstorage to determine what the guess resulted in
        post_word = parse_local(gamestate, guess, correct)
        # update blacklistm yellowlist, and greenlist
        blacklist.extend(post_word["blacklist"])
        yellowlist.extend(post_word["yellowlist"])
        correct = post_word["greenlist"]
        # update possible word list
        masterlist = alg.lst_refine(masterlist["lst"], masterlist["blacklist"], masterlist["yellowlist"],
                                    masterlist["greenlist"])
        # pick a word and suggest it, loop for next guess
        print("I suggest this word- " + alg.pick(masterlist))
        count += 1
    if gamestate["gameStatus"] == "WIN":
        print("Congrats (to me), you got the word right!")
    else:
        print("dang you gotta get better at not making typos lmfao- bg")

    driver.close()
    exit(0)

