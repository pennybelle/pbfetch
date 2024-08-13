from subprocess import run


def parse_wm():
    managers = {"Hyprland": "Hyprland", "kwin": "kwin"}

    # this runs twice, idk why
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
