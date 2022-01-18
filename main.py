def load_words():
    with open('words_alpha.txt.txt') as word_file:
        word_set = set(word_file.read().split())
    valid_words = [val for val in word_set if len(val) == 5]
    return valid_words


def correct_check(val, crrct):
    for i in range(0, 5):
        if crrct[i] != "0" and val[i] != crrct[i]:
            return False
    return True


def contain_char(val, bl):
    for char in bl:
        if char in val:
            return True
    return False


def uniqueness_score(wordin):
    score = 5
    letters = {}
    for i in range(0, 5):
        if wordin[i] in letters.keys():
            letters[wordin[i]] += 1
            score -= 1
        else:
            letters[wordin[i]] = 1
    return score


def get_unique(wordlist):
    values = {}
    for i in wordlist:
        values[i] = uniqueness_score(i)
    tmp = 0
    maxstr = ""
    for i in values:
        if values[i] > tmp:
            tmp = values[i]
            maxstr = i
    return maxstr


def lst_refine(wordin, lst, bl, yllw, crrct):
    for i in range(0, 5):
        if wordle[i] == "b":
            bl.append(wordin[i])
        elif wordle[i] == "y":
            yllw.append(wordin[i])
        else:
            crrct[i] = wordin[i]
    possiblewords = [val for val in lst if
                     not contain_char(val, bl) and contain_char(val, yllw) and correct_check(val, crrct)]
    # allcorrectletters = [val for val in noblacklist if contain_char(val, yllw)]
    # possiblewords = [val for val in allcorrectletters if correct_check(val, crrct)]
    return {
        "blacklist": bl,
        "yellow": yllw,
        "correct": crrct,
        "lst": possiblewords,
    }


if __name__ == '__main__':
    print("Welcome to ruuffian's wordle solver!")
    print("What word did you start with? I suggest something with lots of vowels, like audio or adieu.")
    usrin = input()
    print("What was the wordle output?")
    wordle = input()
    english_words = load_words()
    blacklist = []
    yellow = []
    correct = ["0", "0", "0", "0", "0"]
    masterlst = lst_refine(usrin, english_words, blacklist, yellow, correct)
    count = 1
    unique = get_unique(masterlst["lst"])
    print("Try " + unique)
    while len(masterlst["lst"]) > 0 and count <= 6:
        print("What was the wordle output?")
        wordle = input()
        if "y" not in wordle and "b" not in wordle:
            print("Congratulations! We got the answer in " + str(count) + " tries!!")
            break
        masterlst = lst_refine(unique, masterlst["lst"], masterlst["blacklist"], masterlst["yellow"], masterlst["correct"])
        count += 1
        unique = get_unique(masterlst["lst"])
        print("Try " + unique)
    print("Thank you for using ruuffian's wordle solver. I hope it worked out!")
