from collections import defaultdict


def def_value():
    return 0


def load_words():
    with open('valid.txt') as word_file:
        word_set = set(word_file.read().split())
        valid_lst = []
        for val in word_set:
            valid_lst.append(val.strip(','))
    return valid_lst


# Returns true if the word contains no blacklisted and also has all the yellow letters SOMEWHERE. see check_yellowlist_
# positions for checking the positions of yellow letters
def check_blacklist_and_yellowlist(curword, lst):
    troo = 0
    if len(lst) == 0:
        return True
    for char in lst:
        if char in curword:
            troo += 1
    return troo == len(lst)  # This bit of logic ensures all of the yellow letters appear in the word


# This returns false if the word contains a yellow letter in a yellow position, and true otherwise
def check_yellow_positions(curword, yllw):
    for pos in yllw:
        for i in range(5):
            if curword[i] in pos:
                return False
    return True


# This returns false if the word doesnt contain a green letter in the right position and false otherwise
def check_greenlist_positions(curword, grn):
    for i in range(5):
        if grn[i] != "0" and curword[i] != grn[i]:
            return False
    return True


def uniqueness_score(wordin):
    score = 5
    letters = defaultdict(def_value)
    for i in range(5):
        letters[wordin[i]] += 1
        score -= letters[wordin[i]] - 1
    return score


def letter_frequency(master):
    freq = defaultdict(def_value)
    for word in master.master:
        for char in word:
            freq[char] += 1
    return freq


def frequency_score(word, freq):
    score = 0
    for char in word:
        score += freq[char]
    return score


def get_frequent_unique(master):
    freq = letter_frequency(master.master)
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


def lst_refine(master):
    master.master = [lstword for lstword in master.master if
                     not check_blacklist_and_yellowlist(lstword, master.blacklist)
                     and check_yellow_positions(lstword, master.yellowlist)
                     and check_greenlist_positions(lstword, master.greenlist)]
    return master


def pick(master):
    unique = get_frequent_unique(master.master)
    return unique


class WordList:
    def __init__(self):
        self.master = []
        self.blacklist = []
        self.yellowlist = [[], [], [], [], []]
        self.greenlist = ["0", "0", "0", "0", "0"]

    def update_lists(self, mst, bl, yl, gl):
        self.master = mst
        self.blacklist.extend(bl)
        self.yellowlist = yl
        self.greenlist = gl
