from collections import defaultdict


def def_value():
    return 0


def load_words():
    with open('valid.txt') as word_file:
        word_set = set(word_file.read().split())
        valid_lst = [val for val in word_set]
    return valid_lst


def correct_check(val, crrct):
    for i in range(5):
        if crrct[i] != "0" and val[i] != crrct[i]:
            return False
    return True


def contain_char(curword, lst):
    if len(lst) == 0:
        return True
    for char in lst:
        if char in curword:
            return True
    return False


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


def lst_refine(lst, bl, yllw, crrct):
    possiblewords = [lstword for lstword in lst if
                     not contain_char(lstword, bl) and contain_char(lstword, yllw) and correct_check(lstword,
                                                                                                     crrct)]
    return {
        "blacklist": bl,
        "yellowlist": yllw,
        "greenlist": crrct,
        "lst": possiblewords,
    }


def pick(masterlist):
    unique = get_frequent_unique(masterlist["lst"])
    return unique
