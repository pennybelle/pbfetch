def main():
    import platform, socket, re, psutil, os, subprocess, time

    # TODO: import keywords from config, customizable by user

    # constant for checking cpu usage (in seconds)
    DELAY = 0.25
    DEBUG_DELAY = 0.02

    # parse uptime from /proc/uptime
    def parse_uptime():
        # parse uptime from /proc/uptime
        with open("/proc/uptime", "r") as file:
            seconds = int(float(file.readline().split()[0]))

        # math for time formatting with day, hr, min, sec
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        # string formatting using calculated vals from above
        days = f"{d:d}d"
        hours = f"{h:d}h"
        mins = f"{m:d}m"
        secs = f"{s:d}s"
        uptime = ""

        # only join to uptime if uptime isnt empty
        # else replace empty uptime with new value
        def format_uptime(uptime, time):
            if uptime:
                uptime = " ".join([uptime, time])
            else:
                uptime = time
            
            return uptime

        # only show relevant data (ie: if day is 0, dont show day)
        if d > 0:
            uptime = format_uptime(uptime, days)

        if h > 0:
            uptime = format_uptime(uptime, hours)

        if seconds > 60 and m > 0:
            uptime = format_uptime(uptime, mins)

        if s > 0:
            uptime = format_uptime(uptime, secs)

        if uptime != "":
            return uptime
        else:
            return None


    # parse os name from /etc/os-release
    def parse_os():
        with open("/etc/os-release", "r") as content:
            if content:
                stat_os = content.read()
                stat_os = stat_os.split("=")
                stat_os = stat_os[1].split("\n")[0].replace('"', "")
            else:
                stat_os = None
        
            return stat_os
        

    # parse & format temp from /sys/class/thermal/thermal_zone0/temp
    def parse_temp():
        with open("/sys/class/thermal/thermal_zone0/temp") as temp:
            return round(int(temp.read()) / 1000)


    # parse cpu info from /proc/cpuinfo
    def parse_cpu():
        file = "/proc/cpuinfo"
        try:
            with open(file) as cpu_info:
                cpu_info = cpu_info.readlines()

            cpu_name = None
            
            for line in cpu_info:
                if "model name" not in line:
                    continue
                cpu_name = line.split(":")[1].strip()
            
            return cpu_name

        except Exception as e:
            print(e)
            return None


    # parse memory info from /proc/meminfo
    def parse_mem():
        file = "/proc/meminfo"
        try:
            with open(file) as mem_info:
                mem_info = mem_info.read()
                mem_info = mem_info.split("\n")

            total = None
            active = None

            def mem_format(line):
                return line.split(":")[1].replace("kB", "").strip()

            for line in mem_info:
                if "MemTotal:" in line:
                    total = mem_format(line)
                if "Active:" in line:
                    active = mem_format(line)
                if total and active:
                    used = int(total) - int(active)
                    return int(total), int(used)

        except Exception as e:
            print(e)
            return None, None


    # # parse kernal architecture from /lib/
    # def parse_arch():
    #     if os.path.isfile("/lib/ld-linux-x86-64.so.2"):
    #         return "x86_64"
    #     else:
    #         return "x86"


    # format each line so right side accommodates for stat len
    def horizontal_formatter(fetch_data, key, stat):
        # split fetch string at each keyword (sequentially)
        fetch_data = fetch_data.split(str(key))

        # store lengths for reuse
        key_len = len(key)
        stat_len = len(stat)
        fetch_len = len(fetch_data)

        if key_len < stat_len and fetch_len != 1:
            # number of chars to delete
            diff = stat_len - key_len

            # remove chars following keyword
            for _ in range(diff):
                index = 0
                while (
                    index < diff
                    and fetch_data[1][index] != " "
                ):
                    index += 1

                # TODO: remove char without slicing
                # modified = fetch_data[1][index + 1:] # its because of slicing...
                
                # only remove char if char == " " (IT WORKS!!!!)
                modified = [*fetch_data[1]]
                # modified.reverse()
                del modified[index]
                # modified.reverse()
                modified = "".join(modified)

                # debug
                print(fetch_data[0], end="", flush="")
                print(modified.rstrip())
                time.sleep(DEBUG_DELAY)

                fetch_data[1] = modified

            # # get line length
            # line_len = len(fetch_data[1]) - key_len
            # print(line_len)

            # # remove chars following keyword
            # modified = fetch[1].replace(key, stat).ljust(line_len)

            # # remove chars following keyword
            # modified = fetch[1][diff:]

            # replaces second half with modified string
            fetch_data[1] = modified

            # fetch_data = str(stat).join(fetch_data)

        elif key_len > stat_len and fetch_len != 1:
            # number of chars to add
            diff = key_len - stat_len

            # adds whitespace following keyword
            modified = str(" " * diff) + fetch_data[1]

            # replaces second half with modified string
            fetch_data[1] = modified

            # # rejoin into str and replace keyword with value
            # fetch_data = str(stat).join(fetch_data)

        # rejoin into str and replace keyword with value
        fetch_data = str(stat).join(fetch_data)

        return fetch_data



    ################################
    #####         STATS        #####
    ################################



    # stat logic
    stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
    stat_os = parse_os()
    # stat_arch = platform.machine()
    stat_arch = "x86_64" if os.path.isfile("/lib/ld-linux-x86-64.so.2") else "x86"
    stat_kernel = platform.release()
    stat_version = platform.version()
    stat_uptime = parse_uptime()
    stat_cpu_percent = f"{round(psutil.cpu_percent(DELAY))}%"
    stat_cpu_temp = f"{parse_temp()}°c"
    stat_cpu_name = parse_cpu()
    # TODO: parse memory usage from /proc/meminfo
    ram_total, ram_used = parse_mem()
    # total_ram = round(psutil.virtual_memory().total / (1024.0 ** 2)) # depreciated
    stat_ram = str(
        f"{round(ram_used/1000)}/"
        f"{round(ram_total/1000)}"
        " MB"
    ) if ram_total and ram_used else None
    stat_packages = f"{len(
        str(
            subprocess.check_output(["pacman", "-Q"])
        ).split(" ")
    )} (pacman)"
    statvfs = os.statvfs("/")
    total_disk_size_in_bytes = statvfs.f_frsize * statvfs.f_blocks
    total_disk_size_in_gb = round(total_disk_size_in_bytes / (1024.0 ** 2))
    disk_free_space_gb = round(statvfs.f_frsize * statvfs.f_bfree / (1024.0 ** 2))
    total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
    stat_disk_total_and_used = f"{total_disk_size_used}/{total_disk_size_in_gb} MB"

    # init stats using keywords for configuration in .conf
    stats = {
        "$HOST": stat_hostname,
        "$SYS": stat_os,
        "$ARCH": stat_arch,
        "$KER": stat_kernel,
        "$MEM": stat_ram,
        "$UP": stat_uptime,
        "$PAC": stat_packages,
        "$CPU": stat_cpu_name,
        "$%": stat_cpu_percent,
        "$TEM": stat_cpu_temp,
        "$DISK": stat_disk_total_and_used,
    }


    ################################
    #####     END OF STATS     #####
    ################################


    def fetch():
        # read config and exit if empty
        with open("config.txt", "r") as config:
            content = config.read()
            if content:
                fetch_data = content
            else:
                print("You must insert something in the config!")
                exit()
        
        # omit comments from output
        for line in fetch_data.split("\n"):
            # catch and release comments using # notation
            regex_match = re.search("#.*$", line)
            if regex_match:
                fetch_data = fetch_data.replace(regex_match.group(), "")

        # replace stat keywords with stat data
        for keyword in stats.keys():
            # associate stat keyword with its respective value
            stat = stats[keyword]
            if stat is None:
                continue
            stat = str(stat)

            # format char differences for keyword and respective value
            fetch_data = horizontal_formatter(
                fetch_data,
                keyword,
                stat
            )

        # finally, print fetch to terminal
        # format only from the right
        print(fetch_data.rstrip())
    
    # run fetch
    fetch()

