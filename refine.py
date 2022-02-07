# This file contains all the functions used in refining the master wordlist after each successive guess

# Returns true if the word contains no blacklisted and also has all the yellow letters SOMEWHERE. see check_yellowlist_
# positions for checking the positions of yellow letters
def check_blacklist_and_yellowlist(curword, blck, yllw):
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


# This returns false if the word contains a yellow letter in a yellow position, and true otherwise
def check_yellow_positions(curword, yllw):
    i = 0
    for pos in yllw:
        if curword[i] in pos:
            return False
        i += 1
    return True


# This returns false if the word doesnt contain a green letter in the right position and false otherwise
def check_greenlist_positions(curword, grn):
    for i in range(5):
        if grn[i] != "0" and curword[i] != grn[i]:
            return False
    return True


def lst_refine(master):
    removechars = [lstword for lstword in master.master if
                   check_blacklist_and_yellowlist(lstword, master.blacklist, master.yellowlist)]
    yellowposchecked = [lstword for lstword in removechars if check_yellow_positions(lstword, master.yellowlist)]
    refined = [lstword for lstword in yellowposchecked if check_greenlist_positions(lstword, master.greenlist)]
    return refined
