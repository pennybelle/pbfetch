def parse_cpu_usage():
    file = "/proc/stat"
    try:
        data = None
        with open(file) as file:
            data = file.readline().split()
            data = [int(x) for x in data[1:8]]

        # print(data)

        user = data[0]
        nice = data[1]
        system = data[2]
        idle = data[3]
        iowait = data[4]
        irq = data[5]
        softirq = data[6]

        in_use = user + nice + system
        total = in_use + idle + iowait + irq + softirq

        return str(round((in_use / total) * 100)) + "%"

        # spline = line_parse()
        # print(spline)
        # total = int(spline[2])

        # in_use =

        # # one = int(spline[2])
        # two = int(spline[2])
        # # three = int(spline[4])
        # four = int(spline[4])
        # five = int(spline[5])

        # usage = f"{float((two + four) * 100 / (two + four + five)):.3g}"

        # if first_check > second_check:
        #     usage = ((first_check - second_check) / total) * 100
        # else:
        #     usage = ((second_check - first_check) / total) * 100

        # spline = line_parse()
        # u = int(spline[2])
        # t = int(spline[2]) + int(spline[4]) + int(spline[5])

        # time.sleep(1)

        # spline = line_parse()
        # u1 = int(spline[2])
        # t1 = int(spline[2]) + int(spline[4]) + int(spline[5])

        # return usage
        # return int((u - t) * 100 / (u1 - t1))

    except Exception as e:
        print(f"Parse CPU Usage Error: {e}")
        return None
