from pbfetch.handle_error import error
from time import clock_gettime, CLOCK_BOOTTIME


def parse_uptime():
    try:
        seconds = int(clock_gettime(int(CLOCK_BOOTTIME)))

        # math for time formatting with day, hr, min, sec
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        fdays = f"{d}d " if d > 0 else ""
        fhours = f"{h}h " if h > 0 else ""
        fminutes = f"{m}m " if m > 0 else ""
        fsecs = f"{s}s " if s > 0 else ""

        return (fdays + fhours + fminutes + fsecs).rstrip()

    except Exception as e:
        print(error(e, "Uptime"))
        return None
