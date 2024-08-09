def parse_mb():
    file = "/sys/class/dmi/id/board_name"
    try:
        with open(file) as mb:
            mb = mb.read()

        return str(mb).strip()

    except Exception as e:
        print(e)
        return None
