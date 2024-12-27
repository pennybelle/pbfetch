from pbfetch.handle_error import error
from pbfetch.parse.cpu_temp import parse_cpu_temp
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
            break

        if cpu_name:
            # parse verbose output and strip whitespace
            cpu_name = cpu_name.replace("with Radeon Graphics", "")
            cpu_name = cpu_name.strip()

            temp = parse_cpu_temp()
            usage = int(cpu_percent())

            cpu = cpu_name
            cpu += f" ({temp}°c)" if temp else ""
            cpu += f" ({usage}%)" if usage != 0 else ""

            return cpu

        else:
            print("Error: CPU: Model Name not found in /proc/cpuinfo")
            return cpu_name

    except Exception as e:
        print(error(e, "CPU"))
        return None
