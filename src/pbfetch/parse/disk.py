from os import statvfs


def parse_disk():
    try:
        vfs = statvfs("/")
        total_disk_size_in_bytes = vfs.f_frsize * vfs.f_blocks
        total_disk_size_in_gb = total_disk_size_in_bytes / (1024.0**2) / 1024
        disk_free_space_gb = vfs.f_frsize * vfs.f_bfree / (1024.0**2) / 1024
        total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
        total_percent_used = round((total_disk_size_used / total_disk_size_in_gb) * 100)

        if total_percent_used < 1:
            total_percent_used = "<1"

        return (
            f"{total_disk_size_used:.2f} / "
            f"{total_disk_size_in_gb:.2f} GB "
            f"({total_percent_used}%)"
        )

    except Exception as e:
        print(f"Parse Disk Error: {e}")
        return None
