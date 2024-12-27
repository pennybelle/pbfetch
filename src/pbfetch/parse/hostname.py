from pbfetch.handle_error import error


def parse_hostname():
    file = "/etc/hostname"
    try:
        with open(file) as hostname:
            hostname = hostname.read()

        return hostname.strip()

    except Exception as e:
        print(error(e, "Hostname"))
        return None
