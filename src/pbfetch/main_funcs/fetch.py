import re
from pbfetch.main_funcs.horizontal_formatter import replace_keywords
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
    supported_systems = [
        "linux"
    ]

    # check system name
    system = p_system()

    # exit if system is not supported
    if system.lower() not in supported_systems:
        print("This fetch is currently only supported on linux, sorry!")
        exit()

    # omit comments from output
    def omit_comments(fetch_data, regex):
        for line in fetch_data.split("\n"):
            match = re.search(regex, line)
            if match:
                match = match.group()
                fetch_data = fetch_data.replace(match, " " * len(match))
            
        return fetch_data

    # handle inline comments
    fetch_data = omit_comments(fetch_data, r"<comment>.*?<\/comment>")

    # handle end-of-line comments
    fetch_data = omit_comments(fetch_data, r"<comment>.*$")

    fetch_data = fetch_data.rstrip()

    # debug
    # print(fetch_data)

    # init stats dictionary
    stats_dict = stats(fetch_data)

    # replace each keyword with respective stat (and format accordingly)
    fetch_data = replace_keywords(fetch_data, stats_dict)

    # strip whitespace only from the right and reset colors at the end
    fetch_data = fetch_data.rstrip()

    # finally print fetch to terminal
    return fetch_data
