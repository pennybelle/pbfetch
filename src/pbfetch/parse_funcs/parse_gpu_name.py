import subprocess


def parse_gpu():
    try:
        gpu_name = subprocess.Popen(
            'eglinfo | grep "OpenGL compatibility profile renderer:"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        gpu_name = str(gpu_name.communicate()[0])
        # print(gpu_name)
        gpu_name = gpu_name.split("'")[1]
        gpu_name = gpu_name.split("\\n")[0]
        gpu_name = gpu_name.replace("OpenGL compatibility profile renderer: ", "")

        return gpu_name

    except Exception as e:
        print(e)
        return None
