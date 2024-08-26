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

        return font

    except Exception as e:
        print(f"Parse Font Error: {e}")
        return None
