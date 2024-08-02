# from pbfetch.main_funcs.stats import stat_uptime


def parse_cpu_usage():
    file = "/proc/loadavg"
    # ghz = 0
    # mhz = 0
    try:
        with open(file) as cpu_info:
            cpu_info = cpu_info.read()
            cpu_info = cpu_info.split(" ")
            usage = float(cpu_info[2])

        # for line in cpu_info:
        #     if "model name" in line and "GHz" in line:
        #         ghz += int(float(line.split(" ")[-1].replace("GHz", "")))

        #     if "cpu MHz" in line:
        #         mhz += int(float(line.split()[-1]))

        # return ghz, mhz
        return int((usage) * 100)

    except Exception as e:
        print(e)
        return None
