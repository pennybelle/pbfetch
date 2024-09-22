from pbfetch.fetch import fetch
from pbfetch.config import config


def main():
    return fetch(config())
