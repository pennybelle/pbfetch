from subprocess import run


def parse_cpu_temp():
    try:
        # check at most 30 times for each
        #   thermal_zone dir till cpu is found
        for i in range(30):
            data = run(
                [
                    rf"paste <(cat /sys/class/thermal/thermal_zone{i}/type) <(cat /sys/class/thermal/thermal_zone{i}/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'"
                ],  #  | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'
                shell=True,
                capture_output=True,
            ).stdout

            # return none if cpu isnt found
            if i == 29:
                return None

            # only return cpu temp
            data = str(data)
            if "x86_pkg_temp" in data:
                break
            elif "acpitz" in data:
                break

        # parse string for temp number
        cpu_temp = str(data)
        cpu_temp = " ".join(cpu_temp.split("\\"))
        cpu_temp = cpu_temp.split()[1]

        return round(float(cpu_temp))

    except Exception as e:
        print(e)
        return None
