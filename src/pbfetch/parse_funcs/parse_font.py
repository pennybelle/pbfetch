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

        font = font.splitlines()
        
        for line in font[::-1]:
            if "8x16=y" in line:
                return "8x16"
            elif "8x8=y" in line:
                return "8x8"

    except Exception as e:
        print(f"Parse Font Error: {e}")
        return None
