"""
Author: ruuffian
Name: refine.py
Description:
    Algorithm that predicts the next best guess in a Wordle puzzle given the current gamestate.
    Assigns each word a score based on how many unique letters it contains and how frequently
    its letters appear in the main list of legal words.
"""

from wordlist import WordleState
from collections import defaultdict
from heapq import nlargest


# Default value for my defualt dictionary
def def_value() -> int:
    return 0


def uniqueness_score(wordin: str) -> int:
    """
    Calculates a score for the input string based on how many unique letters it contains.
    More unique letters means a higher score.
    A defualtdict is used to handle the first occurence of a letter and assign it 0
    :param wordin: 5 letter word to be scored
    :return: int -uniqueness score
    """
    score = 5
    letters = defaultdict(def_value)
    for i in range(5):
        letters[wordin[i]] += 1
        score -= letters[wordin[i]] - 1
    return score


def uniques(main: WordleState) -> defaultdict:
    """
    Creates and returns a defaultdict of every word's uniqueness score
    Used to normalize the scores
    :param main: main WordleState, essentially the entire game state
    :return: defaultdict -holds uniqueness scores keyed to the words, as well as a min and max value
    """
    uscores = defaultdict(def_value)
    for word in main.main:
        uscores[word] = uniqueness_score(word)
    return uscores


def letter_frequency(main: WordleState) -> defaultdict:
    """
    Creates a defaultdict of values that are each letter frequency scores
    More occurences means a higher frequency
    :param main: The main WordleState, essentially the gamestate
    :return: defaultdict -a dictionary containing all the letter frequency scores
    """
    freq = defaultdict(def_value)
    for word in main.main:
        for char in word:
            freq[char] += 1
    return freq


def frequency_score(word: str, freq: defaultdict) -> int:
    """
    Scores the input word based on a generated frequency dictionary
    More letters with high frequency means a higher frequency score
    :param word: The string to be scored
    :param freq: The frequency dictionary for the current wordpool
    :return:
    """
    score = 0
    for char in word:
        score += freq[char]
    return score


def frequencies(main: WordleState, freq: defaultdict) -> defaultdict:
    """
    Creates a defaultdict holding every frequency score keyed to the word
    Used to normalize the scores
    :param main: main WordleState, essentially the gamestate
    :param freq: frequency dictionary for the wordpool
    :return: defaultdict -holds frequency scores for the words, as well as a min and max value
    """
    fscores = defaultdict(def_value)
    for word in main.main:
        fscores[word] = frequency_score(word, freq)
    return fscores


def pick(main: WordleState) -> dict:
    """
    Gives each word in the wordpool a score based on its letter frequency and the number of unique letters,
    then returns the one with the highest score
    Unique letters are preferred because they are easier to implement than doing some sort of DFS alg to
    create an optimal tree
    Frequent letters are preferred because they also elminate more words
    :param main: The main WordleState, essentially the game state
    :return: dict -the 3 words with the highest calculated score
    """
    freq = letter_frequency(main)
    uniq_scores = uniques(main)
    freq_scores = frequencies(main, freq)
    # combine the scores
    combined = {}
    for word in main.main:
        combined[word] = uniq_scores[word] + .5 * freq_scores[word]
    scores = {}
    # We want to weigh the uniqueness score more heavily than the frequency
    for word in main.main:
        scores[word] = combined[word]
    largest = nlargest(3, scores, key=scores.get)
    ldict = {}
    for maxx in largest:
        ldict[maxx] = scores[maxx]
    return ldict
