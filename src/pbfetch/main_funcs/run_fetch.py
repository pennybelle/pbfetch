from pbfetch.main_funcs.fetch import fetch
from pbfetch.main_funcs.handle_config import handle_config

# TODO: import keywords from config, customizable by user


def run_fetch():
    # generate/read config
    fetch_data = handle_config()

    # print fetch
    print(fetch(fetch_data))
