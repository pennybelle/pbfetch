# format each line so right side accommodates for stat len
def horizontal_formatter(fetch_data, key, stat):
    # split fetch string at each keyword (sequentially)
    fetch_data = fetch_data.split(str(key))

    # store lengths for reuse
    key_len = len(key)
    stat_len = len(stat)
    fetch_len = len(fetch_data)

    if key_len < stat_len and fetch_len != 1:
        # number of chars to delete
        diff = stat_len - key_len

        # remove chars following keyword
        for _ in range(diff):
            index = 0
            while index < diff and fetch_data[1][index] != " ":
                index += 1

            # TODO: remove only whitespace chars
            # (IT WORKS!!!!)(kinda...)
            # modified = [*fetch_data[1]]
            # del modified[index]
            # modified = "".join(modified)
            modified = fetch_data[1].replace(fetch_data[1][index], "", 1)
            # modified.pop(index)

            # debug
            # print(fetch_data[0], end="", flush="")
            # print(modified.rstrip())
            # time.sleep(DEBUG_DELAY)

            fetch_data[1] = modified

        # replaces second half with modified string
        fetch_data[1] = modified

        # fetch_data = str(stat).join(fetch_data)

    elif key_len > stat_len and fetch_len != 1:
        # number of chars to add
        diff = key_len - stat_len

        # adds whitespace following keyword
        modified = str(" " * diff) + fetch_data[1]

        # replaces second half with modified string
        fetch_data[1] = modified

        # # rejoin into str and replace keyword with value
        # fetch_data = str(stat).join(fetch_data)

    # rejoin into str and replace keyword with value
    fetch_data = str(stat).join(fetch_data)

    return fetch_data
