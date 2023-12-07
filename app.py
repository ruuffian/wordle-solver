"""
Author: ruuffian
Name: app.py
Description:
    Runnable script to begin and solve a Worlde puzzle.
    Can also intereacted with to solve a puzzle besides the puzzle of the day.
"""

import src.scraper as site
import time
import src.wordlist as wordle
from src.wordlist import WordleState
import src.wrd_alg as alg


def check_wordle(state: WordleState, n_state: dict, word: str, ) -> dict:
    """
    Checks the result from the current guess, parsing letters into the black, yellow, and
    greenlists where appropriate
    :param state: Old WordleState
    :param n_state: New info scraped from wordle.com after :param word was input
    :param word: The most recent guess
    :return: New black/yellow/green lists based on the guessed word
    """
    board = n_state["boardState"]
    evaluations = n_state["evaluations"]
    i = 0
    bl = []
    yl = state.yellowlist
    corr = state.greenlist

    # iterates up to the latest guess
    while board[i] != word and i < 5:
        i += 1

    j = 0
    # checks each letter's result and adds them to the correct list
    for char in word:
        if evaluations[i][j] == "correct":
            corr[j] = char
        elif evaluations[i][j] == "present":
            yl[j].append(char)
        else:
            bl.append(char)
        j += 1
    return {
        "blacklist": bl,
        "yellowlist": yl,
        "greenlist": corr,
    }


def validate(word: str, a_state: WordleState) -> bool:
    """
    Argument validation for user-input words.
    :param word: The input from the User.
    :param a_state: The current state of the Worlde algorithm.
    :return: False if the word is invalid, True otherwise.
    """
    if len(word) != 5:
        return False
    if word not in a_state.pool:
        return False
    return str.isalpha(word)


if __name__ == '__main__':
    print("Welcome to ruuffian's Wordle solver!")
    Site = site.WebScraper()
    count = 0
    gamestate = Site.gamestate()
    print("Suggested starting words:\n"
          "Adieu\n"
          "Crane\n"
          "Taste\n")
    algstate = wordle.WordleState()

    while gamestate["gameStatus"] != "FINISHED":
        print("What word would you like to guess?")
        guess = input().lower()

        if not validate(guess, algstate):
            print("Invalid guess- Please try again.")
            continue

        Site.enter_word(guess)
        time.sleep(.5)
        gamestate = gamestate()
        word_results = check_wordle(algstate, gamestate, guess)
        # update blacklist, yellowlist, and greenlist
        algstate.update_info(word_results["blacklist"], word_results["yellowlist"], word_results["greenlist"])

        # update pool
        algstate.refine_list()

        # calculate best words
        suggestions = alg.pick(algstate)

        if gamestate["gameStatus"] == "IN_PROGRESS":
            print("Here are the 3 highest scoring words left in the wordpool:: \n" + str(suggestions))
            count += 1
    if gamestate["gameStatus"] == "WIN":
        print("Congrats (to me), you got the word right!" + "\n" + guess + " was the big ticket winner! GG!")
    else:
        print("dang you gotta get better at not making typos")
