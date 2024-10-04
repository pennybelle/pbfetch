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


"""
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@')}
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/.snapshots', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=260,subvol=/@.snapshots')}
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/var/log', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=258,subvol=/@log')}
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/var/cache/pacman/pkg', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=259,subvol=/@pkg')}
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/home', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=257,subvol=/@home')}
{'/dev/mapper/root': sdiskpart(device='/dev/mapper/root', mountpoint='/home', fstype='btrfs', opts='rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=257,subvol=/@home'), '/dev/nvme0n1p1': sdiskpart(device='/dev/nvme0n1p1', mountpoint='/boot', fstype='vfat', opts='rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro')}
"""
