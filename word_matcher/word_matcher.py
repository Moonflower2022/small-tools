import curses
import english_words

def get_last_space_index(input):
    for i, char in enumerate(input[::-1]):
        if char == " " or char == "\t":
            return len(input) - i - 1
    return False

def value_function(word):
    return -len(word)

def get_output(input, word_list):
    last_space_index = get_last_space_index(input)
    if last_space_index:
        last_word = input[(last_space_index + 1):]
    else:
        last_word = input
    if last_word == "":
        return False
    good_words = [word for word in word_list if last_word == word[:len(last_word)]]
    if not good_words:
        return False
    return sorted(good_words, key=value_function, reverse=True)[0], len(last_word)

def main(stdscr):
    with open("word_matcher/1000_words.txt", "r") as file:
        raw_text = file.read()
    word_list = raw_text.split("\n")

    stdscr.clear()  # Clear the screen

    # Initial message
    prompt = "Start typing a word: "
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()

    user_input = ""
    output = None
    while True:

        key = stdscr.getch()
        if key == 27:  # ESC key to exit
            break
        elif key in (curses.KEY_BACKSPACE, 127):
            user_input = user_input[:-1]
        elif key in (curses.KEY_ENTER, 10):
            break
        elif key == ord("\t"):
            if output:
                user_input += output[0][output[1]:] + " "
                output = None
            else:
                user_input += "\t"
        else:
            user_input += chr(key)
        
        output = get_output(user_input, word_list)
        # Clear only the lines we are using
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, prompt + user_input)
        stdscr.move(1, 0)
        stdscr.clrtoeol()

        if output:
            output_string = f"Did you mean: {output[0]} (tab to autocomplete)"
        else:
            output_string = "Type some characters"
        stdscr.addstr(1, 0, output_string)
        stdscr.refresh()
        stdscr.move(0, len(prompt) + len(user_input))

curses.wrapper(main)