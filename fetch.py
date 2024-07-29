import platform, socket, re, uuid, psutil

with open("logo.txt", "r") as logo:
    if logo:
        logo = logo.read()
    else:
        logo = "BAAAAAAAAAA"

# get longest line length of logo for stat formatting
longest_line = 0
for line in logo.splitlines():
    if len(line) > longest_line:
        longest_line = len(line)

stat_os = None

def os_parse():
    with open("/etc/os-release", "r") as content:
        if content:
            stat_os = content.read()
            stat_os = stat_os.split("=")
            # print(stat_os)

stat_arch = platform.architecture()
stat_release = platform.release()
stat_version = platform.version()
stat_machine = platform.machine()
stat_hostname = socket.gethostname()
stat_ip = socket.gethostbyname(stat_hostname)
stat_mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
stat_processor = platform.processor()
stat_ram = str(
    round(psutil.virtual_memory().total / (1024.0 ** 3))
) + " GB"
stat_platform = platform.platform()

stats = [
    stat_os,        # 0
    stat_arch,      # 1
    stat_release,   # 2
    stat_version,   # 3
    stat_machine,   # 4
    stat_hostname,  # 5
    # stat_ip,
    # stat_mac,
    stat_processor, # 6
    stat_ram,       # 7
]

# debug
for index, stat in enumerate(stats):
    print(f"{index}: {stat}")

# set loop length to either num of lines in logo or elements in stats array, whichever is more
logo_len = len(logo.splitlines())
stats_len = len(stats)
loop_len = logo_len if logo_len > stats_len else stats_len

# stats use a different index to handle empty lines in logo properly
stats_index = 0

# debug
empty_vars = []

# enumberate over length of logo or stats list (whichever is longer)
for index in range(loop_len):
    line = logo.splitlines()[index]

    # append whitespace to logo for formatting
    if len(line) < longest_line:
        line = line + " " * (longest_line - len(line))
    line = line + (" " * 3) # buffer

    # if logo line doesnt have content, continue to next line
    if len(line) == 0 or line.isspace():
        continue

    # same as print!("{line}"); followed by a flush
    print(line, end='', flush=True)

    # conditional prevents trying to pring more than stats list contains
    if stats_index >= len(stats):
        # just print a new line
        print()
    else:
        while stat is None and stats_index > loop_len:
            empty_vars.append(stat) # debug
            stats_index += 1
        # print stat line and then new line
        stat = stats[stats_index]
        print(stat)
        stats_index += 1
