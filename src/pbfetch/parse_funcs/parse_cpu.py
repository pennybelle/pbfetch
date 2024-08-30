import pbfetch.parse_funcs.parse_cpu_temp as cpu_temp
from psutil import cpu_percent

# # constant for checking cpu usage (in seconds)
# DELAY = 0.25


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

        temp = cpu_temp.parse_cpu_temp()
        usage = int(cpu_percent())

        cpu = cpu_name
        cpu += f" ({temp}°c)" if temp else ""
        cpu += f" ({usage}%)" if usage != 0 else ""

        return cpu

    except Exception as e:
        print(e)
        return None
