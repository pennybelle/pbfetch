import time


def parse_uptime():
    seconds = int(time.clock_gettime(time.CLOCK_BOOTTIME))

    # math for time formatting with day, hr, min, sec
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    fdays = "" if d == 0 else f"{d}d "
    fhours = "" if h == 0 else f"{h}h "
    fminutes = "" if m == 0 else f"{m}m "
    fsecs = "" if s == 0 else f"{s}s "

    return (fdays + fhours + fminutes + fsecs).rstrip()
