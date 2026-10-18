# Disk Space Checker

A small, dependency-free Python tool that shows the total, used and free disk space of your **whole computer** with customizable ASCII art and colors.

Works on **Windows**, **Linux** and **macOS**. No `pip install` needed, it only uses the Python standard library.

## Output
+ a picture in the end of the readme!
```
    __     __ __         __
.--|  |.--|  |__|.-----.|  |--.-----.-----.---.-.----.-----.
|  _  ||  _  |  ||__ --||    <|__ --|  _  |  _  |  __|  -__|
|_____||_____|__||_____||__|__|_____|   __|___._|____|_____|
                                    |__|
  Total: 931.5 GB
  Used:  412.3 GB (44.3%)
  Free:  519.2 GB
```

## Requirements

- Python 3.6 or newer
- A terminal with ANSI color support (Windows Terminal, PowerShell 7, VS Code terminal, or any modern Linux/macOS terminal). For the exact colors, truecolor support is needed. Old `cmd.exe` may show wrong colors.

Keep all files in the **same folder**.

## Usage

```
python diskspace.py
```

On Linux/macOS you may need `python3 diskspace.py`.

## How it works

- **Windows:** lists drive letters through the Windows API (`ctypes`) and includes fixed, removable and network drives. CD-ROMs and RAM disks are skipped.
- **Linux:** reads `/proc/mounts` and keeps only real filesystems (ext4, xfs, btrfs, ntfs, nfs, etc.). Virtual ones such as `tmpfs` and `squashfs` are skipped.
- **macOS:** parses the output of `mount` and skips hidden system volumes (Preboot, VM, etc.).
- The same filesystem mounted in several places is counted only once.
- The numbers come from `shutil.disk_usage()`.
