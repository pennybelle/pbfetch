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
        font = font[3:len(font) - 4]

        return font

    except Exception as e:
        print(f"Parse Terminal Font Error: {e}")
        return None