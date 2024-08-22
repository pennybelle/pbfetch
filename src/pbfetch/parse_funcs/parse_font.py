from subprocess import Popen, PIPE


def parse_font():
    try:
        font = Popen(
            'fc-match Monospace',
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        font = str(font.communicate()[0])
        font = font[2:len(font) - 1]
        font = font.replace(r'\n', "")
        font = font.replace("'", "")
        font = font.split('"')[1]

        return font

    except Exception as e:
        print(f"Parse Font Error: {e}")