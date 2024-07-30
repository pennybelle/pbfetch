import platform, socket, re, uuid, psutil
import os, subprocess, datetime

with open("logo.txt", "r") as logo:
    if logo:
        logo = logo.read()
    else:
        logo = None

# get longest line length of logo for stat formatting
def get_longest_line_length(input):
    if logo:
        return max(len(line) for line in input.splitlines(input))
    else:
        return 0

longest_line = get_longest_line_length(logo)

def get_uptime():
    with open("/proc/uptime", "r") as file:
        seconds = int(float(file.readline().split()[0]))
    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    uptime = ""
    uptime += f"{d:d} day{'s' if d > 1 else ''}," if d > 0 else ""
    uptime += f" {h%24:d} hour{'s' if h > 1 else ''}," if h > 0 else ""
    uptime += f" {m:02d} minute{'s' if m > 1 else ''}" if m > 0 else ""
    uptime += f" {s:02d} second{'s' if m > 1 else ''}" if seconds < 60 else ""

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
            # print(stat_os)
        else:
            stat_os = None
        return stat_os

stat_os = f"OS: {os_parse()}"
stat_kernel = f"Kernel: {platform.release()}"
stat_version = platform.version()
stat_arch = f"Arch: {platform.machine()}"
stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
# stat_ip = socket.gethostbyname(stat_hostname)
# stat_mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
stat_processor = platform.processor()
stat_ram = "RAM: " + str(
    round(psutil.virtual_memory().total / (1024.0 ** 3))
) + " GB"
stat_platform = platform.platform()
stat_uptime = f"Uptime: {get_uptime()}"
stat_packages = f"Packages: {len(str(subprocess.check_output(["pacman", "-Q"])).split(" "))} (pacman)"

stats = [
    stat_hostname,
    stat_os,
    # stat_arch,
    stat_arch,
    stat_kernel,
    stat_ram,
    stat_uptime,
    stat_packages,
    # stat_version,
    # stat_ip,
    # stat_mac,
    stat_processor,
    # stat_platform,
]

# set loop to highest: num of lines in logo or elements in stats array
logo_len = len(logo.splitlines())
stats_len = len(stats)
loop_len = logo_len if logo_len > stats_len else stats_len

# stats use a different index to handle empty lines in logo or null stats properly
stats_index = 0

# enumberate over length of logo or stats list (whichever is longer)
for index in range(loop_len):
    if index < logo_len and logo_len > 0:
        line = logo.splitlines()[index]
    else:
        line = ""

    # append whitespace to logo for formatting
    if len(line) < longest_line:
        line = line + " " * (longest_line - len(line))

    # same as print!("{line}"); followed by a flush
    print(line, end='', flush=True)

    # conditional prevents trying to pring more than stats list contains
    if stats_index >= len(stats):
        # just print a new line
        stats_index += 1
        print()

    elif stats[stats_index]:
        stat = stats[stats_index]

        while stat is None and stats_index > loop_len:
            stats_index += 1
            stat = stats[stats_index]

        # print stat line and then new line
        if logo:
            stat = "   " + str(stat) # buffer

        print(stat)
        stats_index += 1

    else:
        print()
