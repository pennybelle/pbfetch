from pbfetch.handle_error import error
from subprocess import Popen, PIPE


def package_query(command):
    package_manager = command.split()[0]
    query_output = Popen(
        command,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    query_output = query_output.communicate()[0]

    # convert byte object to string for parsee
    query_output = str(query_output)

    if query_output == "b''":
        return None

    # remove irrelevent data
    query_output = query_output.replace("/usr/lib", "")
    query_output = query_output.replace(r"\xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80", "")
    query_output = query_output.replace(r"\xe2\x94\x94\xe2\x94\x80\xe2\x94\x80", "")
    # print(query_output)

    # remove artifacts from output
    query_output = query_output[2 : len(query_output) - 1]

    # split lines to count packages
    query_output = query_output.split("\\n")

    # filter out empty strings
    # TODO: replace this with list comprehension
    query_output = list(filter(None, query_output))

    # length of remaining list == num of packages
    package_count = len(query_output)

    return f"{package_count} ({package_manager})"


def parse_packages():
    try:
        managers = [
            package_query("pacman -Q"),
            package_query("flatpak list"),
            package_query("apk info -e -a"),
            # package_query("npm list -g"),
        ]

        return " ".join(filter(None, managers))

    except Exception as e:
        print(error(e, "Package Manager"))
        return None
