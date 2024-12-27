from pbfetch.handle_error import error
from os import path


def parse_bios_type():
    # try:
    #     with open("/sys/class/dmi/id/bios_vendor") as vendor:
    #         vendor = vendor.read().strip()

    #     with open("/sys/class/dmi/id/bios_version") as version:
    #         version = version.read().strip()

    #     return f"{vendor} {version}"

    # except Exception:
    #     pass

    try:
        if path.isdir("/sys/firmware/efi") or path.exists(
            "/sys/firmware/acpi/tables/UEFI"
        ):
            bios_type = "UEFI"
        else:
            bios_type = "Legacy"

        vendor_path = "/sys/class/dmi/id/bios_vendor"
        if path.exists(vendor_path):
            with open(vendor_path) as vendor:
                vendor = vendor.read().strip()
                bios_type += f" {vendor}"

        vendor_version = "/sys/class/dmi/id/bios_version"
        if path.exists(vendor_version):
            with open(vendor_version) as version:
                version = version.read().strip()
                bios_type += f" {version}"

        # return f"{vendor} {version}"

        return bios_type

    except Exception as e:
        print(error(e, "Bios"))
        return None
