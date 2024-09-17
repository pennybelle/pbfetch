from os import environ, path
from subprocess import check_output
from platform import uname, machine
from pathlib import Path

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
from pbfetch.parse.os import parse_os
from pbfetch.parse.packages import parse_packages
from pbfetch.parse.resolution import parse_res
from pbfetch.parse.shell import parse_shell
from pbfetch.parse.term_font import parse_term_font
from pbfetch.parse.theme import parse_theme
from pbfetch.parse.uptime import parse_uptime
from pbfetch.parse.wm import parse_wm


def get_config_dir():
    return environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))


def configpath():
    return str(path.join(get_config_dir(), "config.txt"))


# fill a tuple with uname info to use for other stats
_uname = tuple(uname())
environ = dict(environ)


def system():
    return _uname[0]


def stat_host():
    return _uname[1]


def stat_architecture():
    return _uname[4]


def stat_hostname():
    # return f"{login.parse_login()}@{hostname.parse_hostname()}"
    return f"{environ['USER']}@{stat_host()}"


def stat_datetime():
    return " ".join(check_output(["date"]).decode("utf-8").split())


# TODO: add easter egg stats for fun dynamic things You, 1 second ago • Uncommitted changes
KEYWORDS = {
    "$upt": parse_uptime,
    "$cmp": parse_comp_name,
    "$usr": lambda: environ["USER"],
    "$hst": stat_hostname,
    "$sys": parse_os,
    "$arc": lambda: str(machine()),
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
    "$dat": stat_datetime,
    "$thm": parse_theme,
    "$fnt": parse_font,
    "$tft": parse_term_font,
    "$configpath": configpath,
    "$system": system,
}


def stats(fetch_data):
    init = ["$system", "$hst", "$configpath"]
    stats_dict = {}

    for keyword in KEYWORDS:
        if keyword in init or keyword in fetch_data:
            stats_dict[keyword] = KEYWORDS[keyword]()

    return stats_dict
