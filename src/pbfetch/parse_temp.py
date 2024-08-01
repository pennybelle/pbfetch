# parse & format temp from /sys/class/thermal/thermal_zone0/temp
def parse_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as temp:
        return round(int(temp.read()) / 1000)
