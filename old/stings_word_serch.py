triggers = ["work", "play", "eat", "cry", "sleep", "fight"]

txt = "Lets go and "


def trigger_check():
    for word in txt.split():
        for trigger in triggers:
            if trigger == word:
                return word


def find_keyword_x(string):
    keywords = ["work", "play", "eat", "cry", "sleep", "fight"]
    for word in string.split():
        if word in keywords:
            return word



def find_keyword(string): # Checks if a strings contains a keyword for bot respons

    keywords = ["work", "play", "eat", "cry", "sleep", "fight"]  # bot respons keywoeds


print(find_keyword_x(txt))
