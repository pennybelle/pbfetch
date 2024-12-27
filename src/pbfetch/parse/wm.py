from pbfetch.handle_error import error
from subprocess import run


def parse_wm():
    managers = [
        "kwin",
        "mutter",
        "weston",
        "qtile",
        "swayfx",
        "metacity",
        "wayfire",
        "river",
        "sway",
        "labwc",
        "anvil",
        "cosmic",
        "mirace",
        "theseus",
        "cage",
        "gamescope",
        "niri",
        "gdm",
        "Hyprland",
    ]

    try:
        for manager in managers:
            output = run(["pgrep", "-l", manager], capture_output=True).stdout
            output = output.decode()
            # print(output)

            if output and manager in output:
                session_type = run(
                    ["echo $XDG_SESSION_TYPE"],
                    shell=True,
                    capture_output=True,
                ).stdout

                # parse output
                session_type = session_type.decode().strip()

                if session_type:
                    return f"{manager} ({session_type})"

                return manager

        return "not found/supported"

    except Exception as e:
        print(error(e, "Window Manager"))
        return None
