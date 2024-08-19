import os


def parse_res():
    try:
        path = "/sys/class/drm"

        for i in range(10):
            if os.path.isdir(f"{path}/card{i}-LVDS-1") is not True:
                continue

            with open(f"{path}/card{i}-LVDS-1/modes") as file:
                data = file.read()
                return str(data).strip()

        print("Resolution Error: LVDS not supported")
        return None

    except Exception as e:
        print(f"Resolution Error: {e}")
        return None
