import subprocess

def parse_packages():
     stat_packages = f"{len(
        str(
            subprocess.check_output(["pacman", "-Q"])
        ).split(" ")
    )} (pacman)"
