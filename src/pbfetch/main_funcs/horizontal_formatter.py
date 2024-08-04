from time import sleep
from os import system, name
from shutil import get_terminal_size
from re import sub, fullmatch, compile


# from pbfetch.constants import rgb_regex


# def replace_keyword(fetch_data, keyword, replace_text):
#     fetch_data = fetch_data.rstrip()

#     # # debug
#     # system("cls" if name == "nt" else "clear")
#     # print(fetch_data)
#     # sleep(0.1)

#     # split the string on keyword
#     split_fetch_data = fetch_data.split(keyword, 1)

#     # make sure string contains both halves
#     if len(split_fetch_data) == 1:
#         return fetch_data

#     # measure len of second element in split data
#     before_strip_len = len(split_fetch_data[1])

#     # remove whitespace of the second element in split data
#     split_fetch_data[1] = split_fetch_data[1].lstrip()

#     # measure len of second element after stripping whitespace chars
#     after_strip_len = len(split_fetch_data[1])

#     # calculate whitespace with before and after lens of second element
#     whitespace_count = before_strip_len - after_strip_len

#     # figure out relacement text max len
#     keyword_len = len(keyword)
#     max_allowed_len = keyword_len + whitespace_count

#     # store lens to replace text with desired len
#     replace_text_len = len(replace_text)

#     # make sure replace text isnt too long
#     if replace_text_len > max_allowed_len:
#         replace_text = replace_text[: max_allowed_len - 3]
#         replace_text = replace_text + "..."

#     # pad replace_text with spaces to match the removed whitespace
#     replace_text = replace_text.ljust(max_allowed_len, " ")

#     # stitch output back together with replace_text in place of keyword
#     return_text = split_fetch_data[0] + replace_text + split_fetch_data[1]

#     #############################

#     # check how many characters can fit in the row
#     terminal_width = Popen(["tput", "cols"], stdout=PIPE)
#     terminal_width = int(float(terminal_width.communicate()[0].strip()))
#     # print(terminal_width)  # debug

#     # temp list of lines without rgb to gather line len
#     omit_rgb = sub(
#         r"\$RGB\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)",
#         "",
#         return_text,
#     )
#     omit_rgb = sub(r"\$RST", "", omit_rgb)
#     omit_rgb = omit_rgb.splitlines()

#     # get length of longest line
#     longest_line_len = len(max(omit_rgb, key=len))

#     # cut off end of line if longer than console width
#     if longest_line_len <= terminal_width:
#         return final_touches(return_text)

#     # with rgb, these lines get sliced if too long
#     return_text = return_text.splitlines()

#     # iterate over lines without rgb to get real len of line
#     for index, line in enumerate(omit_rgb):
#         # skip line if its not too long
#         if len(line) <= terminal_width:
#             # print(line)  # debug
#             continue  # debug

#         # line to replace old line that's too long
#         new_line = line[: terminal_width - 3] + "..."

#         string[1:]
#         # print(f"new: {new_line}")  # debug

#         # if line is too long, replace the respective line content
#         # in return_text with the sliced line
#         # (i think this is the problem)
#         return_text[index] = return_text[index].replace(line, new_line)
#         print(return_text[index])  # debug

#     return_text = "\n".join(return_text)

#     return final_touches(return_text)

current_loading_spinner = "/"


def replace_keyword(template, keyword, replace_text):
    # Replace the text with a loading spinner
    if replace_text == "":
        replace_text = current_loading_spinner

    # Split the string on the word
    split_template = template.split(keyword, 1)

    # Make sure the string was actually split
    if len(split_template) == 1:
        return template

    # Measure the length of the second element in the split
    before_strip_length = len(split_template[1])

    # Remove the whitespace of the second element in the split
    split_template[1] = split_template[1].lstrip()

    # Measure the length after stripping :3 to figure out how
    #   many whitespaces we removed
    after_strip_length = len(split_template[1])

    # Use those values to calculate the whitespaces
    whitespace_count = before_strip_length - after_strip_length

    # Figure out the max length the replacement can be
    keyword_length = len(keyword)
    max_allowed_length = keyword_length + whitespace_count

    # Store the length of what we are using to replace it
    replace_tex_length = len(replace_text)

    # Make sure our replaceText isn't too long
    if replace_tex_length > max_allowed_length:
        replace_text = replace_text[:max_allowed_length]

    # Pad replaceText with spaces to match the whitespace we removed
    replace_text = replace_text.ljust(max_allowed_length, " ")

    return split_template[0] + replace_text + split_template[1]


