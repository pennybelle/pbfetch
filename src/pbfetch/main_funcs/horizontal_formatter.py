from time import sleep
from os import system, name


def replace_keyword(fetch_data, keyword, replace_text):
    fetch_data = fetch_data.rstrip()

    # debug
    system("cls" if name == "nt" else "clear")
    print(fetch_data)
    sleep(0.3)

    # split the string on keyword
    split_fetch_data = fetch_data.split(keyword, 1)

    # make sure string contains both halves
    if len(split_fetch_data) == 1:
        return fetch_data

    # measure len of second element in split data
    before_strip_len = len(split_fetch_data[1])

    # remove whitespace of the second element in split data
    split_fetch_data[1] = split_fetch_data[1].lstrip()

    # measure len of second element after stripping whitespace chars
    after_strip_len = len(split_fetch_data[1])

    # calculate whitespace with before and after lens of second element
    whitespace_count = before_strip_len - after_strip_len

    # figure out relacement text max len
    keyword_len = len(keyword)
    max_allowed_len = keyword_len + whitespace_count

    # store lens to replace text with desired len
    replace_text_len = len(replace_text)

    # make sure replace text isnt too long
    if replace_text_len > max_allowed_len:
        replace_text = replace_text[: max_allowed_len - 3]
        replace_text = replace_text + "..."

    # pad replace_text with spaces to match the removed whitespace
    replace_text = replace_text.ljust(max_allowed_len, " ")

    return split_fetch_data[0] + replace_text + split_fetch_data[1]


# # format each line so right side accommodates for stat len
# def horizontal_formatter(fetch_data, key, stat):
#     print(f"before: \n{fetch_data.rstrip()}")
#     # split fetch string at each keyword (sequentially)
#     fetch_data = fetch_data.rstrip().split(str(key))

#     # store lengths for reuse
#     key_len = len(key)
#     stat_len = len(stat)
#     fetch_len = len(fetch_data)

#     if key_len < stat_len and fetch_len != 1:


#         # # number of chars to delete
#         # diff = stat_len - key_len

#         # # TODO: new algo:
#         # # fetch_data is a list split at the keyword (removes keyword)
#         # # diff is difference between len of keyword and stat
#         # # diff is how many whitespace chars are removed to the right
#         # # loop over chars in second string in fetchdata ([1])
#         # # keep a deletion_count of how many " " chars are deleted
#         # # if deletion_count = 0 and char is "\n" then print entire stat + "\n"
#         # # else if char is " " then delete char and add to deletion_count
#         # # else if char is not " " or "\n",
#         # # remove deletion_count from stat (from the right)
#         # # join fetch_data with stat

#         # # keep a whitespace_count of how many " " chars are deleted
#         # whitespace_count = 0

#         # # remove only whitespace chars following keyword
#         # for index in range(diff):
#         #     # line = fetch_data[1]
#         #     char = fetch_data[1][index]

#         #     # # debug
#         #     # print(fetch_data[0], end="", flush="")
#         #     # print(fetch_data[1].rstrip())
#         #     # sleep(0.025)
#         #     # system("cls" if name == "nt" else "clear")

#         #     # if char is "\n" then print entire stat + "\n"
#         #     if whitespace_count == 0 and char == "\n":
#         #         print("if")
#         #         stat = stat + "\n"
#         #         break

#         #     # WORKS!!!
#         #     # if char is " " then delete char and add to whitespace_count
#         #     elif char == " ":
#         #         print("elif")
#         #         modified = fetch_data[1][1:]  # slice off leftmost char
#         #         fetch_data[1] = modified
#         #         whitespace_count += 1

#         #     else:
#         #         print("else")
#         #         stat = stat[:whitespace_count]
#         #         break
#         #         # new_index = index + 1
#         #         # while new_index < diff and fetch_data[1][new_index] == " ":
#         #         #     modified = fetch_data[1].replace(fetch_data[1][index], "", 1)
#         #         #     # fetch_data[1] = modified

#         # print(whitespace_count)

#         # # # replaces second half with modified string
#         # # fetch_data[1] = modified

#     elif key_len > stat_len and fetch_len != 1:
#         # number of chars to add
#         diff = key_len - stat_len

#         # adds whitespace following keyword
#         modified = str(" " * diff) + fetch_data[1]

#         # replaces second half with modified string
#         fetch_data[1] = modified

#         # # rejoin into str and replace keyword with value
#         # fetch_data = str(stat).join(fetch_data)

#     # rejoin into str and replace keyword with value
#     fetch_data = str(stat).join(fetch_data)

#     print(f"after: \n{fetch_data}")

#     return fetch_data
