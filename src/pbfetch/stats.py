from pbfetch.parsers import (
    uptime,
    computer_name,
    os_release,
    kernel,
    packages,
    resolution,
    bios_type,
    motherboard,
    gpu,
    battery,
    cpu,
    fs,
    de,
    wm,
    memory,
)

import subprocess
import platform
import os
from os import statvfs
from pathlib import Path


def get_config_dir():
    return os.environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))


def stats():
    # # constant for checking cpu usage (in seconds)
    # DELAY = 0.025

    # fill a tuple with uname info to use for other stats
    _uname = tuple(platform.uname())
    environ = dict(os.environ)

    def configpath():
        return str(os.path.join(get_config_dir(), "config.txt"))

    def system():
        return _uname[0]

    def stat_host():
        return _uname[1]

    def stat_architecture():
        return _uname[4]

    def stat_hostname():
        # return f"{login.parse_login()}@{hostname.parse_hostname()}"
        return f"{environ["USER"]}@{stat_host()}"

    # def stat_cpu_percent():
    #     # stat_cpu_percent = cpu_usage.parse_cpu_usage() # faster but less accurate
    #     return f"{round(psutil.cpu_percent(DELAY))}%"

    # def stat_cpu_temp():
    #     # stat_cpu_temp = f"{temp.parse_temp()}°c"
    #     return f"{cpu_temp.parse_cpu_temp()}°c"

    # def stat_cpu():
    #     return (
    #         f"{cpu.parse_cpu()} "
    #         f"({cpu_temp.parse_cpu_temp()}°c) "
    #         f"({round(psutil.cpu_percent(DELAY))}%)"
    #     )

    def stat_ram():
        ram_total, ram_used, percent = memory.parse()
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
        total_disk_size_in_gb = round(total_disk_size_in_bytes / (1024.0**2))
        disk_free_space_gb = round(vfs.f_frsize * vfs.f_bfree / (1024.0**2))
        total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
        total_percent_used = round((total_disk_size_used / total_disk_size_in_gb) * 100)
        return (
            f"{total_disk_size_used} / "
            f"{total_disk_size_in_gb} MB "
            f"({total_percent_used}%)"
        )

    def stat_shell():
        shell_pre_parse = environ["SHELL"].split("/")[-1]
        shell_mid_parse = str(
            subprocess.check_output([f"{shell_pre_parse}", "--version"]).decode("utf-8")
        )
        shell_post_parse = shell_mid_parse.split()
        shell_name = shell_post_parse[0]
        shell_version = shell_post_parse[1]
        return f"{shell_name} {shell_version}"

    def stat_datetime():
        return " ".join(subprocess.check_output(["date"]).decode("utf-8").split())

    ########################################

    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$comp": computer_name.parse(),
        "$user": environ["USER"],
        "$host": stat_hostname(),
        "$sys": os_release.parse(),
        # "$ARCH": stat_arch,
        "$arch": stat_architecture(),
        "$ker": kernel.parse(),
        "$mem": stat_ram(),
        "$up": uptime.parse(),
        "$pac": packages.parse(),
        "$cpu": cpu.parse(),
        # "$tem": stat_cpu_temp(),
        # "$pt": stat_cpu_percent(),
        "$disk": stat_disk_total_and_used(),
        "$shell": stat_shell(),
        "$wm": wm.parse(),
        "$de": de.parse(),
        "$fs": fs.parse(),
        "$lang": environ["LANG"],
        "$bat": battery.parse(),
        "$gpun": gpu.parse(),
        "$mboard": motherboard.parse(),
        "$bios": bios_type.parse(),
        "$res": resolution.parse(),
        "$datetime": stat_datetime(),
        # "$node": stat_node,
        "$system": system(),
        "$configpath": configpath(),
    }

    return stats_dict
