import pbfetch.parse_funcs.parse_uptime as uptime
import pbfetch.parse_funcs.parse_os as pos
import pbfetch.parse_funcs.parse_temp as temp
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


def stats():
    # constant for checking cpu usage (in seconds)
    DELAY = 0.2



    ################################
    #####         STATS        #####
    ################################



    # uname = tuple(platform.uname())
    _uname = tuple(platform.uname())
    system = _uname[0]
    environ = dict(os.environ)

    stat_user = environ["USER"]
    stat_host = _uname[1]
    stat_kernel_ver = _uname[2]
    stat_architecture = _uname[4]
    stat_hostname = f"{stat_user}@{stat_host}"
    # stat_hostname = f"{login.parse_login()}@{hostname.parse_hostname()}"
    stat_os = pos.parse_os()
    # stat_arch = platform.machine()
    stat_kernel = kernel.parse_kernel_release()
    stat_uptime = uptime.parse_uptime()
    stat_cpu_percent = f"{round(psutil.cpu_percent(DELAY))}%"
    # stat_cpu_percent = cpu_usage.parse_cpu_usage()
    stat_cpu_temp = f"{temp.parse_temp()}°c" 
    stat_cpu_name = cpu.parse_cpu()
    ram_total, ram_used = mem.parse_mem()
    stat_ram = str(
        f"{round(ram_used/1024)}/"
        f"{round(ram_total/1024)}"
        " MB"
    ) if ram_total and ram_used else None
    stat_packages = f"{len(
        str(
            subprocess.check_output(["pacman", "-Q"])
        ).split(" ")
    )} (pacman)"
    stat_vfs = statvfs("/")
    total_disk_size_in_bytes = stat_vfs.f_frsize * stat_vfs.f_blocks
    total_disk_size_in_gb = round(
        total_disk_size_in_bytes / (1024.0 ** 2)
    )
    disk_free_space_gb = round(
        stat_vfs.f_frsize * stat_vfs.f_bfree / (1024.0 ** 2)
    )
    total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
    stat_disk_total_and_used = (
        f"{total_disk_size_used}/{total_disk_size_in_gb} MB"
    )
    configpath = str(
        os.path.join(
            "/",
            "home",
            stat_user,
            ".config",
            "pbfetch",
            "config"
        )
    )
    # stat_shell = shell.parse_shell()
    stat_shell = environ["SHELL"]
    stat_wm = wm.parse_wm() # pgrep -l compiz |cut -d " " -f2
    stat_de = de.parse_de()
    stat_fs = fs.parse_fs()
    stat_lang = environ["LANG"]
    stat_datetime = " ".join(subprocess.check_output(["date"]).decode("utf-8").split())
    stat_gpu_name = gpu.parse_gpu()
    stat_bat = batt.parse_batt()
    stat_mb = mb.parse_mb()
    stat_comp_name = comp_name.parse_comp_name()
    stat_bios_type = bios.parse_bios_type()
    stat_res = res.parse_res()
    # stat_node = platform.node()

    ##################################################################################
    ##################################################################################
    ##################################################################################

    # TODO: add easter egg stats for fun dynamic things
    # init stats using keywords for configuration in .conf
    stats_dict = {
        # "$UNAME": _uname,
        "$user": stat_user,
        "$host": stat_hostname,
        "$sys": stat_os,
        # "$ARCH": stat_arch,
        "$arch": stat_architecture,
        "$ker": stat_kernel,
        "$mem": stat_ram,
        "$up": stat_uptime,
        "$pac": stat_packages,
        "$cpu": stat_cpu_name,
        "$tem": stat_cpu_temp,
        "$pt": stat_cpu_percent,
        "$disk": stat_disk_total_and_used,
        "$shell": stat_shell,
        "$wm": stat_wm,
        "$de": stat_de,
        "$fs": stat_fs,
        "$lang": stat_lang,
        "$bat": stat_bat,
        "$gpun": stat_gpu_name,
        "$mboard": stat_mb,
        "$bios": stat_bios_type,
        "$comp": stat_comp_name,
        "$res": stat_res,
        "$datetime": stat_datetime,
        # "$node": stat_node,
        "$system": system,
        "$configpath": configpath,
    }



        ################################
        #####     END OF STATS     #####
        ################################



    return stats_dict
