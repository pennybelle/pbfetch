import re, os, shutil
from subprocess import Popen, PIPE

import pbfetch.main_funcs.horizontal_formatter as hf
from pbfetch.main_funcs.stats import stats

# from pbfetch.main_funcs.stats import system

stats_dict = stats()
system = stats_dict["$SYSTEM"]
user = stats_dict["$USER"]

if system != "Linux":
    print("This fetch is currently only supported on linux, sorry!")
    exit()


"""/usr/share/pbfetch/config/"""


file = "config.txt"
usr_share = os.path.join("/", "usr", "share", "pbfetch", "config")
config_directory = os.path.join("/", "home", user, ".config", "pbfetch", "config")


# # init stats using keywords for configuration in .conf
# file = os.path.join("src", "pbfetch", "config", "config.txt")


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


def fetch():
    # copy a default config into ~/.config/pbfetch/config/ on first launch
    if os.path.isdir(config_directory):
        if os.path.exists(os.path.join(config_directory, file)) is not True:
            print("Generating default config")
            shutil.copy(
                os.path.join(usr_share, file),
                os.path.join(config_directory, file),
            )
        with open(os.path.join(config_directory, file)) as fetch_data:
            content = fetch_data.read()

            if content:
                fetch_data = content
            else:
                print("The config is empty! Try adding some ascii art OwO")
                print(f"The config can be located in {config_directory}")
                exit()

    else:
        print(f"Generating new config in {config_directory}")
        with open(str(os.path.join(usr_share, file))) as usr_share_file:
            content = usr_share_file.read()

            if content:
                os.makedirs(config_directory)
                shutil.copy(
                    os.path.join(usr_share, file),
                    os.path.join(config_directory, file),
                )
                fetch_data = content
                print("Default config copied successfully")
            else:
                print("The default config is empty...Uh Oh!")
                exit()

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
    fetch_data = hf.replace_dictionary(fetch_data, stats_dict, get_console_width())

    # # TODO: make this optional from the config.txt
    # # clear the terminal
    # os.system("cls" if os.name == "nt" else "clear")

    # finally print fetch to terminal, format only from the right
    return fetch_data.rstrip()
