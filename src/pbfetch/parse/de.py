from sys import platform
from os import environ
from subprocess import Popen, PIPE
from re import search

# i pulled this code from
#   https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment


def parse_de():
    de = None
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if platform in ["win32", "cygwin"]:
        return "windows"
    elif platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = environ.get("DESKTOP_SESSION")
        if (
            desktop_session is not None
        ):  # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in [
                "gnome",
                "unity",
                "cinnamon",
                "mate",
                "xfce4",
                "lxde",
                "fluxbox",
                "blackbox",
                "openbox",
                "icewm",
                "jwm",
                "afterstep",
                "trinity",
                "kde",
            ]:
                if desktop_session == "kde":
                    de = desktop_session
                else:
                    return desktop_session
            ## Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntustudio"):
                de = "kde"
            elif desktop_session.startswith("ubuntu"):
                return "gnome"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                de = "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
        if environ.get("KDE_FULL_SESSION") == "true":
            de = "kde"
        elif environ.get("GNOME_DESKTOP_SESSION_ID"):
            if "deprecated" not in environ.get("GNOME_DESKTOP_SESSION_ID"):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif is_running("xfce-mcs-manage"):
            return "xfce4"
        elif is_running("ksmserver"):
            de = "kde"

        if de:
            plasma_version = Popen(
                "plasmashell --version",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            plasma_version = str(plasma_version.communicate()[0])
            plasma_version = plasma_version[2 : len(plasma_version) - 3]
            plasma_version = plasma_version.replace("plasmashell", "").strip()

            if plasma_version:
                return f"{de} plasma {plasma_version}"

            return de

    return "not found/supported"


def is_running(process):
    # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = Popen(["ps", "axw"], stdout=PIPE)
    except Exception as _:  # Windows
        s = Popen(["tasklist", "/v"], stdout=PIPE)
    for x in s.stdout:
        x = str(x)
        if search(process, x):
            return True
    return False
