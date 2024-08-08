from re import sub, fullmatch, compile
from subprocess import Popen, PIPE

current_loading_spinner = "/"


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


console_width = get_console_width()


def replace_keyword(template, keyword, replace_text):
    print(type(template))
    template = template.splitlines()
    replaced_template = []
    for line in template:
        # Replace the text with a loading spinner
        if keyword not in line:
            print("no keyword :c")
            replaced_template.append(line)
            continue

        # Store the length of what we are using to replace it
        replace_tex_length = len(replace_text)

        # template = template.ljust(console_width)

        # Split the string on the word
        split_line = line.split(keyword)
        # split_template = [*split_template]
        print(split_line)

        # if len(line) < console_width:
        split_line[1] = split_line[1].ljust(replace_tex_length)

        # # Make sure the string was actually split
        # if split_template[1] == "" and split_template[2] == "":
        #     return template

        # if (split_template[1] == keyword and split_template[2].isspace()) or (
        #     split_template[1] == keyword and split_template[2] == ""
        # ):
        #     print("doot")
        #     modified_line = split_template[2].ljust(
        #         len(split_template[0]) + len(replace_text) + len(split_template[2])
        #     )
        #     # print(modified_line)
        #     split_template[2] = modified_line

        # modified_line = split_template[2].ljust(
        #     console_width - (len(split_template[0]) - len(replace_text))
        # )
        # # print(modified_line)
        # split_template[2] = modified_line

        # split_template[2] = split_template[2].ljust(console_width)

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

        # min_allowed_length = console_width

        # print(
        #     len(template) - replace_tex_length - whitespace_count,
        #     min_allowed_length,
        #     whitespace_count,
        # )
        # if (len(template) - replace_tex_length - whitespace_count) < min_allowed_length:
        #     print("<")
        #     template = template.ljust(console_width * 2)

        # Make sure our replaceText isn't too long (THIS BITCH)
        replace_text = replace_text.ljust(max_allowed_length, " ")
        # template = split_template[0] + replace_text + split_template[1]

        if replace_tex_length > max_allowed_length:
            # print(">")
            replace_text = replace_text[:max_allowed_length]

        # Pad replaceText with spaces to match the whitespace we removed
        replaced_template.append(split_line[0] + replace_text + split_line[1])
        # replace_text = replace_text.ljust(console_width - len(replace_text), " ")

    template = "\n".join(replaced_template)

    return template  # i give up...


def split_at_length(line):
    # TODO: add a counter var that this function returns.
    #   the counter will keep track of how many
    #   characters it counts that are not printed in
    #   the final output.

    START_FLAG = "<"
    END_FLAG = ">"

    COMMAND_PATTERNS = [
        compile(
            r"rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
        ),
        compile(r"\/rgb"),
    ]

    current_count = 0
    skip_count = 0
    # tag_count = 0
    # tag_buffer = 0

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
            for j in range(1, line_length):
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
        r"<rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)\>",
        r"[38;2;\g<1>;\g<2>;\g<3>m",
        return_text,
    )
    return_text = str(sub(r"\<\/rgb\>", "[39m", return_text))

    return return_text


def replace_dictionary(template, dictionary):
    print(type(template))
    # Replace all of the keywords in the dictionary
    for k, v in dictionary.items():
        if v == "":
            v = "LOADING..."
        template = replace_keyword(template, k, v)

    # Make sure each line does not exceed max_line_length
    lines = template.splitlines()

    for i in range(0, len(lines)):
        lines[i] = split_at_length(lines[i])
        # lines[i] = lines[i].ljust(console_width)
        # print(sub(" ", "_", lines[i]))

    template = "\n".join(lines)
    return_text = final_touches(template)

    return return_text
