# ddiskspace

A fast, single-file Python tool that shows the total, used and free disk space of your **whole computer**, with a customizable ASCII logo and colors.

Works on **Windows**, **Linux** and **macOS**. No `pip install` needed, it only uses the Python standard library.

## Output
### Picture is on the very end!
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

- Python 3.7 or newer
- A terminal with ANSI color support (Windows Terminal, PowerShell 7, VS Code terminal, or any modern Linux/macOS terminal). The default logo color uses truecolor, which old `cmd.exe` may not display correctly.

## Usage

`diskspace.py` is the only file. Just run it:

```
python diskspace.py
```

On Linux/macOS you may need `python3 diskspace.py`.

## Customizing

Open `diskspace.py` and edit the block between `#customize` and `#customize ends here!` at the top:

| Variable | What it changes | Default |
|----------|-----------------|---------|
| `ASCII_ART` | The logo text | built-in logo |
| `ASCII_COLOR` | Logo color | ruby red `\033[38;2;202;1;71m` |
| `LABEL_COLOR` | `Total:`, `Used:`, `Free:` | ruby red `\033[38;2;202;1;71m` |
| `VALUE_COLOR` | The numbers | green `\033[92m` |
| `RESET` | Resets the color (leave as is) | `\033[0m` |

## Colors

Colors are ANSI escape codes written as strings.

**Truecolor (any exact color):** `\033[38;2;R;G;Bm`

```python
"\033[38;2;34;139;34m"    # forest green  (34, 139, 34)
"\033[38;2;53;94;59m"     # hunter green  (53, 94, 59)
"\033[38;2;202;1;71m"     # ruby red      (202, 1, 71)
```

Convert any hex code to RGB (for example `#228B22` becomes 34, 139, 34) and put the three numbers in.

**256-color palette (wider support):** `\033[38;5;Nm`

```python
"\033[38;5;28m"           # forest green (closest)
```

**Basic colors:**

| Code | Color | Bright version |
|------|-------|----------------|
| `\033[30m` | black | `\033[90m` |
| `\033[31m` | red | `\033[91m` |
| `\033[32m` | green | `\033[92m` |
| `\033[33m` | yellow | `\033[93m` |
| `\033[34m` | blue | `\033[94m` |
| `\033[35m` | magenta | `\033[95m` |
| `\033[36m` | cyan | `\033[96m` |
| `\033[37m` | white | `\033[97m` |

## How it works

- **Windows:** lists drive letters through the Windows API (`ctypes`). Fixed, removable and network drives are included. CD-ROMs and RAM disks are skipped.
- **Linux:** reads `/proc/mounts` and keeps only real filesystems (ext4, xfs, btrfs, ntfs, nfs, etc.). Virtual ones like `tmpfs` and `squashfs` are skipped.
- **macOS:** parses the output of `mount` and skips hidden system volumes (Preboot, VM, etc.).
- A device mounted in several places is counted only once.

### Why it is fast

- No external commands on Windows and Linux (macOS needs one call to `mount`).
- ANSI colors are enabled with a direct Windows API call instead of `os.system("")`.
- Modules like `re` and `subprocess` are only imported on the system that needs them.
- Disk numbers are read directly with `os.statvfs` (Linux/macOS) and `GetDiskFreeSpaceExW` (Windows).
- The whole output is printed in a single call.

## Troubleshooting

**Weird characters like `←[92m` instead of colors**
Your terminal doesn't support ANSI colors. Use Windows Terminal or PowerShell 7.

**Colors look different than expected**
Your terminal may not support truecolor. Use the 256-color format instead.

**Total looks bigger than the real disk (macOS, Btrfs, ZFS)**
Several volumes can share the same pool of space, so the grand total is only approximate on these systems.
### Picture:
<img width="690" height="222" alt="image" src="https://github.com/user-attachments/assets/81577ac9-28e7-4941-b632-4385cc596be4" />

### Credits to Claude helping little bit with the code & making this read me
### Copyright akettunen 2026
