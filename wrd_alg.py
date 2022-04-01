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


def uniqueness_score(word: str) -> int:
    """
    Calculates a words uniquness score. More unique letters = higher score.
    :param word: The word to be evaluated.
    :return: The calculated uniquness score.
    """
    score = len(word)
    letters = defaultdict(def_value)
    for i in range(len(word)):
        letters[word[i]] += 1
        score -= letters[word[i]] - 1
    return score


def uniques(word_list: list[str]) -> defaultdict:
    """
    Creates and returns a defaultdict of every word's uniqueness score
    :param word_list: List of all legal words.
    :return: dictionary of words:uniqueness_score
    """
    uscores = defaultdict(def_value)
    for word in word_list:
        uscores[word] = uniqueness_score(word)
    return uscores


def f_score(word: str, freq: defaultdict) -> int:
    """
    Calculates a given words frequency score.
    :param word: The word being evaluated.
    :param freq: A dictionary of letter:frequency.
    :return: Sum of f_scores in a given word.
    """
    score = 0
    for char in word:
        score += freq[char]
    return score


def frequency_scores(word_list: list[str], freq: defaultdict) -> defaultdict:
    """
    Calculates the frequency score for every word in the legal wordpool.
    :param word_list: List of legal words.
    :param freq: frequency dictionary for the wordpool
    :return: A dictionary of word:frequency_score.
    """
    fscores = defaultdict(def_value)
    for word in word_list:
        fscores[word] = f_score(word, freq)
    return fscores


def letter_frequency(word_list: list[str]) -> defaultdict:
    """
    Counts the frequency of every letter based on the legal word pool.
    :param word_list: List of all legal words.
    :return: A dictionary of letter:frequency.
    """
    freq = defaultdict(def_value)
    for word in word_list:
        for char in word:
            freq[char] += 1
    return freq


def pick(algstate: WordleState) -> dict:
    """
    Picks the 3 highest scoring words in the legal word pool given the current state of the puzzle.
    Scores are determined based on two factors:
        Frequency: Words with letters that appear more frequently in the list of remaining words are
        prefered because information about those letters will tend to elmininate more words.
        Uniqueness: Words with 5 unique letters tend to give more information than those with repeat letters.
    :param algstate: The state of the algorithm.
    :return: A dictionary of word:score containing the three highest scoring words.
    """
    freq = letter_frequency(algstate.pool)
    uniq_scores = uniques(algstate.pool)
    freq_scores = frequency_scores(algstate.pool, freq)
    # combine the scores
    combined = {}
    for word in algstate.pool:
        combined[word] = uniq_scores[word] + .5 * freq_scores[word]
    largest = nlargest(3, combined, key=combined.get)
    ldict = {}
    for maxx in largest:
        ldict[maxx] = combined[maxx]
    return ldict
