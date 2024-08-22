from os import path, getppid
from subprocess import check_output


def parse_shell():
    shell_pre_parse = path.realpath(f"/proc/{getppid()}/exe")
    shell_name = shell_pre_parse.split("/")[-1]
    shell_version_pre_parse = str(
        check_output([f"{shell_name}", "--version"]).decode("utf-8")
    )
    if shell_name == "zsh":
        shell_version = shell_version_pre_parse.split()[1]
    elif shell_name == "bash":
        shell_version = shell_version_pre_parse.split()[3]
    else:
        return "not supported yet"

    return f"{shell_name} {shell_version}"
