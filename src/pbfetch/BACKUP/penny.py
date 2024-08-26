import re

current_loading_spinner = "/"


def replaceKeyword(template, keyword, replaceText):
    # Replace the text with a loading spinner
    if replaceText == "":
        replaceText = current_loading_spinner

    # Split the string on the word
    splitTemplate = template.split(keyword, 1)

    # Make sure the string was actually split
    if len(splitTemplate) == 1:
        return template

    # Measure the length of the second element in the split
    beforeStripLength = len(splitTemplate[1])

    # Remove the whitespace of the second element in the split
    splitTemplate[1] = splitTemplate[1].lstrip()

    # Measure the length after stripping :3 to figure out how
    #   many whitespaces we removed
    afterStripLength = len(splitTemplate[1])

    # Use those values to calculate the whitespaces
    whitespaceCount = beforeStripLength - afterStripLength
    # Figure out the max length the replacement can be
    keywordLength = len(keyword)
    maxAllowedLength = keywordLength + whitespaceCount
    # Store the length of what we are using to replace it
    replaceTextLength = len(replaceText)

    # Make sure our replaceText isn't too long
    if replaceTextLength > maxAllowedLength:
        replaceText = replaceText[:maxAllowedLength]

    # Pad replaceText with spaces to match the whitespace we removed
    replaceText = replaceText.ljust(maxAllowedLength, " ")

    return splitTemplate[0] + replaceText + splitTemplate[1]


