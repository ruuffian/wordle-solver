"""
Author: ruuffian
Name: app.py
Description:
    Runnable script to begin and solve a Worlde puzzle.
    Can also intereacted with to solve a puzzle besides the puzzle of the day.
"""

import scraper as site
import time
import wordlist as wordle
from wordlist import WordleState


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
    count = 0
    gamestate = site.gamestate()
    print("Welcome to ruuffian's Wordle solver!")
    print("Suggested starting words:"
          "Adieu"
          "Crane"
          "Taste")
    algstate = wordle.WordleState()
    while gamestate["gameStatus"] != "FINISHED":
        print("What word would you like to guess?")
        guess = input()

        if not validate(guess, algstate):
            print("Invalid guess- Please try again.")
            continue

        site.enter_word(guess)
        time.sleep(.5)
        gamestate = gamestate()

        # update blacklist, yellowlist, and greenlist
        algstate.update_info(word_results["blacklist"], word_results["yellowlist"], word_results["greenlist"])

        # update wordpool
        algstate.pool = wordlist.lst_refine(algstate)

        # pick a word and suggest it, loop for next guess
        suggestions = wordlist.pick(algstate)
        if gamestate["gameStatus"] == "IN_PROGRESS":
            print("Here are the 5 highest scoring words left in the wordpool:: \n" + str(suggestions))
            count += 1

    if gamestate["gameStatus"] == "WIN":
        print("Congrats (to me), you got the word right!" + "\n" + guess + " was the big ticket winner! GG!")

    else:
        print("dang you gotta get better at not making typos")
