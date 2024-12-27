from pbfetch.handle_error import error
from subprocess import Popen, PIPE


def parse_weather():
    try:
        weather = Popen(
            """echo $(curl wttr.in/?0?q?T | awk '/°(C|F)/ {printf $(NF-1) $(NF) " ("a")"} /,/ {a=$0}')""",
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        weather = str(weather.communicate()[0])
        weather = weather[2 : len(weather) - 3]
        weather = weather.replace(r"\xc2\xb0", "°")

        return weather

    except Exception as e:
        print(error(e, "Weather"))
        return None
