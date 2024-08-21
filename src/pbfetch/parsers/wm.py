from subprocess import run


def parse():
    managers = {
        "Hyprland": "Hyprland",
        "kwin": "kwin",
        "river": "river",
        "sway": "sway",
        "labwc": "labwc",
        "anvil": "anvil",
        "cosmic": "cosmic",
        "mirace": "miracle",
        "mutter": "mutter",
        "theseus": "theseus",
        "wayfire": "wayfire",
        "weston": "weston",
        "cage": "cage",
        "gamescope": "gamescope",
        "qtile": "qtile",
        "niri": "niri",
        "swayfx": "swayfx",
    }

    try:
        for manager in managers.keys():
            output = run(["pgrep", "-l", manager], capture_output=True).stdout
            output = str(output)
            # print(output)

            if output and manager in output:
                return managers[manager]

        return "not supported yet"

    except Exception as e:
        print(e)
        return None
