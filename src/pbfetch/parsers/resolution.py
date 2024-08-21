import os


def parse():
    try:
        display_types = ["LVDS", "eDP"]

        path = "/sys/class/drm"

        for display in display_types:
            for i in range(10):
                if os.path.isdir(f"{path}/card{i}-{display}-1") is not True:
                    continue

                with open(f"{path}/card{i}-{display}-1/modes") as file:
                    data = file.read()
                    return str(data).strip()

        print("Resolution Error: LVDS and eDP not found")
        return None

    except Exception as e:
        print(f"Resolution Error: {e}")
        return None
