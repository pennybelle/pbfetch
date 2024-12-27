from os import path, getppid
from subprocess import check_output


def parse_shell():
    try:
        shell_pre_parse = path.realpath(f"/proc/{getppid()}/exe")
        shell_name = shell_pre_parse.split("/")[-1]
        shell_name = shell_name.split()[0]
        shell_version_pre_parse = str(
            check_output([f"{shell_name}", "--version"]).decode("utf-8")
        )
        if shell_name == "bash":
            shell_version = shell_version_pre_parse.split()[3]
        elif shell_name == "zsh":
            shell_version = shell_version_pre_parse.split()[1]
        else:
            return str(shell_name)

        return f"{shell_name} {shell_version}"

    except Exception as e:
        print(f"Parse Shell Error: {e}")
        return None