def split_at_length(text, max_length):
    START_FLAG = "<"
    END_FLAG = ">"

    COMMAND_PATTERNS = [
        compile(
            r"RGB\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
        ),
        compile(r"RST"),
    ]

    current_count = 0
    skip_count = 0

    return_buffer = ""

    text_length = len(text)
    # Loop through each character in the string one at a time
    for i in range(0, text_length):
        # Capture the current character we are looking at
        current_char = text[i]

        # Add that current character to our return buffer
        return_buffer += current_char

        # Allow for us to skip parts of the text
        if skip_count > 0:
            skip_count -= 1
            continue

        # If the current character is the starting flag we need to check
        #   if the following character are a command
        if current_char == START_FLAG:
            # Create a buffer to push the next characters to
            buffer = ""

            # Loop through the string from the current location to
            #   the next END_FLAG capturing the characters as we go
            for j in range(1, text_length):
                # Capture the current character at this index
                buffer_char = text[i + j]

                # If the captured character is our end flag then stop
                if buffer_char == END_FLAG:
                    break

                # Add it to our buffer
                buffer += buffer_char

            # Check to see if buffer is a command
            if fullmatch(COMMAND_PATTERNS[0], buffer, flags=0) or fullmatch(
                COMMAND_PATTERNS[1], buffer, flags=0
            ):
                # print(buffer)  # debug
                # Skip the characters that exist in our command
                skip_count = len(buffer) + len(END_FLAG)
                # We KNOW this is a command tag and we don't want to count it, so
                #   continue out of this for loop cycle before the count
                continue

        # count
        current_count += 1

        # IF we have reached our max length, stop counting and return what we have
        if current_count >= max_length:
            break

    return return_buffer


def final_touches(return_text):
    return_text = sub(
        r"<RGB\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)\>",
        r"[38;2;\g<1>;\g<2>;\g<3>m",
        return_text,
    )
    return_text = str(sub(r"\<RST\>", "[39m", return_text))

    return return_text


def replace_dictionary(template, dictionary, max_line_length):
    # Replace all of the keywords in the dictionary
    for k, v in dictionary.items():
        if v == "":
            # do penny :3
            v = "LOADING..."
        template = replace_keyword(template, k, v)

    # Make sure each line does not exceed max_line_length
    lines = template.splitlines()

    for i in range(0, len(lines)):
        lines[i] = split_at_length(lines[i], max_line_length)

    # return final_touches("\n".join(lines))
    return_text = "\n".join(lines)
    return_text = final_touches(return_text)

    return return_text


