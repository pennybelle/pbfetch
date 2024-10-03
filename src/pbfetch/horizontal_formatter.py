from re import sub, fullmatch, compile
from subprocess import Popen, PIPE

from pbfetch.constants import RGB_START, RGB_END, FINAL_RGB_START, COLOR_RESET

# current_loading_spinner = "/"


def get_console_width():
    # gather raw output from console
    console_width = Popen(["stty", "size"], stdout=PIPE)

    # format raw data into int
    console_width = int(
        str(console_width.communicate()[0])
        .replace("b'", "")
        .replace(r"\n", "")
        .replace("'", "")
        .split()[1]
        .strip()
    )

    return console_width


console_width = get_console_width()


# TODO: WIP stretch feature
# def stretch(template, keyword):
#     template = template.splitlines()
#     replaced_template = []

#     for line in template:
#         if keyword not in line:
#             replaced_template.append(line)
#             continue


def replace_keyword(template, keyword, stat):
    template = template.splitlines()
    replaced_template = []

    for line in template:
        line = "<rgb(255,255,255)></rgb>" + line

        # if no keyword add line to replace template and continue
        if keyword not in line:
            replaced_template.append(line.rstrip())
            continue

        is_error = False

        # Store the length of what we are using to replace it
        stat_len = len(stat)

        if stat == "ERROR":
            is_error = True
            stat = "<rgb(255,0,0)>ERROR</rgb>"

        # Split the string on the word
        split_line = line.split(keyword)

        split_line[1] = split_line[1].ljust(stat_len)

        # Measure the length of the second element in the split
        before_strip_length = len(split_line[1])

        # Remove the whitespace of the second element in the split
        split_line[1] = split_line[1].lstrip()

        # Measure the length after stripping to figure out how
        #   many whitespaces we removed
        after_strip_length = len(split_line[1])

        # Use those values to calculate the whitespaces
        whitespace_count = before_strip_length - after_strip_length

        # Figure out the max length the replacement can be
        keyword_length = len(keyword)
        max_allowed_length = keyword_length + whitespace_count

        # handle error color tags conflicting with formatting
        if is_error:
            max_allowed_length += 20

        # Make sure our replaceText isn't too long
        stat = stat.ljust(max_allowed_length, " ")

        if stat_len > max_allowed_length:
            stat = stat[:max_allowed_length]

        # Pad replaceText wr"\/rgb"ith spaces to match the whitespace we removed
        # insert color reset bytecode at the beginning of each line
        # to prevent buggy behavior
        replaced_template.append(split_line[0] + stat + split_line[1].rstrip())

    template = "\n".join(replaced_template)

    return template


def split_at_length(line):
    START_FLAG = "<"
    END_FLAG = ">"

    COMMAND_PATTERNS = [
        compile(RGB_START),
        compile(RGB_END),
    ]

    current_count = 0
    skip_count = 0
    return_buffer = ""
    line_length = len(line)

    # Loop through each character in the string one at a time
    for i in range(0, line_length):
        # Capture the current character we are looking at
        current_char = line[i]

        # Add that current character to our return buffer
        return_buffer += current_char

        # Allow for us to skip parts of the text
        if skip_count > 0:
            skip_count -= 1
            continue

        # TODO: add here a conditional that checks if the last
        #   few characters in the string match a keyword, if so
        #   then add the stat value to the buffer and return buffer

        # If the current character is the starting flag we need to check
        #   if the following character are a command
        if current_char == START_FLAG:
            # Create a buffer to push the next characters to
            buffer = ""

            # Loop through the string from the current location to
            #   the next END_FLAG capturing the characters as we go
            for j in range(1, line_length - i):
                # Capture the current character at this index
                buffer_char = line[i + j]

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
        if current_count >= console_width:
            break

    return return_buffer


def final_touches(return_text):
    return_text = sub(
        FINAL_RGB_START,
        COLOR_RESET,
        return_text,
    )
    return_text = str(sub(r"\<\/rgb\>", "[39m", return_text))

    return return_text


def replace_keywords(template, stats_dict):
    # Replace all of the keywords in the dictionary
    for keyword, stat in stats_dict.items():
        if stat is None:
            stat = "ERROR"

        template = replace_keyword(template, keyword, stat)

    # Make sure each line does not exceed max_line_length
    lines = template.splitlines()

    for i in range(0, len(lines)):
        lines[i] = split_at_length(lines[i])

    template = "\n".join(lines)
    return_text = final_touches(template)

    return return_text
