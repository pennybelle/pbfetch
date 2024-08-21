# parse os name from /etc/os-release
def parse():
    with open("/etc/os-release", "r") as content:
        if content:
            stat_os = content.read()
            stat_os = stat_os.split("=")
            stat_os = stat_os[1].splitlines()[0].replace('"', "")
        else:
            stat_os = None

        return stat_os
