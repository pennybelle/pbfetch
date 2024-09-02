from os import path, makedirs, environ

from pbfetch.constants import DEFAULT_CONFIG
from pbfetch.stats import get_config_dir

user = environ["USER"]
config_directory = get_config_dir()
file = "config.txt"


def handle_config():
    if path.isdir(config_directory) is not True:
        # make config directory
        makedirs(config_directory)

    if path.exists(path.join(config_directory, file)) is not True:
        print("Generating default config")

        # only import default config if needed

        # paste default config string into newly created config.txt
        with open(path.join(config_directory, file), "w") as config:
            # slice first newline in default config
            config.write(DEFAULT_CONFIG[1:])

    # read config
    with open(path.join(config_directory, file)) as config:
        content = config.read()

        if content:
            config = content

        else:
            print("The config is empty! Try adding some ascii art OwO")
            print(f"The config can be located in {config_directory}")
            exit()

    return config
