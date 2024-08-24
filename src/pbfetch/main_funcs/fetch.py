import re
import pbfetch.main_funcs.horizontal_formatter as hf
import pbfetch.main_funcs.stats as stats
from subprocess import Popen, PIPE

current_loading_spinner = "/"


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


console_width = get_console_width()


def fetch(fetch_data):
    stats_dict = stats.stats(fetch_data)
    system = stats_dict["$system"]

    if system.lower() != "linux":
        print("This fetch is currently only supported on linux, sorry!")
        exit()
    # omit comments from output
    for line in fetch_data.split("\n"):
        # catch and release comments using # notation
        regex_match = re.search("#.*$", line)
        if not regex_match:
            continue
        fetch_data = fetch_data.replace(regex_match.group(), "")

    fetch_data = hf.replace_keywords(fetch_data, stats_dict)

    # finally print fetch to terminal, format only from the right
    return fetch_data.rstrip()
