import platform, socket, re, psutil, os, subprocess

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

    days = f"{d:d}d"
    hours = f"{h:d}h"
    mins = f"{m:d}m"
    secs = f"{s:d}s"
    uptime = ""

    def format_uptime(uptime, time):
        if uptime:
            uptime = " ".join([uptime, time])
        else:
            uptime = time
        
        return uptime

    if d > 0:
        uptime = format_uptime(uptime, days)

    if h > 0:
        uptime = format_uptime(uptime, hours)

    if seconds > 60:
        uptime = format_uptime(uptime, mins)

    if s > 0:
        uptime = format_uptime(uptime, secs)

    # uptime += f"{h:2d} hours " if h > 0 else ""
    # uptime += f"{m:2d} mins " if seconds > 60 else ""
    # uptime += f"{s:2d} secs" if s > 0 else ""

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
    

# stat logic
stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
stat_os = os_parse()
stat_arch = platform.machine()
stat_kernel = platform.release()
stat_version = platform.version()
stat_uptime = get_uptime()
stat_ram = str(
    round(psutil.virtual_memory().total / (1024.0 ** 3))
) + "GB"
stat_packages = f"{len(
    str(
        subprocess.check_output(["pacman", "-Q"])
    ).split(" ")
)} (pacman)"


# init stats using keywords for configuration in .conf
stats = {
    "$HOST": stat_hostname,
    "$SYS": stat_os,
    "$ARCH": stat_arch,
    "$KER": stat_kernel,
    "$MEM": stat_ram,
    "$UP": stat_uptime,
    "$PAC": stat_packages,
}

for index, line in enumerate(fetch.split("\n")):
    # # remove whitespace from each line
    # stripped_line = line.strip()
    # fetch = fetch.replace(fetch[index], stripped_line)

    # catch and release comments using # notation
    regex_match = re.search("#.*$", line)
    if regex_match:
        fetch = fetch.replace(regex_match.group(), "")


def horizontal_formatter(fetch, stat, keyword_len, stat_len, fetch_len):
    if keyword_len < stat_len and fetch_len != 1:
        # number of chars to delete
        diff = stat_len - keyword_len

        # remove chars following keyword
        modified = fetch[1][diff:]

        # replaces second half with modified string
        fetch[1] = modified

    elif keyword_len > stat_len and fetch_len != 1:
        # number of chars to add
        diff = keyword_len - stat_len

        # adds whitespace following keyword
        modified = str(" " * diff) + fetch[1]

        # replaces second half with modified string
        fetch[1] = modified

    # rejoin into str and replace keyword with value
    fetch = str(stat).join(fetch)

    return fetch


for keyword in stats.keys():
    # split fetch string at each keyword (sequentially)
    fetch = fetch.split(keyword)

    # associate stat keyword with its respective value
    stat = stats[keyword]

    # store lengths for reuse
    keyword_len = len(keyword)
    stat_len = len(stat)
    fetch_len = len(fetch)

    # format char differences for keyword and respective value
    fetch = horizontal_formatter(
        fetch,
        stat,
        keyword_len,
        stat_len,
        fetch_len
    )

print(fetch.strip())