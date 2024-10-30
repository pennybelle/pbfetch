from os import path
from subprocess import Popen, PIPE, run

import tkinter as tk


def command(input, index):
    try:
        output = Popen(
            input,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        output = str(output.communicate()[index])
        output = output[2 : len(output) - 1]

        return output

    except Exception:
        pass


def parse_res():
    try:
        root = tk.Tk()

        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        res = f"{w}x{h}"
        if res and w and h:
            return res
        else:
            pass

    except Exception:
        pass

    # try:
    #     res = command("screenresolution get 2>&1", 0)

    #     return res

    # except Exception:
    #     # print("screenresolution failed")
    #     pass

    try:
        res = command("system_profiler SPDisplaysDataType", 0)

        if res:
            return res
        else:
            pass

    except Exception:
        # print("system_profiler failed")
        pass

    try:
        res = command(
            """PlistBuddy -c "Print DisplayAnyUserSets:0:0:Resolution" /Library/Preferences/com.apple.windowserver.plist""",
            0,
        )

        if res:
            return res
        else:
            pass

    except Exception:
        # print("PlistBuddy failed")
        pass

    try:
        h = command(
            """wmic path Win32_VideoController get CurrentHorizontalResolution""", 0
        )
        w = command(
            """wmic path Win32_VideoController get CurrentVerticalResolution)""", 0
        )

        res = f"{w}x{h}"

        if res and w and h:
            return res
        else:
            pass

    except Exception:
        # print("wmic failed")
        pass

    try:
        res = command("screenmode", 0)

        if res:
            return res
        else:
            pass

    except Exception:
        # print("screenmode failed")
        pass

    try:
        res = command("xrandr --nograb --current", 0)

        if res:
            return res
        else:
            pass

    except Exception:
        # print("xrandr failed")
        pass

    try:
        res = command("xwininfo -root", 0)

        if res:
            return res
        else:
            pass

    except Exception:
        pass

    try:
        res = command("xdpyinfo", 0)

        if res:
            return res
        else:
            pass

    except Exception:
        # print("xdpyinfo failed")
        pass

    try:
        font_size = command("setfont -v", 1)
        font_size = font_size.split("font from file")[0]
        font_size = font_size.split()[-1]
        font_x, font_y = tuple(map(int, font_size.split("x")))
        term_size = command("stty size", 0).replace(r"\n", "")
        y, x = tuple(map(int, term_size.split()))

        res_x = x * font_x
        res_y = y * font_y

        res = f"{res_x}x{res_y}"

        if res and res_x and res_y:
            return res
        else:
            pass

    except Exception:
        pass

    # print("all failed, falling back to eDP or LVDS")

    # try:
    #     cards = run(["ls", "-l", res_path], capture_output=True).stdout
    #     cards = str(cards)[2:len(cards)-1]
    #     cards = cards.split("\\n")
    #     print(cards)
    #     for index, card in enumerate(cards):
    #         if "card" not in card:
    #             # print("card skipped")
    #             continue

    #         card = card.split(" ")
    #         card = list(filter(None, card))
    #         card = card[8]
    #         print(card)
    #         edid_path = os.path.join(res_path, card, "edid")
    #         if os.path.exists(edid_path) is not True:
    #             print("no path")
    #             continue

    #         with open(edid_path, mode="rb") as edid:
    #             byte = edid.read()
    #             while byte != b"":
    #                 edid = edid.read()

    #         print(edid_path, edid)
    #         if edid == "b''":
    #             continue
    #     print(edid)
    #     return

    # except AttributeError:

    # except Exception as e:
    #     print(e)

    res_path = "/sys/class/drm"

    try:
        display_types = ["LVDS", "eDP"]

        for display in display_types:
            for i in range(10):
                if path.isdir(f"{res_path}/card{i}-{display}-1") is not True:
                    continue

                with open(f"{res_path}/card{i}-{display}-1/modes") as file:
                    data = file.read()
                    data = data.splitlines()[0]
                    return str(data).strip()

        print("Resolution Error: LVDS and eDP not found")
        return None

    except Exception as e:
        print(f"Resolution Error: {e}")
        return None
