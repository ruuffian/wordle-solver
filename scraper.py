from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import chromedriver_binary
import time
import alg
import json
import refine


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
def parse_local(local, wordin, master):
    guesses = local["boardState"]
    curr = wordin
    i = 0
    while curr != guesses[i] and i < 5:
        i += 1
    bl = []
    yl = master.yellowlist
    corr = master.greenlist
    j = 0
    # THIS IS WRONG, NEED TO MODULARIZE THIS
    for let in wordin:
        if local["evaluations"][i][j] == "correct":
            corr[j] = let
        elif local["evaluations"][i][j] == "present":
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
    yellowlist = [[], [], [], [], []]
    greenlist = ["0", "0", "0", "0", "0"]
    count = 0
    masterlist = alg.WordList()
    masterlist.update_lists(blacklist, yellowlist, greenlist)
    masterlist.refine_list(alg.load_words())
    # loop until game is won or lost
    suggestion = ""
    while gamestate["gameStatus"] == "IN_PROGRESS" and count < 6:
        print("What word would you like to guess?")
        guess = input()
        # Need arg validation: no nums, special chars, exactly 5 chars long
        enter_word(guess)
        time.sleep(1)
        # grab localstorage
        gamestate = grab_local()
        # read localstorage to determine what the guess resulted in
        post_word = parse_local(gamestate, guess, masterlist)
        # update blacklistm yellowlist, and greenlist
        masterlist.update_lists(post_word["blacklist"], post_word["yellowlist"], post_word["greenlist"])
        # update possible word list
        masterlist.master = refine.lst_refine(masterlist)

        # pick a word and suggest it, loop for next guess
        suggestion = alg.pick(masterlist)
        print("I suggest this word- " + suggestion)
        count += 1
    if gamestate["gameStatus"] == "WIN":
        print("Congrats (to me), you got the word right!" + "\n" + suggestion + " was the big ticket winner! GG!")
    else:
        print("dang you gotta get better at not making typos")

    driver.close()
    exit(0)
