from pbfetch.main_funcs.stats import get_config_dir, stats

import os
from shutil import copy

# from pbfetch.main_funcs.stats import system

user = os.environ["USER"]


file = "config.txt"
usr_tmp = os.path.join("/", "usr", "share", "pbfetch", "config")
config_directory = get_config_dir()


def handle_config():
    # copy a default config into ~/.config/pbfetch/config/ on first launch
    if os.path.isdir(config_directory):
        if os.path.exists(os.path.join(config_directory, file)) is not True:
            print("Generating default config")
            copy(
                os.path.join(usr_tmp, file),
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
        with open(str(os.path.join(usr_tmp, file))) as usr_share_file:
            content = usr_share_file.read()

            if content:
                os.makedirs(config_directory)
                copy(
                    os.path.join(usr_tmp, file),
                    os.path.join(config_directory, file),
                )
                fetch_data = content
                print("Default config copied successfully")
            else:
                print("The default config is empty...Uh Oh!")
                exit()

    return fetch_data
