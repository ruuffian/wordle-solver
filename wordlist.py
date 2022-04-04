"""
Author: ruuffian
Name: wordlist.py
Description:
    Definition of WordleState object and related methods.
"""


class WordleState:
    """

    """
    pool: list[str]
    blacklist: list[str]
    yellowlist: list[list[str]]
    greenlist: list[str]

    def __init__(self):
        self.pool = []
        self.blacklist = []
        self.yellowlist = [[""]] * 5
        self.greenlist = ["0"] * 5

    def update_info(self, bl, yl, gl):
        self.blacklist.extend(bl)
        self.yellowlist = yl
        self.greenlist = gl

    def refine_list(self):
        self.pool = lst_refine(self)


# Initializes words from text file, in this case all of Wordle's valid answers
def load_words(flag: bool) -> list:
    """
    Initializes the wordpool with all of Wordles valid answers, stored in a text file
    :param flag: Boolean flag to enable or disable the full word pool
    :return: List of words pulled from text file
    """
    valid_lst = []
    if flag == 1:
        with open('resources/solutions.txt') as word_file:
            word_set = set(word_file.read().split())
            for val in word_set:
                valid_lst.append(val.strip(','))
    with open('resources/accepted.txt') as word_file:
        word_set = set(word_file.read().split())
        for val in word_set:
            valid_lst.append(val.strip(','))
    return valid_lst


def check_blacklist_and_yellowlist(curword: str, blck: list, yllw: list) -> bool:
    """
    Checks the current word against a list of blacklisted letters and an array of
    yellowlisted letters. It will reject any word that contains a blacklisted letter, and also
    any word that doesn't contain a yellowlisted letter. Checking the yellowlisted positions is
    delegated to a later function.
    :param curword: The current word from the wordpool
    :param blck: List of absent letters
    :param yllw: List of present letters and the positions they are NOT in
    :return: Bool -false if word contains blacklisted or doesnt contain yellowlisted letters, true otherwise
    """
    unique = []
    # This loop checks the blaclisted letters and removes words that contain them
    for char in blck:
        if char in curword:
            return False
    # This loop first checks that every yellowlisted character is present in the word
    for pos in yllw:
        for char in pos:
            if char not in curword:
                return False
            if char not in unique:
                unique.append(char)
    # This for loop ensures that every yellow character is contained
    for char in unique:
        if char not in curword:
            return False
    # Reaching this point implies that the word has every yellow character, no blacklisted characters
    return True


def check_yellow_positions(curword: str, yllw: list) -> bool:
    """
    Checks the positions of present letters to eliminate words that have previously guessed yellow letter
    positions
    :param curword: The currently word from the wordpool
    :param yllw: List of present words
    :return: Bool -False if word doesnt contain yellow letters, true otherwise
    """
    i = 0
    for pos in yllw:
        if curword[i] in pos:
            return False
        i += 1
    return True


def check_greenlist_positions(curword: str, grn: list) -> bool:
    """
    Checks the greenlist positions to ensure every word has a green letter in the correct positions
    :param curword: The current word from the word pool
    :param grn: Array representing the correct letters
    :return: Bool -false if the word does not contain green letters, true otherwise
    """
    for i in range(5):
        # Checks if a letter has been guessed and then if the word matches the correct guess
        if grn[i] != "0" and curword[i] != grn[i]:
            return False
    return True


def lst_refine(main: WordleState) -> list:
    """
    Uses a large list comprehension in order to trim the wordpool based on newly gathered information
    about the correct answer
    :param main: WordleState object containing all of the relevant gamestate information such as the blacklist,
    yellowlist, greenlist, and wordpool
    :return: List -Narrowed down wordpool
    """
    refined = [lstword for lstword in main.pool
               if check_blacklist_and_yellowlist(lstword, main.blacklist, main.yellowlist)
               and check_yellow_positions(lstword, main.yellowlist)
               and check_greenlist_positions(lstword, main.greenlist)]
    return refined
