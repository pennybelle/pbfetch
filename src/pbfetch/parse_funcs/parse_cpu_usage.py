import time


def parse_cpu_usage():
    file = "/proc/stat"
    try:
        with open(file) as file:

            def get_cpu_stats():
                data = file.readline().split()
                return [int(x) for x in data[1:]]

            # spline = line_parse()
            # print(spline)
            # total = int(spline[2])

            first_check = get_cpu_stats()
            time.sleep(0.1)
            second_check = get_cpu_stats()

            deltas = [t2 - t1 for t1, t2 in zip(first_check, second_check)]

            total_time = sum(deltas)

            idle_time = deltas[3]

            active_time = total_time - idle_time

            usage = f"{(active_time / total_time) * 100:.2g}"

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

        return usage
        # return int((u - t) * 100 / (u1 - t1))

    except Exception as e:
        print(e)
        return None
