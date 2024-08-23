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

def stats():
    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$cmp": parse_comp_name(),
        "$usr": environ["USER"],
        "$hst": stat_hostname(),
        "$sys": parse_os(),
        # "$ARCH": stat_arch,
        "$ach": stat_architecture(),
        "$ker": parse_kernel_release(),
        "$mem": parse_mem(),
        "$upt": parse_uptime(),
        "$pac": parse_packages(),
        "$cpu": parse_cpu(),
        # "$tem": stat_cpu_temp(),
        # "$pt": stat_cpu_percent(),
        "$dsk": parse_disc(),
        "$shl": parse_shell(),
        "$wmn": parse_wm(),
        "$den": parse_de(),
        "$fsm": parse_fs(),
        "$lcl": environ["LANG"],
        "$bat": parse_batt(),
        "$gpu": parse_gpu(),
        "$mbd": parse_mb(),
        "$bio": parse_bios_type(),
        "$res": parse_res(),
        "$dat": stat_datetime(),
        "$thm": parse_theme(),
        "$fnt": parse_font(),
        "$tft": parse_term_font(),
        # "$weather": parse_weather(),
        # "$node": stat_node,
        "$system": system(),
        "$configpath": configpath(),
    }

    return stats_dict
