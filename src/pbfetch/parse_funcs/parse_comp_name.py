def parse_comp_name():
    file = "/sys/class/dmi/id"
    name = "/product_name"
    version = "/product_version"
    try:
        with open(file + name) as comp_name:
            name = comp_name.read().strip()

        with open(file + version) as comp_version:
            version = comp_version.read().strip()

        name = name + " " + version

        return name

    except Exception as e:
        print(e)
        return None
