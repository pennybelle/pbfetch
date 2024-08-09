import os


def parse_batt():
    full = None
    now = None
    try:
        path = os.path.join("/", "sys", "class", "power_supply", "BAT0")

        with open(os.path.join(path, "charge_full")) as full:
            full = int(full.read())
            print(full)

        with open(os.path.join(path, "charge_now")) as now:
            now = int(now.read())
            print(now)

        if full and now:
            charge = f"{(now / full) * 100:.2f}" + "%"
            print(charge)
            return charge

        return None

    except Exception as e:
        print(e)
        return None
