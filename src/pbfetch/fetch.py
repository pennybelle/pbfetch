from re import search
from platform import system as p_system

from pbfetch.horizontal_formatter import replace_keywords
from pbfetch.stats import stats
from pbfetch.constants import PLUG

# current_loading_spinner = "/"


# omit comments from output
def omit_comments(fetch_data, regex):
    for line in fetch_data.split("\n"):
        match = search(regex, line)
        if match:
            match = match.group()
            fetch_data = fetch_data.replace(match, " " * len(match))

    return fetch_data


def fetch(data):
    supported_systems = ["linux"]

    # check system name
    system = p_system()

    # exit if system is not supported
    if system.lower() not in supported_systems:
        print("This fetch is currently only supported on linux, sorry!")
        print("Want your system to be supported? Consider raising an issue")
        print("on https://github.com/pennybelle/pbfetch/issues")
        print("or consider contributing to the project!")
        exit()

    fetch_data, is_default = data

    # handle inline comments
    fetch_data = omit_comments(fetch_data, r"<comment>.*?<\/comment>")

    # handle end-of-line comments
    fetch_data = omit_comments(fetch_data, r"<comment>.*$")

    # strip whitespace only from the right
    fetch_data = fetch_data.rstrip()

    # debug
    # print(fetch_data)

    # init stats dictionary
    stats_dict = stats(fetch_data)

    # replace each keyword with respective stat (and format accordingly)
    fetch_data = replace_keywords(fetch_data, stats_dict)

    if is_default:
        plug = replace_keywords(PLUG, stats_dict)
        fetch_data = fetch_data + plug

    # send finalized output back to pbfetch.__init__.main
    return fetch_data
