import re

# from subprocess import Popen, PIPE

import pbfetch.main_funcs.horizontal_formatter as hf
from pbfetch.main_funcs.stats import stats
from subprocess import Popen, PIPE

current_loading_spinner = "/"


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


console_width = get_console_width()

# from pbfetch.main_funcs.stats import system

stats_dict = stats()
system = stats_dict["$system"]

if system != "Linux":
    print("This fetch is currently only supported on linux, sorry!")
    exit()


"""/usr/share/pbfetch/config/"""


# # init stats using keywords for configuration in .conf
# file = os.path.join("src", "pbfetch", "config", "config.txt")


def fetch(fetch_data):
    # replaced_fetch_data = []

    # omit comments from output
    for line in fetch_data.split("\n"):
        # catch and release comments using # notation
        regex_match = re.search("#.*$", line)
        if not regex_match:
            continue
        fetch_data = fetch_data.replace(regex_match.group(), "")

        # # replace stat keywords with stat data
        # for keyword in stats_dict.keys():
        #     # associate stat keyword with its respective value
        #     stat = stats_dict[keyword]
        #     if stat is None:
        #         continue
        #     stat = str(stat)

        # format char differences for keyword and respective value

    # for line in fetch_data.splitlines():
    fetch_data = hf.replace_dictionary(fetch_data, stats_dict)

    # fetch_data = "\n".join(replaced_fetch_data)
    # fetch_data = hf.replace_dictionary(fetch_data, stats_dict)

    # # TODO: make this optional from the config.txt
    # # clear the terminal
    # os.system("cls" if os.name == "nt" else "clear")

    # finally print fetch to terminal, format only from the right
    return fetch_data.rstrip()
