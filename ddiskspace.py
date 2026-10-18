import ctypes
import os
import platform
import re
import shutil
import subprocess

from customize import ASCII_ART, ART_COLOR, LABEL_COLOR, VALUE_COLOR, RESET  # <-- import here

os.system("")  # enables ANSI colors on older Windows consoles

def format_bytes(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"

# ---------- Find the drives/mount points per OS ----------

def get_windows_drives():
    kernel32 = ctypes.windll.kernel32
    drives = []
    bitmask = kernel32.GetLogicalDrives()
    for i in range(26):
        if bitmask & (1 << i):
            root = f"{chr(65 + i)}:\\"
            drive_type = kernel32.GetDriveTypeW(root)
            if drive_type in (2, 3, 4):
                drives.append((root, root, {2: "removable", 3: "fixed", 4: "network"}[drive_type]))
    return drives

REAL_LINUX_FS = {
    "ext2", "ext3", "ext4", "xfs", "btrfs", "zfs", "f2fs", "vfat", "exfat",
    "ntfs", "ntfs3", "fuseblk", "nfs", "nfs4", "cifs", "smb3",
}

def get_linux_drives():
    drives = []
    with open("/proc/mounts") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            device, mountpoint, fstype = parts[0], parts[1], parts[2]
            mountpoint = mountpoint.replace("\\040", " ")
            if fstype in REAL_LINUX_FS:
                drives.append((device, mountpoint, fstype))
    return drives

SKIP_MAC_PREFIXES = (
    "/System/Volumes/VM", "/System/Volumes/Preboot", "/System/Volumes/Update",
    "/System/Volumes/xarts", "/System/Volumes/iSCPreboot", "/System/Volumes/Hardware",
)

def get_macos_drives():
    drives = []
    output = subprocess.run(["mount"], capture_output=True, text=True).stdout
    for line in output.splitlines():
        m = re.match(r"^(/dev/\S+) on (.+) \(([^,)]+)", line)
        if not m:
            continue
        device, mountpoint, fstype = m.groups()
        if mountpoint.startswith(SKIP_MAC_PREFIXES):
            continue
        drives.append((device, mountpoint, fstype))
    return drives

def get_drives():
    system = platform.system()
    if system == "Windows":
        return get_windows_drives()
    if system == "Linux":
        return get_linux_drives()
    if system == "Darwin":
        return get_macos_drives()
    raise RuntimeError(f"Unsupported OS: {system}")

# ---------- Check usage ----------

def check_whole_computer():
    total_all = used_all = free_all = 0
    seen = set()

    for device, mountpoint, fstype in get_drives():
        try:
            usage = shutil.disk_usage(mountpoint)
            dev_id = os.stat(mountpoint).st_dev
        except (PermissionError, OSError):
            continue

        if dev_id in seen:
            continue
        seen.add(dev_id)

        total_all += usage.total
        used_all += usage.used
        free_all += usage.free

    # ---- the print lines go here, replacing the old ones ----
    print(f"{ART_COLOR}{ASCII_ART}{RESET}")
    print(f"  {LABEL_COLOR}Total:{RESET} {VALUE_COLOR}{format_bytes(total_all)}{RESET}")
    if total_all:
        pct = used_all / total_all * 100
        print(f"  {LABEL_COLOR}Used:{RESET}  {VALUE_COLOR}{format_bytes(used_all)} ({pct:.1f}%){RESET}")
    print(f"  {LABEL_COLOR}Free:{RESET}  {VALUE_COLOR}{format_bytes(free_all)}{RESET}")

if __name__ == "__main__":
    check_whole_computer()