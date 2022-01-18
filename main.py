def load_words():
    with open('words_alpha.txt') as word_file:
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


# make n-time with hashmap
def uniqueness_score(wordin):
    score = 5
    for i in range(0, 5):
        for j in range(1, 5):
            if i != j and i < j and wordin[i] == wordin[j]:
                score -= 1
    return score


def get_unique(wordlist):
    values = {}
    for i in wordlist:
        values[i] = uniqueness_score(i)
    tmp = 0
    unique = ""
    for i in values:
        if values[i] > tmp:
            tmp = values[i]
            unique = i
    return unique


def lst_refine(lst, wordin, result, bl, yllw, crrct):
    for i in range(0, 5):
        if result[i] == "b":
            bl.append(wordin[i])
        elif result[i] == "y":
            yllw.append(wordin[i])
        else:
            crrct[i] = wordin[i]
    noblacklist = [val for val in lst if not contain_char(val, bl)]
    allcorrectletters = [val for val in noblacklist if contain_char(val, yllw)]
    possiblewords = [val for val in allcorrectletters if correct_check(val, crrct)]
    return {
        "blacklist": bl,
        "yellow": yllw,
        "correct": crrct,
        "lst": possiblewords,
    }


if __name__ == '__main__':
    print("Welcome to ruuffian's wordle solver!")
    print("To start, try audio.")
    word = "audio"
    print("What was the wordle output?")
    wordle = input()
    english_words = load_words()
    blacklist = []
    yellow = []
    correct = ["0", "0", "0", "0", "0"]
    masterlst = lst_refine(english_words, word, wordle, blacklist, yellow, correct)
    count = 1
    word = get_unique(masterlst["lst"])
    print("Try " + word)
    while len(masterlst["lst"]) != 1 and count <= 6:
        print("What was the wordle output?")
        wordle = input()
        if "y" not in wordle and "b" not in wordle:
            print("Congratulations! We got the answer in " + str(count) + " tries!!")
            break
        masterlst = lst_refine(masterlst["lst"], word, wordle, masterlst["blacklist"],
                               masterlst["yellow"], masterlst["correct"])
        count += 1
        word = get_unique(masterlst["lst"])
        print("Try " + get_unique(masterlst["lst"]))
    print("Thank you for using ruuffian's wordle solver. I hope it worked out!")
