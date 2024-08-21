# parse memory info from /proc/meminfo
def parse():
    file = "/proc/meminfo"
    try:
        with open(file) as mem_info:
            mem_info = mem_info.read()
            mem_info = mem_info.splitlines()

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
                percent = round((int(active) / int(total)) * 100)
                return int(total), int(used), percent

    except Exception as e:
        print(e)
        return None, None
