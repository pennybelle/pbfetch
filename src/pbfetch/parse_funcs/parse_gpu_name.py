from subprocess import check_output


def parse_gpu():
    gpu_info = check_output(["glxinfo"]).decode("utf-8")
    gpu_info = gpu_info.split("Device: ")[1]
    gpu_name = gpu_info.splitlines()[0].strip()
    gpu_name = gpu_name.replace("Mesa", "").replace("mesa", "").strip()

    return gpu_name
