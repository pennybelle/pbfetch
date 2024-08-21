from os import readlink, getppid


def parse():
    return readlink("/proc/%d/exe" % getppid()).replace("/usr/bin/", "")
