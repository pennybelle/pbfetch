import platform, socket, re, uuid, psutil
import os, subprocess, datetime

with open("config.conf", "r") as config:
    content = config.read()
    if content:
        fetch = content
    else:
        print("You must insert something in the config!")
        exit()

def get_uptime():
    with open("/proc/uptime", "r") as file:
        seconds = int(float(file.readline().split()[0]))
    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    uptime = ""
    # TODO: use "".join() to better format spaces
    uptime += f"{d:d} day{'s' if d > 1 else ''}," if d > 0 else ""
    uptime += f" {h%24:d} hour{'s' if h > 1 else ''}," if h > 0 else ""
    uptime += f" {m:2d} minute{'s' if m > 1 else ''}" if m > 0 else ""
    uptime += f"{s:02d} second{'s' if m > 1 else ''}" if seconds < 60 else ""

    if uptime != "":
        return uptime
    else:
        return None

def os_parse():
    with open("/etc/os-release", "r") as content:
        if content:
            stat_os = content.read()
            stat_os = stat_os.split("=")
            stat_os = stat_os[1].split("\n")[0].replace('"', "")
        else:
            stat_os = None
    
        return stat_os
    

stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
stat_os = f"OS: {os_parse()}"
stat_arch = f"Arch: {platform.machine()}"
stat_kernel = f"Kernel: {platform.release()}"
stat_version = platform.version()
stat_ram = "RAM: " + str(
    round(psutil.virtual_memory().total / (1024.0 ** 3))
) + " GB"
stat_uptime = f"{get_uptime()}"
stat_packages = f"{len(str(subprocess.check_output(["pacman", "-Q"])).split(" "))} (pacman)"

stats = {
    "HOSTNAME": stat_hostname,
    "OPERATINGSYSTEM": stat_os,
    "ARCHITECTURE": stat_arch,
    "KERNEL": stat_kernel,
    "MEMORY": stat_ram,
    "UPTIME": stat_uptime,
    "PACKAGES": stat_packages,
}

for line in fetch.split("\n"):
    regex_match = re.search("#.*$", line)
    # print(regex_match) # debug
    if regex_match:
        fetch = fetch.replace(regex_match.group(), "")

for stat in stats.keys():
    fetch = fetch.replace(stat, stats[stat])

print(fetch.strip())