from pbfetch.handle_error import error


# parse os name from /etc/os-release
def parse_os():
    try:
        with open("/etc/os-release", "r") as content:
            if content:
                stat_os = content.read()
                stat_os = stat_os.split("=")
                stat_os = stat_os[1].splitlines()[0].replace('"', "")
            else:
                stat_os = None

            return stat_os

    except Exception as e:
        print(error(e, "OS"))
        return None
