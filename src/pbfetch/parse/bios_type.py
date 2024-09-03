import os


def parse_bios_type():
    try:
        if os.path.isdir("/sys/firmware/efi") or os.path.exists(
            "/sys/firmware/acpi/tables/UEFI"
        ):
            bios_type = "UEFI"
        else:
            bios_type = "Legacy"

        return bios_type

    except Exception as e:
        print(f"Bios Parse Error: {e}")
        return None
