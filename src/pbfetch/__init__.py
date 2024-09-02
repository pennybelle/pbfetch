from pbfetch.fetch import fetch
from pbfetch.handle_config import handle_config


def main():
    print(fetch(handle_config()))
