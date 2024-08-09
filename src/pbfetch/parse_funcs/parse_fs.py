def parse_fs():
    file = "/etc/fstab"
    try:
        with open(file) as fstab:
            fstab = fstab.read()
            lines = fstab.splitlines()
            for line in lines:
                print(line)
                if "subvol=/@" in line:
                    print("found it")
                    file_system = line.split("/")[1]
                    file_system = file_system.split()[0]
                    return file_system

        return None

    except Exception as e:
        print(e)
        return None