def split_at_length(text, max_length):
    START_FLAG = "<"
    END_FLAG = ">"
    KEYWORD_REGEX = "blah"

    COMMAND_PATTERNS = [
        re.compile(
            r"RGB\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
        ),
        re.compile(r"RST"),
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
            if re.fullmatch(COMMAND_PATTERNS[0], buffer, flags=0) or re.fullmatch(
                COMMAND_PATTERNS[1], buffer, flags=0
            ):
                print(buffer)
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


def replaceDictionary(template, dictionary, max_line_length):
    # Replace all of the keywords in the dictionary
    for k, v in dictionary.items():
        if v == "":
            # do penny :3
            v = "LOADING..."
        template = replaceKeyword(template, k, v)

    # Make sure each line does not exceed max_line_length
    lines = template.splitlines()

    for i in range(0, len(lines)):
        lines[i] = split_at_length(lines[i], max_line_length)

    return "\n".join(lines)


print(
    replaceDictionary(
        """
$RGB(091,206,250)                               $RST $RGB(255,255,255) ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓$RST
$RGB(091,206,250) ⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⢀⠀⠀⠀⢠⠀⠀⠀⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿$RST $RGB(255,255,255) ┃ Software:                   ┃ $HOST              ┃$RST $RGB(213,045,000)⣿⣿⣿⢸⣿⣿⡏⢰⣿⣿⣿⡟⢠⣜⡛⣛⣡⣿⣿⣿⡏⢠⣄⠀⠻⠀⣿⣿⣿⣿⣿$RST
$RGB(091,206,250) ⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠰⡄⠀⣃⣠⣤⣬⣆⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿$RST $RGB(255,255,255) ┃ • OS: $SYS                  ┃ a really good girl ┃$RST $RGB(213,045,000)⣿⣿⡇⣼⣿⡟⠀⣾⣿⡿⠋⣰⣿⣿⠀⣿⣿⣿⣿⣿⢇⠸⢿⡿⠆⡀⢻⣿⣿⣿⣿$RST
$RGB(245,169,184) ⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿$RST $RGB(255,255,255) ┃ • Uptime: $UP               ┗━━━━━━━━━━━━━━━━━━━━┫$RST $RGB(255,154,086)⣿⣿⡇⢿⠟⠰⠇⠛⠋⣤⣚⣛⣛⣿⠀⣿⣿⣿⣿⢏⣼⣿⣶⣶⣿⣇⠸⣿⣿⣿⣿$RST
$RGB(245,169,184) ⣿⣿⣿⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⣠⣀⠀⠀⠈⣿⣿$RST $RGB(255,255,255) ┃ • Packages: $PAC                                 ┃$RST $RGB(255,154,086)⣿⣿⡇⣈⣴⠆⠀⠀⠀⠀⠀⠀⣬⣿⡆⢻⣿⣿⢏⣼⣿⢿⣟⡿⣿⣿⡄⢿⣿⡿⣿$RST
$RGB(255,255,255) ⣿⣿⡏⠀⡴⢄⠀⠀⢠⣾⣿⣿⠿⠿⠿⣿⣿⣦⣽⣼⣀⣜⣠⣿⣿⣴⡄⠀⣽⣿$RST $RGB(255,255,255) ┃ • Kernel: $KER                                   ┃$RST $RGB(255,255,255)⣿⣿⡇⣿⣿⡄⣤⣄⠛⣀⣘⢿⣿⣿⡏⢚⣩⣵⣾⣿⣿⡆⠈⠉⠛⠻⠷⠈⣿⡇⣿$RST
$RGB(255,255,255) ⣿⣿⡇⠠⢰⠆⢢⣤⣼⣿⣿⣧⣶⣶⡖⠀⠀⠀⢈⣿⣿⣯⣭⣭⠉⠉⠁⠀⣿⣿$RST $RGB(255,255,255) ┃                                                  ┃$RST $RGB(255,255,255)⠘⣿⣧⢹⣿⣷⣬⣛⣛⣛⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣀⢠⡄⢀⣀⣄⠹⢀⣿$RST
$RGB(255,255,255) ⣿⣿⡇⠠⡀⢺⠸⢿⣿⣿⣿⣿⣿⣿⣥⣤⣤⣴⣿⣿⣿⣿⣿⣛⣀⣀⡀⣰⣿⣿$RST $RGB(255,255,255) ┃ Hardware:                                        ┃$RST $RGB(255,255,255)⡇⣌⠻⡎⣷⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⡻⢦⣴⡾⣻⣿⡆⣸⣿$RST
$RGB(245,169,184) ⣿⣿⡇⠀⠈⠣⠴⡾⢻⣿⣿⣿⣿⣿⣿⣟⠻⠿⠿⠛⠿⠿⢛⣿⣿⣿⠇⣿⣿⣿$RST $RGB(255,255,255) ┃ • CPU: $CPU                                      ┃$RST $RGB(211,098,164)⡇⣿⣷⣮⣽⣿⣿⡟⣋⣤⡘⣿⣿⣿⣿⣿⣩⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⡿⢀⠏⣿$RST
$RGB(245,169,184) ⣿⣿⡇⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⣿⣮⣛⣫⣵⣾⣿⣿⠿⠋⢠⣿⣿⣿$RST $RGB(255,255,255) ┃ • RAM: $MEM                 ┏━━━━━━━━━━━━━━━━━━━━┫$RST $RGB(211,098,164)⡇⠹⣿⣿⣿⣿⣿⢰⣿⣿⣷⣌⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⡹⢁⢠⣾⣿$RST
$RGB(091,206,250) ⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⡀⢰⣶⣿⣿⣟⠛⠛⠛⠛⠛⠋⠉⠀⠀⠀⢸⣿⣿⣿$RST $RGB(255,255,255) ┃ • Disk: $DISK               ┃ CPU Usage: $PT     ┃$RST $RGB(163,002,098)⡀⡀⠈⠻⣿⣿⣿⡎⢿⣿⣿⣿⣿⣶⣭⣍⣛⡛⢻⣿⣿⣿⣿⣿⣿⣾⣿⡿⣸⣿⣿$RST
$RGB(091,206,250) ⣿⣿⠀⠀⠀⠀⠀⠀⢀⢸⣿⣦⣝⠻⡿⣡⣄⠀⠀⠀⠀⠀⠀⢐⠀⠀⢸⣿⣿⣿$RST $RGB(255,255,255) ┃ • Arch: $ARCH               ┃ CPU Temp: $TEM     ┃$RST $RGB(163,002,098)⠀⣷⣿⣷⣦⣙⠻⢿⣮⣛⠿⣿⣿⣿⣿⣿⣿⢏⣾⣿⣿⣿⣿⣿⣿⠿⣋⢱⣿⡏⣿$RST
$RGB(091,206,250)                               $RST $RGB(255,255,255) ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛$RST
""",
        {
            "$SYS": "value too looooong",
            "$UP": "peep",
            "$PAC": "My Pac",
            "$KER": "My Ker",
            "$CPU": "My CPU",
            "$MEM": "",
            "$DISK": "",
            "$ARCH": "",
        },
        100,
    )
)
# print(replaceKeyword("This is a bit of TEXT       doot", "TEXT", "delicious apple pie"))
# print(replaceKeyword("This is a bit of NOPE       doot", "TEXT", "delicious apple pie"))


s1 = "00000000<RST>000000<o.o>000000<RGB(5,255,255)>000000000000000<RST>00000000000000000000000000000000000<RGB(255,255,255)>000000000000000<RST>0000000<RGB(255,255,255)>00"
s2 = "00000000<<RST>>000000000000<<RGB(5,255,255)>>000000000000000<<RST>>00000000000000000000000000000000000<<RGB(255,255,255)>>000000000000000<<RST>>0000000<<RGB(255,255,255)>>00"

# s2 = ' ⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⢀⠀⠀⠀⢠⠀⠀⠀⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿  ┃ Software:                   ┃ $HOST              ┃ ⣿⣿⣿⢸⣿⣿⡏⢰⣿⣿⣿⡟⢠⣜⡛⣛⣡⣿⣿⣿⡏⢠⣄⠀⠻⠀⣿⣿⣿⣿⣿'


# s = '$RGB(091,206,250) ⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⢀⠀⠀⠀⢠⠀⠀⠀⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿$RST $RGB(255,255,255) ┃ Software:                   ┃ $HOST              ┃$RST $RGB(213,045,000)⣿⣿⣿⢸⣿⣿⡏⢰⣿⣿⣿⡟⢠⣜⡛⣛⣡⣿⣿⣿⡏⢠⣄⠀⠻⠀⣿⣿⣿⣿⣿$RST'

# print(re.sub('[a-z]+@', 'ABC@', s))
print(split_at_length(s2, 80))
