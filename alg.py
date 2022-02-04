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


def correct_check(curword, grn):
    for i in range(5):
        if grn[i] != "0" and curword[i] != grn[i]:
            return False
    return True


def contain_char(curword, lst):
    troo = 0
    if len(lst) == 0:
        return True
    for char in lst:
        if char in curword:
            troo += 1
    return troo == len(lst)  # This bit of logic ensures all of the yellow letters appear in the word


def uniqueness_score(wordin):
    score = 5
    letters = defaultdict(def_value)
    for i in range(5):
        letters[wordin[i]] += 1
        score -= letters[wordin[i]] - 1
    return score


def letter_frequency(lst):
    dnsty = defaultdict(def_value)
    for word in lst:
        for char in word:
            dnsty[char] += 1
    return dnsty


def frequency_score(word, frqncy):
    score = 0
    for char in word:
        score += frqncy[char]
    return score


def get_frequent_unique(wordlist):
    freq = letter_frequency(wordlist)
    scores = {}
    for i in wordlist:
        scores[i] = (uniqueness_score(i) ** 2) * frequency_score(i, freq)
    tmp = 0
    maxstr = ""
    for i in scores:
        if scores[i] > tmp:
            tmp = scores[i]
            maxstr = i
    return maxstr


def lst_refine(lst, black, yellow, green):
    possiblewords = [lstword for lstword in lst if
                     not contain_char(lstword, black)
                     and contain_char(lstword, yellow)
                     and correct_check(lstword, green)]
    return {
        "blacklist": black,
        "yellowlist": yellow,
        "greenlist": green,
        "lst": possiblewords,
    }


def pick(masterlist):
    unique = get_frequent_unique(masterlist["lst"])
    return unique
