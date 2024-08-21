from pbfetch.fetch import fetch
from pbfetch.config import parse_config

# TODO: import keywords from config, customizable by user


def main():
    print(fetch(parse_config()))
