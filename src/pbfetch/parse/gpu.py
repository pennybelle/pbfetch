from pbfetch.handle_error import error
from subprocess import Popen, PIPE
from re import sub


def command(input):
    input = Popen(
        input,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    input = str(input.communicate()[0])
    input = input[2 : len(input) - 3]

    return input


def parse_gpu():
    try:
        gpu_name = command("nvidia-smi --query-gpu=name --format=csv,noheader")

        return gpu_name.strip()

    except Exception:
        pass

    try:
        gpu_name = command("lspci | grep -i nvidia")

        if gpu_name:
            gpu_name = gpu_name.split(": ")[1]
            gpu_name = gpu_name.strip()
            return sub(r" \(.+\)$", "", gpu_name.strip())

    except Exception:
        pass

    try:
        gpu_name = command('eglinfo | grep "OpenGL compatibility profile renderer:"')
        # print(gpu_name)

        gpu_name = gpu_name.split("\\n")[2]
        # print(gpu_name)

        gpu_name = gpu_name.replace("OpenGL compatibility profile renderer: ", "")
        # print(gpu_name)

        return sub(r" \(.+\)$", "", gpu_name.strip())

    except Exception:
        pass

    try:
        gpu_name = Popen(
            'lspci | grep "VGA compatible controller:"',
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        gpu_name = str(gpu_name.communicate()[0])
        # print(gpu_name)

        gpu_name = gpu_name[2 : len(gpu_name) - 3]
        gpu_name = gpu_name.split("VGA compatible controller:")[1].strip()

        return sub(r" \(.+\)$", "", gpu_name.strip())

    except Exception as e:
        print(error(e, "GPU"))
        return None
