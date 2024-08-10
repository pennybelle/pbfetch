import subprocess


def parse_res():
    res = str(subprocess.check_output(["xrandr"]).decode("utf-8"))
    res = res.splitlines()[0]
    res = res.split(",")[1]
    res = "".join(res.replace("current", "").split())

    return res
