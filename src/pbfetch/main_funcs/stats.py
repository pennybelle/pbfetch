import pbfetch.parse_funcs.parse_uptime as uptime
import pbfetch.parse_funcs.parse_os as pos
# import pbfetch.parse_funcs.parse_temp as temp
# import pbfetch.parse_funcs.parse_cpu_temp as cpu_temp
import pbfetch.parse_funcs.parse_cpu as cpu
import pbfetch.parse_funcs.parse_mem as mem
# import pbfetch.parse_funcs.parse_login as login
import pbfetch.parse_funcs.parse_kernel as kernel
# import pbfetch.parse_funcs.parse_shell as shell
import pbfetch.parse_funcs.parse_wm as wm
import pbfetch.parse_funcs.parse_de as de
import pbfetch.parse_funcs.parse_fs as fs
import pbfetch.parse_funcs.parse_gpu_name as gpu
import pbfetch.parse_funcs.parse_batt as batt
import pbfetch.parse_funcs.parse_mb as mb
import pbfetch.parse_funcs.parse_comp_name as comp_name
import pbfetch.parse_funcs.parse_bios_type as bios
import pbfetch.parse_funcs.parse_res as res
import pbfetch.parse_funcs.parse_packages as pac
# import pbfetch.parse_funcs.parse_cpu_usage as cpu_usage         
# import pbfetch.parse_funcs.parse_hostname as hostname

import subprocess, platform
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
        ram_total, ram_used, percent = mem.parse_mem()
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
        total_percent_used = round((total_disk_size_used / total_disk_size_in_gb) * 100)
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

    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$comp": comp_name.parse_comp_name(),
        "$user": environ["USER"],
        "$host": stat_hostname(),
        "$sys": pos.parse_os(),
        # "$ARCH": stat_arch,
        "$arch": stat_architecture(),
        "$ker": kernel.parse_kernel_release(),
        "$mem": stat_ram(),
        "$up": uptime.parse_uptime(),
        "$pac": pac.parse_packages(),
        "$cpu": cpu.parse_cpu(),
        # "$tem": stat_cpu_temp(),
        # "$pt": stat_cpu_percent(),
        "$disk": stat_disk_total_and_used(),
        "$shell": stat_shell(),
        "$wm": wm.parse_wm(),
        "$de": de.parse_de(),
        "$fs": fs.parse_fs(),
        "$lang": environ["LANG"],
        "$bat": batt.parse_batt(),
        "$gpun": gpu.parse_gpu(),
        "$mboard": mb.parse_mb(),
        "$bios": bios.parse_bios_type(),
        "$res": res.parse_res(),
        "$datetime": stat_datetime(),
        # "$node": stat_node,
        "$system": system(),
        "$configpath": configpath(),
    }

    return stats_dict
