from subprocess import run


def parse_cpu_temp():
    for i in range(9):
        cpu_temp = run(
            [
                rf"paste <(cat /sys/class/thermal/thermal_zone{i}/type) <(cat /sys/class/thermal/thermal_zone{i}/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'"
            ],  #  | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'
            shell=True,
            capture_output=True,
        ).stdout
        if "BAT" not in str(cpu_temp):
            break

    cpu_temp = str(cpu_temp)
    cpu_temp = " ".join(cpu_temp.split("\\"))
    cpu_temp = cpu_temp.split()[1]

    return round(float(cpu_temp))