# return_text = replace_dictionary(
#     """
# $RGB(091,206,250)                               $RST $RGB(255,255,255) ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓$RST
# $RGB(091,206,250) ⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⢀⠀⠀⠀⢠⠀⠀⠀⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿$RST $RGB(255,255,255) ┃ Software:                   ┃ $HOST              ┃$RST $RGB(213,045,000)⣿⣿⣿⢸⣿⣿⡏⢰⣿⣿⣿⡟⢠⣜⡛⣛⣡⣿⣿⣿⡏⢠⣄⠀⠻⠀⣿⣿⣿⣿⣿$RST
# $RGB(091,206,250) ⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠰⡄⠀⣃⣠⣤⣬⣆⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿$RST $RGB(255,255,255) ┃ • OS: $SYS                  ┃ a really good girl ┃$RST $RGB(213,045,000)⣿⣿⡇⣼⣿⡟⠀⣾⣿⡿⠋⣰⣿⣿⠀⣿⣿⣿⣿⣿⢇⠸⢿⡿⠆⡀⢻⣿⣿⣿⣿$RST
# $RGB(245,169,184) ⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿$RST $RGB(255,255,255) ┃ • Uptime: $UP               ┗━━━━━━━━━━━━━━━━━━━━┫$RST $RGB(255,154,086)⣿⣿⡇⢿⠟⠰⠇⠛⠋⣤⣚⣛⣛⣿⠀⣿⣿⣿⣿⢏⣼⣿⣶⣶⣿⣇⠸⣿⣿⣿⣿$RST
# $RGB(245,169,184) ⣿⣿⣿⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⣠⣀⠀⠀⠈⣿⣿$RST $RGB(255,255,255) ┃ • Packages: $PAC                                 ┃$RST $RGB(255,154,086)⣿⣿⡇⣈⣴⠆⠀⠀⠀⠀⠀⠀⣬⣿⡆⢻⣿⣿⢏⣼⣿⢿⣟⡿⣿⣿⡄⢿⣿⡿⣿$RST
# $RGB(255,255,255) ⣿⣿⡏⠀⡴⢄⠀⠀⢠⣾⣿⣿⠿⠿⠿⣿⣿⣦⣽⣼⣀⣜⣠⣿⣿⣴⡄⠀⣽⣿$RST $RGB(255,255,255) ┃ • Kernel: $KER                                   ┃$RST $RGB(255,255,255)⣿⣿⡇⣿⣿⡄⣤⣄⠛⣀⣘⢿⣿⣿⡏⢚⣩⣵⣾⣿⣿⡆⠈⠉⠛⠻⠷⠈⣿⡇⣿$RST
# $RGB(255,255,255) ⣿⣿⡇⠠⢰⠆⢢⣤⣼⣿⣿⣧⣶⣶⡖⠀⠀⠀⢈⣿⣿⣯⣭⣭⠉⠉⠁⠀⣿⣿$RST $RGB(255,255,255) ┃                                                  ┃$RST $RGB(255,255,255)⠘⣿⣧⢹⣿⣷⣬⣛⣛⣛⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣀⢠⡄⢀⣀⣄⠹⢀⣿$RST
# $RGB(255,255,255) ⣿⣿⡇⠠⡀⢺⠸⢿⣿⣿⣿⣿⣿⣿⣥⣤⣤⣴⣿⣿⣿⣿⣿⣛⣀⣀⡀⣰⣿⣿$RST $RGB(255,255,255) ┃ Hardware:                                        ┃$RST $RGB(255,255,255)⡇⣌⠻⡎⣷⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⡻⢦⣴⡾⣻⣿⡆⣸⣿$RST
# $RGB(245,169,184) ⣿⣿⡇⠀⠈⠣⠴⡾⢻⣿⣿⣿⣿⣿⣿⣟⠻⠿⠿⠛⠿⠿⢛⣿⣿⣿⠇⣿⣿⣿$RST $RGB(255,255,255) ┃ • CPU: $CPU                                      ┃$RST $RGB(211,098,164)⡇⣿⣷⣮⣽⣿⣿⡟⣋⣤⡘⣿⣿⣿⣿⣿⣩⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⡿⢀⠏⣿$RST
# $RGB(245,169,184) ⣿⣿⡇⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⣿⣮⣛⣫⣵⣾⣿⣿⠿⠋⢠⣿⣿⣿$RST $RGB(255,255,255) ┃ • RAM: $MEM                 ┏━━━━━━━━━━━━━━━━━━━━┫$RST $RGB(211,098,164)⡇⠹⣿⣿⣿⣿⣿⢰⣿⣿⣷⣌⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⡹⢁⢠⣾⣿$RST
# $RGB(091,206,250) ⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⡀⢰⣶⣿⣿⣟⠛⠛⠛⠛⠛⠋⠉⠀⠀⠀⢸⣿⣿⣿$RST $RGB(255,255,255) ┃ • Disk: $DISK               ┃ CPU Usage: $PT     ┃$RST $RGB(163,002,098)⡀⡀⠈⠻⣿⣿⣿⡎⢿⣿⣿⣿⣿⣶⣭⣍⣛⡛⢻⣿⣿⣿⣿⣿⣿⣾⣿⡿⣸⣿⣿$RST
# $RGB(091,206,250) ⣿⣿⠀⠀⠀⠀⠀⠀⢀⢸⣿⣦⣝⠻⡿⣡⣄⠀⠀⠀⠀⠀⠀⢐⠀⠀⢸⣿⣿⣿$RST $RGB(255,255,255) ┃ • Arch: $ARCH               ┃ CPU Temp: $TEM     ┃$RST $RGB(163,002,098)⠀⣷⣿⣷⣦⣙⠻⢿⣮⣛⠿⣿⣿⣿⣿⣿⣿⢏⣾⣿⣿⣿⣿⣿⣿⠿⣋⢱⣿⡏⣿$RST
# $RGB(091,206,250)                               $RST $RGB(255,255,255) ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛$RST
# """,
#     stats_dict,
#     get_console_width(),
# )


# return return_text
