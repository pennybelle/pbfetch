import os


def parse_res():
    res_path = "/sys/class/drm"

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
                if os.path.isdir(f"{res_path}/card{i}-{display}-1") is not True:
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
