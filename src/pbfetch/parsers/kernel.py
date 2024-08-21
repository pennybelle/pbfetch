def parse():
    file = "/proc/version"
    try:
        with open(file) as kernel:
            kernel = kernel.read()
            kernel = kernel.split(" ")[2]

        return kernel

    except Exception as e:
        print(e)
        return None
