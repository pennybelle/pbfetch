def parse_mb():
    file = "/sys/class/dmi/id"
    try:
        with open(f"{file}/board_name") as mb:
            mb = mb.read().strip()

        with open(f"{file}/board_vendor") as v:
            v = v.read().strip()

        return f"{v} {mb}"

    except Exception as e:
        print(e)
        return None
