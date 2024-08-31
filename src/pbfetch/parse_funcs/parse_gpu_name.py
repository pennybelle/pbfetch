from subprocess import Popen, PIPE


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
        gpu_name = command("lspci | grep -i nvidia")

        if gpu_name:
            gpu_name = gpu_name.split(": ")[1]
            gpu_name = gpu_name.strip()
            return gpu_name

    except Exception:
        pass

    try:
        gpu_name = command('eglinfo | grep "OpenGL compatibility profile renderer:"')
        # print(gpu_name)

        gpu_name = gpu_name.split("\\n")[2]
        # print(gpu_name)

        gpu_name = gpu_name.replace("OpenGL compatibility profile renderer: ", "")
        # print(gpu_name)

        return gpu_name

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

        return gpu_name

    except Exception as e:
        print(f"GPU Parse Error: {e}")
        return None
