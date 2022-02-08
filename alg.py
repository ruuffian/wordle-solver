from collections import defaultdict


# Default value for my defualt dictionary
def def_value():
    return 0


# Initializes words from text file, in this case all of Wordle's valid answers
def load_words():
    with open('resources/valid.txt') as word_file:
        word_set = set(word_file.read().split())
        valid_lst = []
        for val in word_set:
            valid_lst.append(val.strip(','))
    return valid_lst


# gives each score a uniqueness score based on how many unique letters it contains -faster implementation exists
def uniqueness_score(wordin):
    score = 5
    letters = defaultdict(def_value)
    for i in range(5):
        letters[wordin[i]] += 1
        score -= letters[wordin[i]] - 1
    return score


# Finds the letter frequency for the current word pool, regenerated every guess
def letter_frequency(master):
    freq = defaultdict(def_value)
    for word in master.master:
        for char in word:
            freq[char] += 1
    return freq


# gives a word a frequency score based on the frequency object of the word pool -more frequent letters = higher score
# can be improved
def frequency_score(word, freq):
    score = 0
    for char in word:
        score += freq[char]
    return score


# finds the best word based on our characteristics: letter frequency and unique letters
def get_frequent_unique(master):
    freq = letter_frequency(master)
    scores = {}
    for word in master.master:
        scores[word] = (uniqueness_score(word) ** 2) * frequency_score(word, freq)
    maxscr = 0
    maxstr = ""
    for key in scores:
        if scores[key] > maxscr:
            maxscr = scores[key]
            maxstr = key
    return maxstr


# picks a word to suggest to the user
def pick(master):
    unique = get_frequent_unique(master)
    return unique


# Data class used to store all the game information in one place
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
