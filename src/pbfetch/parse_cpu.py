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
