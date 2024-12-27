from pbfetch.handle_error import error


# parse & format temp from /sys/class/thermal/thermal_zone0/temp
def parse_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as temp:
            return round(int(temp.read()) / 1000)

    except Exception as e:
        print(error(e, "Temp"))
        return None
