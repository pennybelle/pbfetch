import re
import pbfetch.main_funcs.horizontal_formatter as hf
from pbfetch.main_funcs.stats import stats
from subprocess import Popen, PIPE
from platform import system as p_system

current_loading_spinner = "/"


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


console_width = get_console_width()


def fetch(fetch_data):
    system = p_system()

    if system.lower() != "linux":
        print("This fetch is currently only supported on linux, sorry!")
        exit()

    # omit comments from output
    for line in fetch_data.split("\n"):
        # catch and release comments using # notation
        inline_comment = re.search(r"<comment>.*?<\/comment>", line)
        if inline_comment:
            match = inline_comment.group()
            print("inline comment:", match)
            fetch_data = fetch_data.replace(match, " " * len(match))

    for line in fetch_data.split("\n"):
        rest_of_line_comment = re.search(r"<comment>.*$", line)
        if rest_of_line_comment:
            match = rest_of_line_comment.group()
            print("rest of line comment:", match)
            fetch_data = fetch_data.replace(match, " " * len(match))

    stats_dict = stats(fetch_data)
    fetch_data = hf.replace_keywords(fetch_data, stats_dict)

    # strip whitespace only from the right and reset colors at the end
    fetch_data = f"{fetch_data.rstrip()}[39m"

    # finally print fetch to terminal
    return fetch_data
