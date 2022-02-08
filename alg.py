"""
Author: ruuffian
Name: alg.py
Description:
    This is the python file containing all of the methods used to analyze the wordpool and pick the best guess.
"""

from collections import defaultdict
from heapq import nlargest


class WordList:
    master: list[str]
    blacklist: list[str]
    yellowlist: list[list]
    greenlist: list[str]

    def __init__(self):
        self.master = []
        self.blacklist = []
        self.yellowlist = [[], [], [], [], []]
        self.greenlist = ["0", "0", "0", "0", "0"]

    def update_lists(self, bl, yl, gl):
        self.blacklist.extend(bl)
        self.yellowlist = yl
        self.greenlist = gl

    def refine_list(self, mst):
        self.master = mst


# Default value for my defualt dictionary
def def_value() -> int:
    return 0


# Initializes words from text file, in this case all of Wordle's valid answers
def load_words() -> list:
    """
    Initializes the wordpool with all of Wordles valid answers, stored in a text file
    :return: List of words pulled from text file
    """
    with open('resources/valid.txt') as word_file:
        word_set = set(word_file.read().split())
        valid_lst = []
        for val in word_set:
            valid_lst.append(val.strip(','))
    with open('resources/answers.txt') as word_file:
        word_set = set(word_file.read().split())
        for val in word_set:
            valid_lst.append(val.strip(','))
    return valid_lst


def norm_score(low: int, high: int, score: int) -> float:
    """
    Normalizes the scores being calculated so that they can be weighted properly
    :param low: Min value in the list
    :param high: Max val in the list
    :param score: The score being normalized
    :return: int -score between 0 and 1, rounded to two decimals
    """
    if high - low != 0:
        return round((score - low) / (high - low), 2)
    else:
        return 0


def normalization(scores: dict) -> dict:
    low = 1000
    high = 0
    normalized = {}
    for word in scores:
        if scores[word] < low:
            low = scores[word]
        if scores[word] > high:
            high = scores[word]
    for key in scores:
        normalized[key] = norm_score(low, high, scores[key])
    return normalized


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


def uniques(master: WordList) -> defaultdict:
    """
    Creates and returns a defaultdict of every word's uniqueness score
    Used to normalize the scores
    :param master: master WordList, essentially the entire game state
    :return: defaultdict -holds uniqueness scores keyed to the words, as well as a min and max value
    """
    uscores = defaultdict(def_value)
    for word in master.master:
        uscores[word] = uniqueness_score(word)
    return uscores


def letter_frequency(master: WordList) -> defaultdict:
    """
    Creates a defaultdict of values that are each letter frequency scores
    More occurences means a higher frequency
    :param master: The master WordList, essentially the gamestate
    :return: defaultdict -a dictionary containing all the letter frequency scores
    """
    freq = defaultdict(def_value)
    for word in master.master:
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


def frequencies(master: WordList, freq: defaultdict) -> defaultdict:
    """
    Creates a defaultdict holding every frequency score keyed to the word
    Used to normalize the scores
    :param master: master WordList, essentially the gamestate
    :param freq: frequency dictionary for the wordpool
    :return: defaultdict -holds frequency scores for the words, as well as a min and max value
    """
    fscores = defaultdict(def_value)
    for word in master.master:
        fscores[word] = frequency_score(word, freq)
    return fscores


def pick(master: WordList) -> dict:
    """
    Gives each word in the wordpool a score based on its letter frequency and the number of unique letters,
    then returns the one with the highest score
    Unique letters are preferred because they are easier to implement than doing some sort of DFS alg to
    create an optimal tree
    Frequent letters are preferred because they also elminate more words
    :param master: The master WordList, essentially the game state
    :return: dict -the 5 words with the highest calculated score
    """
    freq = letter_frequency(master)
    uscores = uniques(master)
    fscores = frequencies(master, freq)
    # normalize the characteristic scores
    norm_uscores = normalization(uscores)
    norm_fscores = normalization(fscores)
    # combine the scores
    nnorm_combine = {}
    for nscore in norm_uscores:
        nnorm_combine[nscore] = norm_uscores[nscore] + .5*norm_fscores[nscore]
    final_norm_scores = normalization(nnorm_combine)
    scores = {}
    # We want to weigh the uniqueness score more heavily than the frequency
    for word in master.master:
        scores[word] = final_norm_scores[word]
    largest = nlargest(5, scores, key=scores.get)
    ldict = {}
    for maxx in largest:
        ldict[maxx] = scores[maxx]
    return ldict
