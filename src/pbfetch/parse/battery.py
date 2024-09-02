from os import path


def parse_batt():
    # print("batt boop")
    full = None
    now = None
    try:
        for i in range(11):
            batt_path = path.join("/", "sys", "class", "power_supply", f"BAT{i}")

            if i == 10:
                return "not found"

            if path.exists(batt_path):
                break

        if path.exists(path.join(batt_path, "charge_full")):
            file_full = "charge_full"
        elif path.exists(path.join(batt_path, "energy_full")):
            file_full = "energy_full"

        if path.exists(path.join(batt_path, "charge_now")):
            file_now = "charge_now"
        elif path.exists(path.join(batt_path, "energy_now")):
            file_now = "energy_now"

        with open(path.join(batt_path, file_full)) as full:
            full = int(full.read())
            # print(full)

        with open(path.join(batt_path, file_now)) as now:
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
