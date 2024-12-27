from pbfetch.handle_error import error


def parse_kernel_release():
    file = "/proc/version"
    try:
        with open(file) as kernel:
            kernel = kernel.read()
            kernel = kernel.split(" ")[2]

        return kernel

    except Exception as e:
        print(error(e, "Kernel"))
        return None
