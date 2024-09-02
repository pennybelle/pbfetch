from subprocess import Popen, PIPE


def parse_term_font():
    try:
        font = Popen(
            "gsettings get org.gnome.desktop.interface monospace-font-name",
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        font = str(font.communicate()[0])
        font = font[3 : len(font) - 4]

        if font:
            return font
        else:
            font = Popen(
                "zgrep FONT /proc/config.gz",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            font = str(font.communicate()[0])
            font = font[3 : len(font) - 4]

            font = font.split(r"\n")

            for line in font[::-1]:
                if "=y" in line:
                    return line[12 : len(line) - 2]

        return "not found"

    except Exception as e:
        print(f"Parse Terminal Font Error: {e}")
        return None
