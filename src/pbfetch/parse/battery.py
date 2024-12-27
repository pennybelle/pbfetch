from os import path
from subprocess import run


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

        charge_path = path.join("/", "sys", "class", "power_supply")

        charge_file = run(["ls", charge_path], capture_output=True).stdout
        charge_file = charge_file.decode().split()
        ac_dir = None

        for i in charge_file:
            if i.startswith("A"):
                ac_dir = i
                break

        if ac_dir:
            with open(path.join(charge_path, ac_dir, "online")) as is_charging:
                is_charging = int(is_charging.read())

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
            charge = f"{round((now / full) * 100)}%"
            if ac_dir:
                if is_charging:
                    charge = f"{charge} (AC Connected)"
                else:
                    charge = f"{charge} (Discharging)"
            # print(charge)
            return charge

        return None

    except Exception as e:
        print(f"Parse Battery Error: {e}")
        return None
