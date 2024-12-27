def parse_hostname():
    file = "/etc/hostname"
    try:
        with open(file) as hostname:
            hostname = hostname.read()

        return hostname.strip()

    except Exception as e:
        print(f"Parse Host Error: {e}")
        return None
