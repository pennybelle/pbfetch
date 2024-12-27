from pbfetch.handle_error import error


def mem_format(line):
    return line.split(":")[1].replace("kB", "").strip()


# parse memory info from /proc/meminfo
def parse_mem():
    file = "/proc/meminfo"
    try:
        with open(file) as mem_info:
            mem_info = mem_info.read()
            mem_info = mem_info.splitlines()

        total = None
        free = None

        for line in mem_info:
            if total and free:
                break

            if "MemTotal:" in line:
                total = mem_format(line)
            if "MemFree:" in line:
                free = mem_format(line)

        if total and free:
            total, free = int(total), int(free)
            used = total - free
            percent = round(used / total * 100)

            if percent < 1:
                percent = "<1"

            return str(
                f"{used/1024/1024:.2f} / " f"{total/1024/1024:.2f}" f" GB ({percent}%)"
            )

        else:
            print("Error: could not parse ram usage")
            return None

    except Exception as e:
        print(error(e, "RAM"))
        return None
