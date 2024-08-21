import subprocess


def parse():
    try:
        gpu_name = subprocess.Popen(
            'eglinfo | grep "OpenGL compatibility profile renderer:"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        gpu_name = str(gpu_name.communicate()[0])
        # print(gpu_name)

        gpu_name = gpu_name.split("\\n")[2]
        # print(gpu_name)

        gpu_name = gpu_name.replace("OpenGL compatibility profile renderer: ", "")
        # print(gpu_name)

        return gpu_name

    except Exception as e:
        print(f"GPU Parse Error: {e}")
        return None
