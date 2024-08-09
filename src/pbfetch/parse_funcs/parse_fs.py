def parse_fs():
    file = "/proc/cmdline"
    try:
        with open(file) as cmdline:
            cmdline = cmdline.read()
            pieces = cmdline.split(" ")
            file_system = None
            for piece in reversed(pieces):
                if "rootfstype" in piece:
                    filesystem = piece.replace("rootfstype=", "")

        return filesystem

    except Exception as e:
        print(e)
        return None
