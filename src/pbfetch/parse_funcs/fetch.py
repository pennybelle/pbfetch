import re
import pbfetch.src.pbfetch.main_funcs.horizontal_formatter as hf
from pbfetch.src.pbfetch.main_funcs.stats import stats as get_stats

# init stats using keywords for configuration in .conf
stats = get_stats()


def fetch():
    # read config and exit if empty
    with open("config.txt", "r") as config:
        content = config.read()
        if content:
            fetch_data = content
        else:
            print("You must insert something in the config!")
            exit()

    # omit comments from output
    for line in fetch_data.split("\n"):
        # catch and release comments using # notation
        regex_match = re.search("#.*$", line)
        if not regex_match:
            continue
        fetch_data = fetch_data.replace(regex_match.group(), "")

    # replace stat keywords with stat data
    for keyword in stats.keys():
        # associate stat keyword with its respective value
        stat = stats[keyword]
        if stat is None:
            continue
        stat = str(stat)

        # format char differences for keyword and respective value
        fetch_data = hf.horizontal_formatter(fetch_data, keyword, stat)

    # finally print fetch to terminal, format only from the right
    return fetch_data.rstrip()
