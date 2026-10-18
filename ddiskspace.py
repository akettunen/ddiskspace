import os
import sys

#customize

#default customized
ASCII_ART = r"""
    __     __ __         __
.--|  |.--|  |__|.-----.|  |--.-----.-----.---.-.----.-----.
|  _  ||  _  |  ||__ --||    <|__ --|  _  |  _  |  __|  -__|
|_____||_____|__||_____||__|__|_____|   __|___._|____|_____|
                                    |__|"""
#ASCII_COLOR = logo color
#LABEL_COLOR = Total, Used, Free
#VALUE_COLOR = the values the tool gives
ASCII_COLOR = "\033[38;2;202;1;71m"    #ruby red (default)
LABEL_COLOR = "\033[38;2;202;1;71m"  # ruby red (default)
VALUE_COLOR = "\033[92m"  # green (default)
RESET = "\033[0m"
#customize ends here!


def format_bytes(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def usage_windows():
    import ctypes
    k = ctypes.windll.kernel32
    k.SetErrorMode(1)  # no popups for empty drives

    # enable ANSI colors (much faster than os.system(""))
    h = k.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    if k.GetConsoleMode(h, ctypes.byref(mode)):
        k.SetConsoleMode(h, mode.value | 4)

    total = free = 0
    mask = k.GetLogicalDrives()
    avail, tot, fr = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
    for i in range(26):
        if mask & (1 << i):
            root = chr(65 + i) + ":\\"
            # 2=removable, 3=fixed, 4=network
            if k.GetDriveTypeW(root) in (2, 3, 4):
                if k.GetDiskFreeSpaceExW(root, ctypes.byref(avail), ctypes.byref(tot), ctypes.byref(fr)):
                    total += tot.value
                    free += fr.value
    return total, total - free, free


REAL_FS = {
    "ext2", "ext3", "ext4", "xfs", "btrfs", "zfs", "f2fs", "vfat", "exfat",
    "ntfs", "ntfs3", "fuseblk", "nfs", "nfs4", "cifs", "smb3",
}


def usage_linux():
    total = used = free = 0
    seen = set()
    with open("/proc/mounts") as f:
        for line in f:
            p = line.split()
            if len(p) < 3 or p[2] not in REAL_FS or p[0] in seen:
                continue
            try:
                s = os.statvfs(p[1].replace("\\040", " "))
            except OSError:
                continue
            seen.add(p[0])
            fr = s.f_frsize
            total += s.f_blocks * fr
            used += (s.f_blocks - s.f_bfree) * fr
            free += s.f_bavail * fr
    return total, used, free


def usage_macos():
    import re
    import subprocess
    skip = ("/System/Volumes/VM", "/System/Volumes/Preboot", "/System/Volumes/Update",
            "/System/Volumes/xarts", "/System/Volumes/iSCPreboot", "/System/Volumes/Hardware")
    out = subprocess.run(["mount"], capture_output=True, text=True).stdout
    total = used = free = 0
    seen = set()
    for line in out.splitlines():
        m = re.match(r"^(/dev/\S+) on (.+) \(", line)
        if not m or m.group(1) in seen or m.group(2).startswith(skip):
            continue
        try:
            s = os.statvfs(m.group(2))
        except OSError:
            continue
        seen.add(m.group(1))
        fr = s.f_frsize
        total += s.f_blocks * fr
        used += (s.f_blocks - s.f_bfree) * fr
        free += s.f_bavail * fr
    return total, used, free

#usage

def main():
    if sys.platform == "win32":
        total, used, free = usage_windows()
    elif sys.platform == "darwin":
        total, used, free = usage_macos()
    elif sys.platform.startswith("linux"):
        total, used, free = usage_linux()
    else:
        raise RuntimeError(f"Unsupported OS: {sys.platform}")

    lines = [
        f"{ASCII_COLOR}{ASCII_ART}{RESET}",
        f"  {LABEL_COLOR}Total:{RESET} {VALUE_COLOR}{format_bytes(total)}{RESET}",
    ]
    if total:
        lines.append(f"  {LABEL_COLOR}Used:{RESET}  {VALUE_COLOR}{format_bytes(used)} ({used / total * 100:.1f}%){RESET}")
    lines.append(f"  {LABEL_COLOR}Free:{RESET}  {VALUE_COLOR}{format_bytes(free)}{RESET}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
