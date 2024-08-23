from subprocess import Popen, PIPE


def parse_theme():
    try:
        theme = Popen(
            'gsettings get org.gnome.desktop.interface gtk-theme',
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        theme = str(theme.communicate()[0])
        theme = theme[2:len(theme) - 3]
        theme = theme.replace("'", "")

        return theme

    except Exception as e:
        print(f"Parse Theme Error: {e}")
        return None