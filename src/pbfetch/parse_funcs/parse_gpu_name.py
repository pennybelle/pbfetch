from subprocess import check_output


def vulkan():
    try:
        gpu_info = check_output(["vulkaninfo | grep GPU id"])
        # print(gpu_info)
        return gpu_info

    except Exception:
        print("vulkan didnt work")
        return None


def glxinfo():
    try:
        gpu_info = check_output(["glxinfo"])
        # print(gpu_info)
        gpu_info = gpu_info.split("Device: ")[1]
        gpu_name = gpu_info.splitlines()[0].strip()
        gpu_name = gpu_name.lower().replace("mesa", "").strip().title()
        return gpu_info

    except Exception:
        print("glxinfo didnt work")
        return None


def parse_gpu():
    if vulkan():
        print("first")
        gpu_name = vulkan()

    elif glxinfo():
        print("second")
        gpu_name = glxinfo()

    else:
        return None

    return gpu_name
    # return gpu_info
