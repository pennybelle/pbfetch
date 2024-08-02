def parse_hostname():
    file = "/etc/hostname"
    try:
        with open(file) as hostname:
            hostname = hostname.read()

        return hostname.strip()

    except Exception as e:
        print(e)
        return None
