from pbfetch.handle_error import error
from subprocess import run
from os import path


def parse_cpu_temp():
    dir = "/sys/class/thermal/thermal_zone"
    try:
        # priority sensor is inside cpu,
        #   secondary sensor (backup data) is
        #   beside the cpu socket.
        for sensor_type in ("x86_pkg_temp", "acpitz"):
            # check at most 30 times for each
            #   thermal_zone dir till cpu is found
            for j in range(30):
                # check for valid thermal zone
                if path.isdir(f"{dir}{j}") is not True:
                    continue

                # get thermal zone type and temp readout
                data = run(
                    [rf"paste <(cat {dir}{j}/type) <(cat {dir}{j}/temp)"],
                    shell=True,
                    capture_output=True,
                ).stdout  # | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'

                # parse output
                data = data.decode()
                data = str(data).replace("\t", " ").replace("\n", " ")

                # only return temp if thermal zone is valid type
                if sensor_type in data:
                    # parse string for temp number
                    cpu_temp = data.split(" ")[1]

                    return round(float(cpu_temp)) // 1000

        return None

    except Exception as e:
        print(error(e, "CPU Temp"))
        return "Error"
