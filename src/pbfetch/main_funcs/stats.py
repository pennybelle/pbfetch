from pbfetch.parse_funcs.parse_uptime import parse_uptime
from pbfetch.parse_funcs.parse_os import parse_os
from pbfetch.parse_funcs.parse_cpu import parse_cpu
from pbfetch.parse_funcs.parse_mem import parse_mem
from pbfetch.parse_funcs.parse_kernel import parse_kernel_release
from pbfetch.parse_funcs.parse_wm import parse_wm
from pbfetch.parse_funcs.parse_de import parse_de
from pbfetch.parse_funcs.parse_fs import parse_fs
from pbfetch.parse_funcs.parse_gpu_name import parse_gpu
from pbfetch.parse_funcs.parse_batt import parse_batt
from pbfetch.parse_funcs.parse_mb import parse_mb
from pbfetch.parse_funcs.parse_comp_name import parse_comp_name
from pbfetch.parse_funcs.parse_bios_type import parse_bios_type
from pbfetch.parse_funcs.parse_res import parse_res
from pbfetch.parse_funcs.parse_packages import parse_packages
from pbfetch.parse_funcs.parse_disc import parse_disc
from pbfetch.parse_funcs.parse_shell import parse_shell
from pbfetch.parse_funcs.parse_theme import parse_theme
from pbfetch.parse_funcs.parse_term_font import parse_term_font
from pbfetch.parse_funcs.parse_font import parse_font
# from pbfetch.parse_funcs.parse_weather import parse_weather

import os
from subprocess import check_output
from platform import uname
from pathlib import Path


def get_config_dir():
    return os.environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))

# fill a tuple with uname info to use for other stats
_uname = tuple(uname())
environ =  dict(os.environ)

def configpath():
    return str(
        os.path.join(
            get_config_dir(),
            "config.txt"
        )
    )

def system():
    return _uname[0]

def stat_host():
    return _uname[1]

def stat_architecture():
    return _uname[4]

def stat_hostname():
    # return f"{login.parse_login()}@{hostname.parse_hostname()}"
    return f"{environ["USER"]}@{stat_host()}"

def stat_datetime():
    return " ".join(
        check_output(["date"]).decode("utf-8").split()
    )

########################################

def stats(fetch_data):
    # init stats using keywords for configuration in .conf
    # TODO: add easter egg stats for fun dynamic things
    stats_dict = {
        "$cmp": parse_comp_name() if "$cmp" in fetch_data else None,
        "$usr": environ["USER"] if "$usr" in fetch_data else None,
        "$hst": stat_hostname() if "$hst" in fetch_data else None,
        "$sys": parse_os() if "$sys" in fetch_data else None,
        "$ach": stat_architecture() if "$arc" in fetch_data else None,
        "$ker": parse_kernel_release() if "$ker" in fetch_data else None,
        "$mem": parse_mem() if "$mem" in fetch_data else None,
        "$upt": parse_uptime() if "$upt" in fetch_data else None,
        "$pac": parse_packages() if "$pac" in fetch_data else None,
        "$cpu": parse_cpu() if "$cpu" in fetch_data else None,
        "$dsk": parse_disc() if "$dsk" in fetch_data else None,
        "$shl": parse_shell() if "$shl" in fetch_data else None,
        "$wmn": parse_wm() if "$wmn" in fetch_data else None,
        "$den": parse_de() if "$den" in fetch_data else None,
        "$fsm": parse_fs() if "$fsm" in fetch_data else None,
        "$lcl": environ["LANG"] if "$lcl" in fetch_data else None,
        "$bat": parse_batt() if "$bat" in fetch_data else None,
        "$gpu": parse_gpu() if "$gpu" in fetch_data else None,
        "$mbd": parse_mb() if "$mbd" in fetch_data else None,
        "$bio": parse_bios_type() if "$bio" in fetch_data else None,
        "$res": parse_res() if "$res" in fetch_data else None,
        "$dat": stat_datetime() if "$dat" in fetch_data else None,
        "$thm": parse_theme() if "$thm" in fetch_data else None,
        "$fnt": parse_font() if "$fnt" in fetch_data else None,
        "$tft": parse_term_font() if "$tft" in fetch_data else None,
        "$configpath": configpath() if "$configpath" in fetch_data else None,
        "$system": system(),
    }

    return stats_dict
