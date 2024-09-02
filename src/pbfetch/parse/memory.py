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
        active = None

        for line in mem_info:
            if total and active:
                break

            if "MemTotal:" in line:
                total = mem_format(line)
            if "Active:" in line:
                active = mem_format(line)

        if total and active:
            total, active = int(total), int(active)
            used = total - active
            percent = round(active / total * 100)

            if percent < 1:
                percent = "<1"

            return str(
                f"{round(used/1024)} / " f"{round(total/1024)}" f" MB ({percent}%)"
            )
        else:
            print("Error: could not parse ram usage")
            return None

    except Exception as e:
        print(f"Parse RAM Error: {e}")
        return None
