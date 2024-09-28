from os import path
from subprocess import Popen, PIPE

import tkinter as tk


def command(input):
    output = Popen(
        input,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    output = str(output.communicate()[0])[2 : len(output) - 1]

    return output


def parse_res():
    try:
        root = tk.Tk()

        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        return f"{w}x{h}"

    except Exception:
        pass

    try:
        res = command("screenresolution get 2>&1")

        return res

    except Exception:
        # print("screenresolution failed")
        pass

    try:
        res = command("system_profiler SPDisplaysDataType")

        return res

    except Exception:
        # print("system_profiler failed")
        pass

    try:
        res = command(
            """PlistBuddy -c "Print DisplayAnyUserSets:0:0:Resolution" /Library/Preferences/com.apple.windowserver.plist"""
        )

        return res

    except Exception:
        # print("PlistBuddy failed")
        pass

    try:
        h = command(
            """wmic path Win32_VideoController get CurrentHorizontalResolution"""
        )
        w = command(
            """wmic path Win32_VideoController get CurrentVerticalResolution)"""
        )

        res = f"{w}x{h}"

        return res

    except Exception:
        # print("wmic failed")
        pass

    try:
        res = command("screenmode")

        return res

    except Exception:
        # print("screenmode failed")
        pass

    try:
        res = command("xrandr --nograb --current")

        return res

    except Exception:
        # print("xrandr failed")
        pass

    try:
        res = command("xwininfo -root")

        return res

    except Exception:
        pass

    try:
        res = command("xdpyinfo")

        return res

    except Exception:
        # print("xdpyinfo failed")
        pass

    res_path = "/sys/class/drm"

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
