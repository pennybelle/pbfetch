import os


def parse_batt():
    full = None
    now = None
    try:
        path = os.path.join("/", "sys", "class", "power_supply", "BAT0")

        if os.path.exists(path) is not True:
            return "no battery"

        if os.path.exists(os.path.join(path, "charge_full")):
            file_full = "charge_full"
        elif os.path.exists(os.path.join(path, "energy_full")):
            file_full = "energy_full"

        if os.path.exists(os.path.join(path, "charge_now")):
            file_now = "charge_now"
        elif os.path.exists(os.path.join(path, "energy_now")):
            file_now = "energy_now"

        with open(os.path.join(path, file_full)) as full:
            full = int(full.read())
            # print(full)

        with open(os.path.join(path, file_now)) as now:
            now = int(now.read())
            # print(now)

        # dont ask ok... just........ dont ask.
        if now > full:
            full = now

        if full and now:
            charge = str(round((now / full) * 100)) + "%"
            # print(charge)
            return charge

        return None

    except Exception as e:
        print(e)
        return None
