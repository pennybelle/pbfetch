from pbfetch.handle_error import error
from subprocess import Popen, PIPE


def parse_theme():
    try:
        theme = Popen(
            "gsettings get org.gnome.desktop.interface gtk-theme",
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        theme = str(theme.communicate()[0])
        theme = theme[2 : len(theme) - 3]
        theme = theme.replace("'", "")

        if theme:
            return theme
        else:
            return "not found/supported"

    except Exception as e:
        print(error(e, "Theme"))
        return None
