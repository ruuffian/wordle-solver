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
import wrd_alg as alg


def check_wordle(localstate: dict, word: str, alg: WordleState) -> dict:
    """
    Checks the result from the current guess, parsing letters into the black, yellow, and
    greenlists where appropriate
    :param localstate: json-ified string from localstorage[gamestate]
    :param word: The current guess
    :param alg: Current WordleState
    :return: New black/yellow/green lists based on the guessed word
    """
    board = localstate["boardState"]
    evaluations = localstate["evaluations"]
    i = 0
    bl = []
    yl = alg.yellowlist
    corr = alg.greenlist

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
        word_results = check_wordle(gamestate, guess, algstate)
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
