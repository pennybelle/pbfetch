def parse_uptime():
    # parse uptime from /proc/uptime
    with open("/proc/uptime", "r") as file:
        seconds = int(float(file.readline().split()[0]))

    # math for time formatting with day, hr, min, sec
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    # string formatting using calculated vals from above
    days = f"{d:d}d"
    hours = f"{h:d}h"
    mins = f"{m:d}m"
    secs = f"{s:d}s"
    uptime = ""

    # only join to uptime if uptime isnt empty
    # else replace empty uptime with new value
    def format_uptime(uptime, time):
        if uptime:
            uptime = " ".join([uptime, time])
        else:
            uptime = time

        return uptime

    # only show relevant data (ie: if day is 0, dont show day)
    if d > 0:
        uptime = format_uptime(uptime, days)

    if h > 0:
        uptime = format_uptime(uptime, hours)

    if seconds > 60 and m > 0:
        uptime = format_uptime(uptime, mins)

    if s > 0:
        uptime = format_uptime(uptime, secs)

    if uptime != "":
        return uptime
    else:
        return None
