from psutil import disk_partitions


def parse_fs():
    try:
        partitions = disk_partitions()
        disks = {}
        for disk in partitions:
            disks[disk.mountpoint] = disk.fstype

        values = [item for item in disks.values()]
        if len(values) == 1:
            fs = values[0]
            return fs

        elif "/" in disks.keys():
            fs = disks["/"]
            return fs

    except Exception:
        pass

    file = "/etc/fstab"
    try:
        with open(file) as fstab:
            fstab = fstab.read()
            lines = fstab.splitlines()
            for line in lines:
                if "/ " in line:
                    file_system = line.split("/")[1]
                    file_system = file_system.split()[0]
                    return file_system

        return "not found"

    except Exception as e:
        print(f"Parse Filesystem Error: {e}")
        return None
