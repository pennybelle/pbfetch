from subprocess import run


def parse():
    try:
        # priority sensor is inside cpu,
        #   secondary sensor (backup data) is
        #   beside the cpu socket.
        for sensor_type in ("x86_pkg_temp", "acpitz"):
            # check at most 30 times for each
            #   thermal_zone dir till cpu is found
            for j in range(30):
                data = run(
                    [
                        rf"paste <(cat /sys/class/thermal/thermal_zone{j}/type) <(cat /sys/class/thermal/thermal_zone{j}/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'"
                    ],  #  | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'
                    shell=True,
                    capture_output=True,
                ).stdout

                # return none if cpu isnt found
                if j == 29:
                    break

                # only return cpu temp
                data = str(data)
                if sensor_type in data:
                    # parse string for temp number
                    cpu_temp = str(data)
                    cpu_temp = " ".join(cpu_temp.split("\\"))
                    cpu_temp = cpu_temp.split()[1]

                    return round(float(cpu_temp))

        print("CPU Temp Error: CPU not found")
        return None

    except Exception as e:
        print(f"CPU Temp Error: {e}")
        return None
