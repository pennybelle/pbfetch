import platform, socket, re, uuid, psutil, os, subprocess

with open("config.conf", "r") as config:
    content = config.read()
    if content:
        fetch = content
    else:
        print("You must insert something in the config!")
        exit()

def get_uptime():
    with open("/proc/uptime", "r") as file:
        seconds = int(float(file.readline().split()[0]))
    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    uptime = ""
    # TODO: use "".join() to better format spaces
    # uptime += f"{d:d}:"
    # uptime += f"{h%24:d}:"
    uptime += f"{h:02d}h, "
    uptime += f"{m:02d}m, "
    uptime += f"{s:02d}s"

    if uptime != "":
        return uptime
    else:
        return None

def os_parse():
    with open("/etc/os-release", "r") as content:
        if content:
            stat_os = content.read()
            stat_os = stat_os.split("=")
            stat_os = stat_os[1].split("\n")[0].replace('"', "")
        else:
            stat_os = None
    
        return stat_os

stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
stat_os = f"{os_parse()}"
stat_arch = f"{platform.machine()}"
stat_kernel = f"{platform.release()}"
stat_version = platform.version()
stat_ram = str(
    round(psutil.virtual_memory().total / (1024.0 ** 3))
) + " GB"
stat_uptime = f"{get_uptime()}"
stat_packages = f"{len(str(subprocess.check_output(["pacman", "-Q"])).split(" "))} (pacman)"
stat_machine = platform.machine()

stats = {
    "HOSTNAME": stat_hostname,
    "OPERATINGSYSTEM": stat_os,
    "ARCHITECTURE": stat_arch,
    "KERNEL": stat_kernel,
    "MEMORY": stat_ram,
    "UPTIME": stat_uptime,
    "PACKAGES": stat_packages,
    "MACHINE": stat_machine,
}

# def get_longest_stat_length(stats):
#     return max(len(str(stat)) for stat in stats)
# print(get_longest_stat_length(stats))

# for stat in stats.items():
#     pass

def replaceKeyword(template, keyword, replaceText):
    # Split the string on the word
    splitTemplate = template.split(keyword, 1)

    # Make sure the string was actually split
    if len(splitTemplate) == 1:
        return template
    
    # Measure the length of the second element in the split
    beforeStripLength = len(splitTemplate[1])

    # Remove the whitespace of the second element in the split
    splitTemplate[1] = splitTemplate[1].lstrip()

    # Measure the length after stripping :3 to figure out how
    #   many whitespaces we removed
    afterStripLength = len(splitTemplate[1])

    # Use those values to calculate the whitespaces
    whitespaceCount = beforeStripLength - afterStripLength;

    # Figure out the max length the replacement can be
    keywordLength = len(keyword)
    maxAllowedLength = keywordLength + whitespaceCount;

    # Store the length of what we are using to replace it
    replaceTextLength = len(replaceText)

    # Make sure our replaceText isn't too long
    if replaceTextLength > maxAllowedLength:
        replaceText = replaceText[:maxAllowedLength]

    # Pad replaceText with spaces to match the whitespace we removed
    replaceText = replaceText.ljust(maxAllowedLength, ' ')

    return splitTemplate[0] + replaceText + splitTemplate[1]

# catch and release comments using # notation
for line in fetch.split("\n"):
    regex_match = re.search("#.*$", line)
    if regex_match:
        fetch = fetch.replace(regex_match.group(), "")

for keyword in stats.keys():
    stat = stats[keyword]

    replaceKeyword(fetch, keyword, stat)

    # fetch = fetch.split(keyword)

    # keyword_len = len(keyword)
    # stat_len = len(stat)
    # fetch_len = len(fetch)
    # print(fetch) # debug

    # if keyword_len > stat_len and fetch_len != 1:
    #     diff = keyword_len - stat_len # number of chars to del
    #     modified = fetch[1][diff:] # remove chars following keyword
    #     fetch[1] = modified # replaces second half with modified string
    # elif keyword_len < stat_len and fetch_len != 1:
    #     modifier = stat_len - keyword_len
    #     modified = str(" " * modifier) + fetch[1]
    #     fetch[1] = modified
    #     # stat += " " * (len(stat) - len(keyword)) # insert whitespace

    # fetch = str(stat).join(fetch) # rejoin into str 


print(fetch.strip())