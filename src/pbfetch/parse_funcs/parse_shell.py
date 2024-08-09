from os import readlink, getppid


def parse_shell():
    return readlink("/proc/%d/exe" % getppid()).replace("/usr/bin/", "")
