from subprocess import Popen, PIPE


def parse_term_font():
    try:
        font = Popen(
            'gsettings get org.gnome.desktop.interface monospace-font-name',
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        font = str(font.communicate()[0])
        font = font[2:len(font) - 1]
        font = font.replace(r'\n', "")
        font = font.replace("'", "")

        return font

    except Exception as e:
        print(f"Parse Terminal Font Error: {e}")
        return None