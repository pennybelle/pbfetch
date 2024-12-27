from os import environ, path
from subprocess import check_output, run
from platform import uname
from pathlib import Path

# import requests

from pbfetch.parse.battery import parse_batt
from pbfetch.parse.bios_type import parse_bios_type
from pbfetch.parse.computer_name import parse_comp_name
from pbfetch.parse.cpu import parse_cpu
from pbfetch.parse.de import parse_de
from pbfetch.parse.disk import parse_disk
from pbfetch.parse.font import parse_font
from pbfetch.parse.fs import parse_fs
from pbfetch.parse.gpu import parse_gpu
from pbfetch.parse.kernel import parse_kernel_release
from pbfetch.parse.memory import parse_mem
from pbfetch.parse.motherboard import parse_mb
from pbfetch.parse.packages import parse_packages
from pbfetch.parse.resolution import parse_res
from pbfetch.parse.shell import parse_shell
from pbfetch.parse.term_font import parse_term_font
from pbfetch.parse.theme import parse_theme
from pbfetch.parse.uptime import parse_uptime
from pbfetch.parse.wm import parse_wm


# fill a tuple with uname info to use for other stats
_uname = tuple(uname())
environ = dict(environ)


def get_config_dir():
    return environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))


def configpath():
    return str(path.join(get_config_dir(), "config.txt"))


# parse os name from /etc/os-release
def parse_os():
    try:
        with open("/etc/os-release", "r") as content:
            if content:
                stat_os = content.read()
                stat_os = stat_os.split("=")
                stat_os = stat_os[1].splitlines()[0].replace('"', "")
            else:
                stat_os = None

            return f"{stat_os} {_uname[4]}"

    except Exception as e:
        print(f"Parse OS Error: {e}")
        return None


def term():
    term = environ["TERM"]
    # term_size = run(["stty", "size"], capture_output=True).stdout.decode()
    # print(term_size)
    try:
        term_ver = run([term, "--version"], capture_output=True).stdout
        term_ver = term_ver.decode().split(" ")
        for i in term_ver:
            if "." in i:
                return f"{term} {i}"
        return term

    except Exception:
        return term


# def is_connected():
#     try:
#         requests.get("https://www.google.com")

#     except Exception:
#         return


# TODO: add easter egg stats for fun dynamic things
KEYWORDS = {
    "$upt": parse_uptime,
    "$cmp": parse_comp_name,
    "$usr": lambda: environ["USER"],
    "$nde": lambda: _uname[1],
    "$hst": lambda: f"{environ['USER']}@{_uname[1]}",
    "$sys": parse_os,
    "$arc": lambda: _uname[4],
    "$ker": parse_kernel_release,
    "$mem": parse_mem,
    "$pac": parse_packages,
    "$cpu": parse_cpu,
    "$dsc": parse_disk,
    "$shl": parse_shell,
    "$wmn": parse_wm,
    "$den": parse_de,
    "$fsm": parse_fs,
    "$lcl": lambda: environ["LANG"],
    "$bat": parse_batt,
    "$gpu": parse_gpu,
    "$mbd": parse_mb,
    "$bio": parse_bios_type,
    "$res": parse_res,
    "$dat": lambda: " ".join(check_output(["date"]).decode("utf-8").split()),
    "$thm": parse_theme,
    "$fnt": parse_font,
    "$tft": parse_term_font,
    "$trm": term,
    "$configpath": configpath,
    "$system": lambda: _uname[0],
}


def stats(fetch_data):
    init = ["$system", "$hst", "$configpath"]
    stats_dict = {}

    for keyword in KEYWORDS:
        if keyword in init or keyword in fetch_data:
            stats_dict[keyword] = KEYWORDS[keyword]()

    return stats_dict
