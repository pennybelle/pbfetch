from os import path, makedirs, environ

from pbfetch.constants import DEFAULT_CONFIG
from pbfetch.stats import get_config_dir

user = environ["USER"]
config_directory = get_config_dir()
file = "config.txt"


def config():
    is_default = False

    # make config directory
    if path.isdir(config_directory) is not True:
        makedirs(config_directory)

    # only import default config if needed
    if path.exists(path.join(config_directory, file)) is not True:
        print("Generating default config...")

        # slice first newline in default config
        default_config = DEFAULT_CONFIG[1:]

        is_default = True

        # paste default config string into newly created config.txt
        with open(path.join(config_directory, file), "w") as config:
            config.write(default_config)

        return default_config, is_default

    # read config
    with open(path.join(config_directory, file)) as config:
        config = config.read()

        if config:
            return config, is_default

        else:
            print("The config is empty! Try adding some ascii art OwO")
            print(f"The config can be located in {config_directory}")
            exit()
