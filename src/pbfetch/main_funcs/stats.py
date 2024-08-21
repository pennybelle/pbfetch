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

import subprocess, platform
import os
from os import statvfs
from pathlib import Path

def get_config_dir():
    return os.environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))

# fill a tuple with uname info to use for other stats
_uname = tuple(platform.uname())
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

def stat_ram():
    ram_total, ram_used, percent = parse_mem()
    if ram_total and ram_used:
        return str(
            f"{round(ram_used/1024)} / "
            f"{round(ram_total/1024)}"
            f" MB ({percent}%)"
        ) 
    else: 
        return None

def stat_disk_total_and_used():
    vfs = statvfs("/")
    total_disk_size_in_bytes = vfs.f_frsize * vfs.f_blocks
    total_disk_size_in_gb = round(
        total_disk_size_in_bytes / (1024.0 ** 2)
    )
    disk_free_space_gb = round(
        vfs.f_frsize * vfs.f_bfree / (1024.0 ** 2)
    )
    total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
    total_percent_used = round(
        (total_disk_size_used / total_disk_size_in_gb) * 100
    )
    return (
        f"{total_disk_size_used} / "
        f"{total_disk_size_in_gb} MB "
        f"({total_percent_used}%)"
    )

def stat_shell():
    shell_pre_parse = environ["SHELL"].split("/")[-1]
    shell_mid_parse = str(
        subprocess.check_output(
            [f"{shell_pre_parse}", "--version"]
        ).decode("utf-8")
    )
    shell_post_parse = shell_mid_parse.split()
    shell_name = shell_post_parse[0]
    shell_version = shell_post_parse[1]
    return f"{shell_name} {shell_version}"

def stat_datetime():
    return " ".join(
        subprocess.check_output(["date"]).decode("utf-8").split()
    )

########################################

def stats():
    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$comp": parse_comp_name(),
        "$user": environ["USER"],
        "$host": stat_hostname(),
        "$sys": parse_os(),
        # "$ARCH": stat_arch,
        "$arch": stat_architecture(),
        "$ker": parse_kernel_release(),
        "$mem": stat_ram(),
        "$up": parse_uptime(),
        "$pac": parse_packages(),
        "$cpu": parse_cpu(),
        # "$tem": stat_cpu_temp(),
        # "$pt": stat_cpu_percent(),
        "$disk": stat_disk_total_and_used(),
        "$shell": stat_shell(),
        "$wm": parse_wm(),
        "$de": parse_de(),
        "$fs": parse_fs(),
        "$lang": environ["LANG"],
        "$bat": parse_batt(),
        "$gpun": parse_gpu(),
        "$mboard": parse_mb(),
        "$bios": parse_bios_type(),
        "$res": parse_res(),
        "$datetime": stat_datetime(),
        # "$node": stat_node,
        "$system": system(),
        "$configpath": configpath(),
    }

    return stats_dict
