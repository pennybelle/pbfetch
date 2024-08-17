import pbfetch.parse_funcs.parse_uptime as uptime
import pbfetch.parse_funcs.parse_os as pos
import pbfetch.parse_funcs.parse_temp as temp
import pbfetch.parse_funcs.parse_cpu_temp as cpu_temp
import pbfetch.parse_funcs.parse_cpu as cpu
import pbfetch.parse_funcs.parse_mem as mem
import pbfetch.parse_funcs.parse_login as login
import pbfetch.parse_funcs.parse_kernel as kernel
import pbfetch.parse_funcs.parse_shell as shell
import pbfetch.parse_funcs.parse_wm as wm
import pbfetch.parse_funcs.parse_de as de
import pbfetch.parse_funcs.parse_fs as fs
import pbfetch.parse_funcs.parse_gpu_name as gpu
import pbfetch.parse_funcs.parse_batt as batt
import pbfetch.parse_funcs.parse_mb as mb
import pbfetch.parse_funcs.parse_comp_name as comp_name
import pbfetch.parse_funcs.parse_bios_type as bios
import pbfetch.parse_funcs.parse_res as res
import pbfetch.parse_funcs.parse_cpu_usage as cpu_usage         
# import pbfetch.parse_funcs.parse_hostname as hostname

import subprocess, platform, psutil
import os
from os import statvfs
from pathlib import Path

def get_config_dir():
    return os.environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))

def stats():
    # constant for checking cpu usage (in seconds)
    DELAY = 0.025
    
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

    def stat_user():
        return environ["USER"]
    
    def stat_host():
        return _uname[1]
    
    def stat_architecture():
        return _uname[4]
    
    def stat_hostname():
        # return f"{login.parse_login()}@{hostname.parse_hostname()}"
        return f"{stat_user()}@{stat_host()}"
    
    def stat_os():
        return pos.parse_os()
    
    # def stat_kernel_ver():
    #     return _uname[2]
    
    def stat_kernel():
        return kernel.parse_kernel_release()
    
    def stat_uptime():
        return uptime.parse_uptime()
    
    def stat_cpu_percent():
        # stat_cpu_percent = cpu_usage.parse_cpu_usage() # faster but less accurate
        return f"{round(psutil.cpu_percent(DELAY))}%"
    
    def stat_cpu_temp():
        # stat_cpu_temp = f"{temp.parse_temp()}°c"
        return f"{cpu_temp.parse_cpu_temp()}°c"
    
    def stat_cpu_name():
        return cpu.parse_cpu()
    
    def stat_ram():
        ram_total, ram_used = mem.parse_mem()
        if ram_total and ram_used:
            return str(
                f"{round(ram_used/1024)} / "
                f"{round(ram_total/1024)}"
                " MB"
            ) 
        else: 
            return None
    
    def stat_packages():
        return f"{len(
            str(
                subprocess.check_output(["pacman", "-Q"])
            ).split(" ")
        )} (pacman)"
    
    
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
        return (
            f"{total_disk_size_used} / {total_disk_size_in_gb} MB"
        )
    
    def stat_shell():
        shell_pre_parse = environ["SHELL"].replace("/bin/", "")
        shell_mid_parse = str(
            subprocess.check_output(
                [f"{shell_pre_parse}", "--version"]
            ).decode("utf-8")
        )
        shell_post_parse = shell_mid_parse.split()
        shell_name = shell_post_parse[0]
        shell_version = shell_post_parse[1]
        return f"{shell_name} {shell_version}"
    
    def stat_wm():
        return wm.parse_wm() # pgrep -l compiz |cut -d " " -f2
    
    def stat_de():
        return de.parse_de()
    
    def stat_fs():
        return fs.parse_fs()
    
    def stat_lang():
        return environ["LANG"]
    
    def stat_datetime():
        return " ".join(
            subprocess.check_output(["date"]).decode("utf-8").split()
        )
    
    def stat_gpu_name():
        return gpu.parse_gpu()
    
    def stat_bat():
        return batt.parse_batt()
    
    def stat_mb():
        return mb.parse_mb()
    
    def stat_comp_name():
        return comp_name.parse_comp_name()
    
    def stat_bios_type():
        return bios.parse_bios_type()
    
    def stat_res():
        return res.parse_res()
    
    ########################################

    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$user": stat_user(),
        "$host": stat_hostname(),
        "$sys": stat_os(),
        # "$ARCH": stat_arch,
        "$arch": stat_architecture(),
        "$ker": stat_kernel(),
        "$mem": stat_ram(),
        "$up": stat_uptime(),
        "$pac": stat_packages(),
        "$cpu": stat_cpu_name(),
        "$tem": stat_cpu_temp(),
        "$pt": stat_cpu_percent(),
        "$disk": stat_disk_total_and_used(),
        "$shell": stat_shell(),
        "$wm": stat_wm(),
        "$de": stat_de(),
        "$fs": stat_fs(),
        "$lang": stat_lang(),
        "$bat": stat_bat(),
        "$gpun": stat_gpu_name(),
        "$mboard": stat_mb(),
        "$bios": stat_bios_type(),
        "$comp": stat_comp_name(),
        "$res": stat_res(),
        "$datetime": stat_datetime(),
        # "$node": stat_node,
        "$system": system(),
        "$configpath": configpath(),
    }

    return stats_dict
