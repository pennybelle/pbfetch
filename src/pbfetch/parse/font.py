from pbfetch.handle_error import error
from subprocess import Popen, PIPE


def parse_font():
    try:
        font = Popen(
            "fc-match Monospace",
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        font = str(font.communicate()[0])
        font = font[3 : len(font) - 4]
        font = font.split('"')[1]

        if font:
            return font
        else:
            return "not found"

    except Exception:
        pass

    try:
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

    except Exception as e:
        print(error(e, "Font"))
        return None
