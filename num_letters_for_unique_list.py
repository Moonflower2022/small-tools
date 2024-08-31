words = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]
# ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def abbreviations_different(words, num_letters):
    abbreviated_words = [word[:num_letters] for word in words]
    for abbreviated_word in abbreviated_words:
        if abbreviated_words.count(abbreviated_word) > 1:
            return False
    return True


if __name__ == "__main__":
    for num_letters in range(1, max(len(word) for word in words) + 1):
        if abbreviations_different(words, num_letters):
            print(num_letters)
            break
