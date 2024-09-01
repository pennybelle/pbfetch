from pbfetch.main_funcs.stats import get_config_dir

from os import path, makedirs, environ

# from pbfetch.main_funcs.stats import system

user = environ["USER"]


file = "config.txt"
usr_tmp = path.join("/", "usr", "share", "pbfetch", "config")
config_directory = get_config_dir()


def handle_config():
    if path.isdir(config_directory):
        if path.exists(path.join(config_directory, file)) is not True:
            print("Generating default config")

            # only import default config if needed
            from pbfetch.constants.default_config import DEFAULT_CONFIG

            # paste default config string into newly created config.txt
            with open(path.join(config_directory, file), "w") as config:
                config.write(DEFAULT_CONFIG)

        # read config
        with open(path.join(config_directory, file)) as config:
            content = config.read()

            if content:
                config = content
            else:
                print("The config is empty! Try adding some ascii art OwO")
                print(f"The config can be located in {config_directory}")
                exit()

    else:
        print(f"Generating new config in {config_directory}")

        # only import default config if needed
        from pbfetch.constants.default_config import DEFAULT_CONFIG

        content = DEFAULT_CONFIG

        if content:
            # make config directory
            makedirs(config_directory)

            # paste default config string into newly created config.txt
            with open(path.join(config_directory, file), "w") as config:
                config.write(DEFAULT_CONFIG)

            config = content
            print("Default config copied successfully")
        else:
            print("The default config is empty...Uh Oh!")
            exit()

    return config
