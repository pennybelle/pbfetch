import subprocess


def parse_res():
    try:
        res = subprocess.Popen(
            "xdpyinfo | grep dimensions",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        res = res.communicate()[0]
        # print(res)
        res = str(res)
        res = res.split()
        res = str(res[2])

        return res

    except Exception as e:
        print(e)
        return None
