from pbfetch.fetch import fetch
from pbfetch.config import handle_config


def main():
    print(fetch(handle_config()))
