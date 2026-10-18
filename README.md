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

## Files

| File | Purpose |
|------|---------|
| `diskspace.py` | The main script. Run this one. |
| `customize.py` | Your ASCII art and color settings (optional). |
| `colors.py` | Color helper with 237 named colors (optional). |
| `colors_names_ansi.txt` | Copy-paste list of every color as a ready ANSI code. |

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

## Customizing

Create or edit `customize.py`. If the file is missing, the script uses built-in defaults. If it only defines some settings, the rest fall back to defaults.

```python
from colors import fg, RESET

ASCII_ART = r"""
    __     __ __         __
.--|  |.--|  |__|.-----.|  |--.-----.-----.---.-.----.-----.
|  _  ||  _  |  ||__ --||    <|__ --|  _  |  _  |  __|  -__|
|_____||_____|__||_____||__|__|_____|   __|___._|____|_____|
                                    |__|"""

ART_COLOR = fg("forest")      # color of the ASCII art
LABEL_COLOR = fg("saffron")   # color of "Total:", "Used:", "Free:"
VALUE_COLOR = fg("lime")      # color of the numbers
```

### Setting colors

Using `colors.py`, a color can be given in three ways:

```python
fg("forest")            # by name
fg("#228B22")           # by hex code
fg((34, 139, 34))       # by RGB values
```

Names are lowercase and use underscores instead of spaces, e.g. `burnt_orange`, `french_beige`, `hunter`.

Some names appear twice in the original color chart with different shades. The second one ends with `_2`, e.g. `orchid` and `orchid_2`.

To preview every color in your terminal:

```
python colors.py
```

### Without colors.py

You can also write raw ANSI codes directly. Truecolor format is `\033[38;2;R;G;Bm`:

```python
ART_COLOR = "\033[38;2;34;139;34m"   # forest green
```

`colors_names_ansi.txt` contains ready-made lines such as `forest = "\033[38;2;11;102;35m"` for every color.

## Troubleshooting

**`ModuleNotFoundError: No module named 'customize'`**
`customize.py` is not in the same folder as `diskspace.py`, or it is named wrong (for example `customize.py.txt`). In File Explorer, enable *View > Show > File name extensions* to check. The script still runs with defaults even if the file is missing.

**Weird characters like `←[96m` instead of colors**
Your terminal does not support ANSI colors. Use Windows Terminal or PowerShell 7, or remove the color codes.

**Colors look slightly different than expected**
Your terminal may not support truecolor. Use 256-color codes instead: `\033[38;5;Nm` (for example `\033[38;5;28m` for a forest green).

**Total looks bigger than the real disk (macOS, Btrfs, ZFS)**
Several volumes can share the same pool of space, so the grand total is only approximate on these systems.

## Notes

- A few hex values in `colors.py` (for example `spring`, `snow`, `dusty_gray`) were read from an image and may be slightly off. Edit them in the `COLORS` dictionary if needed.
