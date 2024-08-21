from pbfetch.parsers import cpu_temperature
from psutil import cpu_percent

# # constant for checking cpu usage (in seconds)
# DELAY = 0.25


# parse cpu info from /proc/cpuinfo
def parse():
    file = "/proc/cpuinfo"
    try:
        with open(file) as cpu_info:
            cpu_info = cpu_info.readlines()

        cpu_name = None

        for line in cpu_info:
            if "model name" not in line:
                continue
            cpu_name = line.split(":")[1].strip()

        return (
            f"{cpu_name} "
            f"({cpu_temperature.parse()}°c) "
            f"({round(cpu_percent())}%)"
        )

    except Exception as e:
        print(e)
        return None
