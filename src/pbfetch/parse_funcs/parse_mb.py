from os import path


def parse_mb():
    file = path.join("sys", "class", "dmi", "id")
    try:
        if path.isdir(path.join(file, "board_name")) is not True:
            return "not found"

        with open(f"{file}/board_name") as mb:
            mb = mb.read().strip()

        if path.isdir(path.join(file, "board_vendor")) is not True:
            return mb

        with open(f"{file}/board_vendor") as v:
            v = v.read().strip()

        return f"{v} {mb}"

    except Exception as e:
        print(f"Parse Motherboard Error: {e}")
        return None
