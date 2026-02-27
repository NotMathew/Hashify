#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                    Hashify  •  by Python                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime

# ANSI Colors
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"

# Hash Algorithms
HASH_OPTIONS = {
    "1":  ("MD5",       "md5"),
    "2":  ("SHA-1",     "sha1"),
    "3":  ("SHA-224",   "sha224"),
    "4":  ("SHA-256",   "sha256"),
    "5":  ("SHA-384",   "sha384"),
    "6":  ("SHA-512",   "sha512"),
    "7":  ("SHA3-224",  "sha3_224"),
    "8":  ("SHA3-256",  "sha3_256"),
    "9":  ("SHA3-384",  "sha3_384"),
    "10": ("SHA3-512",  "sha3_512"),
    "11": ("BLAKE2b",   "blake2b"),
    "12": ("BLAKE2s",   "blake2s"),
    "13": ("SHAKE-128", "shake_128"),
    "14": ("SHAKE-256", "shake_256"),
}

SHAKE_ALGOS = {"shake_128", "shake_256"}

# Helpers
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════╗
║                 🔐  Hashify  🔐                  ║
║          Hash any file easily & quickly          ║
╚══════════════════════════════════════════════════╝{RESET}
""")

def divider(color=DIM):
    print(f"{color}{'─' * 66}{RESET}")

def section(title):
    print(f"\n{BLUE}{BOLD}▸ {title}{RESET}")
    divider()

def fmt_size(size):
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def pause(msg="Press Enter to continue..."):
    input(f"\n{GRAY}{msg}{RESET}")

def get_files_in_dir(path):
    try:
        return sorted([str(f) for f in path.iterdir() if f.is_file()])
    except PermissionError:
        return []

def get_files_recursive(path):
    result = []
    for root, _, filenames in os.walk(path):
        for fn in sorted(filenames):
            result.append(os.path.join(root, fn))
    return result

def show_selected_summary(files):
    clear()
    banner()
    section("FILES SELECTED")
    limit = 25
    for i, fp in enumerate(files, 1):
        if i > limit:
            print(f"  {GRAY}  ... and {len(files) - limit} more file(s){RESET}")
            break
        size = fmt_size(os.path.getsize(fp)) if os.path.isfile(fp) else "?"
        print(f"  {GRAY}[{i:>3}]{RESET}  {WHITE}{os.path.basename(fp)}{RESET}  {GRAY}({size}){RESET}")
    print(f"\n{GREEN}✔ {len(files)} file(s) ready to be hashed.{RESET}")
    pause("Press Enter to continue to hash selection...")


# File Browser: pick single or multiple files
def browse_files(mode):
    cwd = Path.cwd()

    while True:
        clear()
        banner()

        try:
            all_entries = sorted(cwd.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
        except PermissionError:
            all_entries = []

        dirs  = [e for e in all_entries if e.is_dir()]
        files = [e for e in all_entries if e.is_file()]
        entries = dirs + files

        mode_label = "SINGLE FILE" if mode == "single" else "MULTI FILE"
        section(f"FILE BROWSER  ·  {mode_label}")
        print(f"  {GRAY}📂 Location:{RESET} {WHITE}{BOLD}{cwd}{RESET}\n")
        print(f"  {DIM}[ 0]{RESET}  {YELLOW}↑  Go up one level{RESET}")
        divider(GRAY)

        if not entries:
            print(f"  {RED}  (empty or inaccessible directory){RESET}")
        else:
            for i, entry in enumerate(entries, 1):
                if entry.is_dir():
                    print(f"  {DIM}[{i:>3}]{RESET}  {CYAN}📁 {entry.name}/{RESET}")
                else:
                    size = fmt_size(entry.stat().st_size)
                    print(f"  {DIM}[{i:>3}]{RESET}  {WHITE}📄 {entry.name}{RESET}  {GRAY}({size}){RESET}")

        divider(GRAY)
        if mode == "single":
            print(f"  {YELLOW}Enter a file number{RESET} to select it.")
            print(f"  {YELLOW}Enter a folder number{RESET} to navigate into it.")
        else:
            print(f"  {YELLOW}Enter file number(s){RESET} separated by commas  {GRAY}(e.g. 3, 5, 7){RESET}")
            print(f"  {YELLOW}Enter a single folder number{RESET} to navigate into it.")
        print(f"  {GRAY}[ q ] Cancel.{RESET}\n")

        raw = input(f"{CYAN}> {RESET}").strip()

        if raw.lower() == "q":
            return []
        if raw == "0":
            parent = cwd.parent
            cwd = parent if parent != cwd else cwd
            continue

        try:
            nums = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            print(f"\n{RED}❌ Invalid input.{RESET}")
            pause()
            continue

        if not nums:
            continue

        if len(nums) == 1:
            idx = nums[0]
            if idx < 1 or idx > len(entries):
                print(f"\n{RED}❌ Number out of range.{RESET}")
                pause()
                continue
            entry = entries[idx - 1]
            if entry.is_dir():
                cwd = entry.resolve()
                continue
            else:
                return [str(entry)]
        else:
            if mode == "single":
                print(f"\n{YELLOW}⚠ Single mode: enter only one number.{RESET}")
                pause()
                continue
            picked = []
            for idx in nums:
                if idx < 1 or idx > len(entries):
                    print(f"  {YELLOW}⚠ [{idx}] out of range, skipped.{RESET}")
                    continue
                entry = entries[idx - 1]
                if entry.is_file():
                    picked.append(str(entry))
                else:
                    print(f"  {YELLOW}⚠ [{idx}] is a folder - enter alone to navigate.{RESET}")
            if not picked:
                print(f"\n{RED}❌ No valid files selected.{RESET}")
                pause()
                continue
            return picked


# Option 5: Specific Folder Browser
def browse_folder_then_files():
    cwd = Path.cwd()

    # Step 1: Choose root folder
    while True:
        clear()
        banner()
        section("SELECT A FOLDER  ·  Option 5")
        print(f"  {GRAY}📂 Scanning:{RESET} {WHITE}{BOLD}{cwd}{RESET}")
        print(f"  {GRAY}Pick a folder to browse files inside it.{RESET}\n")

        try:
            dirs = sorted([e for e in cwd.iterdir() if e.is_dir()],
                          key=lambda e: e.name.lower())
        except PermissionError:
            dirs = []

        if not dirs:
            print(f"  {RED}  No folders found in the current directory.{RESET}")
            divider(GRAY)
            print(f"  {GRAY}[ q ] Cancel{RESET}\n")
            raw = input(f"{CYAN}> {RESET}").strip()
            if raw.lower() == "q":
                return []
            continue

        for i, d in enumerate(dirs, 1):
            try:
                sub_dirs  = sum(1 for x in d.iterdir() if x.is_dir())
                sub_files = sum(1 for x in d.iterdir() if x.is_file())
                info = f"{sub_files} file(s), {sub_dirs} subfolder(s)"
            except PermissionError:
                info = "no access"
            print(f"  {DIM}[{i:>3}]{RESET}  {CYAN}📁 {d.name}/{RESET}  {GRAY}({info}){RESET}")

        divider(GRAY)
        print(f"  {GRAY}[ q ] Cancel{RESET}\n")

        raw = input(f"{CYAN}Pick folder number: {RESET}").strip()
        if raw.lower() == "q":
            return []

        try:
            idx = int(raw)
        except ValueError:
            print(f"\n{RED}❌ Invalid input.{RESET}")
            pause()
            continue

        if idx < 1 or idx > len(dirs):
            print(f"\n{RED}❌ Number out of range.{RESET}")
            pause()
            continue

        root_folder = dirs[idx - 1].resolve()
        break

    # Step 2: Browse inside root_folder
    return _browse_inside_folder(root_folder, root_folder)


def _browse_inside_folder(root, cwd):
    while True:
        clear()
        banner()

        try:
            all_entries = sorted(cwd.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
        except PermissionError:
            all_entries = []

        dirs  = [e for e in all_entries if e.is_dir()]
        files = [e for e in all_entries if e.is_file()]
        entries = dirs + files

        try:
            rel = cwd.relative_to(root.parent)
        except ValueError:
            rel = cwd

        at_root = (cwd.resolve() == root.resolve())

        section("FILE BROWSER  ·  SPECIFIC FOLDER")
        print(f"  {GRAY}📁 Root folder:{RESET}  {CYAN}{BOLD}{root.name}/{RESET}")
        print(f"  {GRAY}📂 You are in:{RESET}   {WHITE}{rel}{RESET}\n")

        if not at_root:
            print(f"  {DIM}[ 0]{RESET}  {YELLOW}↑  Back to {cwd.parent.name}/{RESET}")
        else:
            print(f"  {GRAY}     (you are at the root of this folder){RESET}")

        divider(GRAY)

        if not entries:
            print(f"  {GRAY}  (empty or inaccessible){RESET}")
        else:
            for i, entry in enumerate(entries, 1):
                if entry.is_dir():
                    print(f"  {DIM}[{i:>3}]{RESET}  {CYAN}📁 {entry.name}/{RESET}")
                else:
                    size = fmt_size(entry.stat().st_size)
                    print(f"  {DIM}[{i:>3}]{RESET}  {WHITE}📄 {entry.name}{RESET}  {GRAY}({size}){RESET}")

        divider(GRAY)
        print(f"  {YELLOW}Enter file number(s){RESET} to select  {GRAY}(e.g.  3  or  2, 4, 5){RESET}")
        print(f"  {YELLOW}Enter 'all'{RESET} to select all files in this folder.")
        print(f"  {YELLOW}Enter a folder number{RESET} alone to go inside it.")
        if not at_root:
            print(f"  {GRAY}[ 0 ] Go back   [ q ] Cancel{RESET}\n")
        else:
            print(f"  {GRAY}[ q ] Cancel{RESET}\n")

        raw = input(f"{CYAN}> {RESET}").strip()

        if raw.lower() == "q":
            return []
        if raw == "0":
            if at_root:
                print(f"\n{YELLOW}⚠ Already at root. Use 'q' to cancel.{RESET}")
                pause()
            else:
                cwd = cwd.parent
            continue

        # 'all' → select all files in current folder
        if raw.lower() == "all":
            picked = [str(e) for e in files]
            if not picked:
                print(f"\n{YELLOW}⚠ No files in this folder to select.{RESET}")
                pause()
                continue
            print(f"\n{GREEN}✔ Selected all {len(picked)} file(s) in this folder.{RESET}")
            return picked

        try:
            nums = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            print(f"\n{RED}❌ Invalid input.{RESET}")
            pause()
            continue

        if not nums:
            continue

        if len(nums) == 1:
            idx = nums[0]
            if idx < 1 or idx > len(entries):
                print(f"\n{RED}❌ Number out of range.{RESET}")
                pause()
                continue
            entry = entries[idx - 1]
            if entry.is_dir():
                cwd = entry.resolve()
                continue
            else:
                return [str(entry)]
        else:
            picked = []
            for idx in nums:
                if idx < 1 or idx > len(entries):
                    print(f"  {YELLOW}⚠ [{idx}] out of range, skipped.{RESET}")
                    continue
                entry = entries[idx - 1]
                if entry.is_file():
                    picked.append(str(entry))
                else:
                    print(f"  {YELLOW}⚠ [{idx}] is a folder - enter alone to navigate.{RESET}")
            if not picked:
                print(f"\n{RED}❌ No valid files selected.{RESET}")
                pause()
                continue
            return picked


# MENU 1
def menu_select_files():
    clear()
    banner()
    section("MENU 1 - Select Files")

    cwd = Path.cwd()
    print(f"  {GRAY}Working directory: {WHITE}{cwd}{RESET}\n")
    print(f"  {YELLOW}[1]{RESET} Single file")
    print(f"       {GRAY}Browse & pick one file{RESET}")
    print(f"  {YELLOW}[2]{RESET} Multiple files")
    print(f"       {GRAY}Browse & pick several files at once{RESET}")
    print(f"  {YELLOW}[3]{RESET} All files in current directory")
    print(f"       {GRAY}Auto-reads every file here - no subfolders{RESET}")
    print(f"  {YELLOW}[4]{RESET} All files - recursive")
    print(f"       {GRAY}Auto-reads every file here + all subfolders{RESET}")
    print(f"  {YELLOW}[5]{RESET} Specific folder")
    print(f"       {GRAY}Choose a folder, navigate its contents, pick files{RESET}")
    divider()

    choice = input(f"\n{CYAN}Your Choice [1/2/3/4/5]: {RESET}").strip()
    files = []

    if choice == "1":
        files = browse_files("single")

    elif choice == "2":
        files = browse_files("multi")

    elif choice == "3":
        clear()
        banner()
        section("MENU 1 - All Files in Current Directory")
        print(f"  {GRAY}📂 Scanning:{RESET} {WHITE}{cwd}{RESET}\n")
        files = get_files_in_dir(cwd)
        if not files:
            print(f"  {YELLOW}⚠ No files found in the current directory.{RESET}")
            pause()
        else:
            print(f"  {DIM}Found {len(files)} file(s):{RESET}\n")
            limit = 30
            for i, fp in enumerate(files, 1):
                if i > limit:
                    print(f"  {GRAY}  ... and {len(files) - limit} more{RESET}")
                    break
                size = fmt_size(os.path.getsize(fp))
                print(f"  {GRAY}[{i:>3}]{RESET}  {WHITE}{os.path.basename(fp)}{RESET}  {GRAY}({size}){RESET}")
            print(f"\n{GREEN}✔ {len(files)} file(s) will be hashed.{RESET}")
            pause("Press Enter to continue to hash selection...")
            return files

    elif choice == "4":
        clear()
        banner()
        section("MENU 1 - All Files (Recursive)")
        print(f"  {GRAY}📂 Scanning recursively:{RESET} {WHITE}{cwd}{RESET}\n")
        print(f"  {DIM}Please wait...{RESET}", end="\r")
        files = get_files_recursive(cwd)
        print(" " * 50, end="\r")
        if not files:
            print(f"  {YELLOW}⚠ No files found.{RESET}")
            pause()
        else:
            print(f"  {DIM}Found {len(files)} file(s) across all subfolders:{RESET}\n")
            limit = 30
            for i, fp in enumerate(files, 1):
                if i > limit:
                    print(f"  {GRAY}  ... and {len(files) - limit} more{RESET}")
                    break
                size = fmt_size(os.path.getsize(fp))
                try:
                    rel = os.path.relpath(fp, cwd)
                except ValueError:
                    rel = fp
                print(f"  {GRAY}[{i:>3}]{RESET}  {WHITE}{rel}{RESET}  {GRAY}({size}){RESET}")
            print(f"\n{GREEN}✔ {len(files)} file(s) will be hashed.{RESET}")
            pause("Press Enter to continue to hash selection...")
            return files

    elif choice == "5":
        files = browse_folder_then_files()

    else:
        print(f"\n{RED}❌ Invalid choice.{RESET}")
        pause()
        return []

    if files:
        show_selected_summary(files)

    return files


# MENU 2
def menu_select_algos():
    clear()
    banner()
    section("MENU 2 - Select Hash Algorithm")

    for key, (label, _) in HASH_OPTIONS.items():
        print(f"  {YELLOW}[{key:>2}]{RESET} {label}")

    print(f"\n  {MAGENTA}[all]{RESET} All algorithms at once")
    divider()
    print(f"  {GRAY}Tip: combine multiple → e.g.  1, 4, 6{RESET}\n")

    raw = input(f"{CYAN}Your choice: {RESET}").strip().lower()

    if raw == "all":
        return list(HASH_OPTIONS.values())

    keys = [k.strip() for k in raw.split(",")]
    selected = []
    for k in keys:
        if k in HASH_OPTIONS:
            selected.append(HASH_OPTIONS[k])
        else:
            print(f"{YELLOW}⚠ Option '{k}' unrecognized, skipped.{RESET}")

    if not selected:
        print(f"{RED}❌ No algorithm selected.{RESET}")

    return selected


# Hashing-─
def compute_hash(filepath, algo):
    try:
        h = hashlib.new(algo)
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        if algo in SHAKE_ALGOS:
            return h.hexdigest(32)
        return h.hexdigest()
    except PermissionError:
        return "[ERROR: Permission Denied]"
    except Exception as e:
        return f"[ERROR: {e}]"

def hash_file(filepath, selected_algos):
    return {label: compute_hash(filepath, algo) for label, algo in selected_algos}


# Display Results
def display_results(results):
    clear()
    banner()
    lines = []
    header = (
        f"Hashify - Hash Results\n"
        f"Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'=' * 70}\n"
    )
    lines.append(header)
    section("HASH RESULTS")

    for filepath, algo_results in results.items():
        size = os.path.getsize(filepath) if os.path.isfile(filepath) else 0
        size_str = fmt_size(size)
        print(f"\n{WHITE}{BOLD}📄 {os.path.basename(filepath)}{RESET}")
        print(f"   {GRAY}{filepath}  ({size_str}){RESET}")
        lines.append(f"\nFILE : {filepath}")
        lines.append(f"SIZE : {size_str}")
        lines.append("-" * 70)
        divider(GRAY)

        for algo_label, hash_val in algo_results.items():
            color = GREEN if not hash_val.startswith("[ERROR") else RED
            print(f"  {CYAN}{algo_label:<12}{RESET} : {color}{hash_val}{RESET}")
            lines.append(f"  {algo_label:<12} : {hash_val}")

    return "\n".join(lines)


# MENU 3
def menu_after(result_text):
    section("MENU 3 - What's Next?")
    print(f"  {YELLOW}[1]{RESET} Export results to .txt file")
    print(f"  {YELLOW}[2]{RESET} Restart from the beginning")
    print(f"  {YELLOW}[3]{RESET} Exit program")
    divider()

    choice = input(f"\n{CYAN}Your choice [1/2/3]: {RESET}").strip()

    if choice == "1":
        default_name = f"hash_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        out_path = input(
            f"{CYAN}Output filename [{default_name}]: {RESET}"
        ).strip() or default_name
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(result_text)
            print(f"\n{GREEN}✔ Saved to: {os.path.abspath(out_path)}{RESET}")
        except Exception as e:
            print(f"{RED}❌ Failed to save: {e}{RESET}")

        again = input(f"\n{CYAN}Restart? [y/n]: {RESET}").strip().lower()
        return "restart" if again == "y" else "exit"

    elif choice == "2":
        return "restart"
    elif choice == "3":
        return "exit"
    else:
        print(f"{RED}❌ Invalid choice, exiting.{RESET}")
        return "exit"


# Main
def main():
    clear()
    banner()

    while True:
        files = []
        while not files:
            files = menu_select_files()
            if not files:
                retry = input(f"\n{CYAN}Try again? [y/n]: {RESET}").strip().lower()
                if retry != "y":
                    print(f"\n{YELLOW}Goodbye! 👋{RESET}\n")
                    sys.exit(0)

        selected_algos = []
        while not selected_algos:
            selected_algos = menu_select_algos()
            if not selected_algos:
                retry = input(f"\n{CYAN}Try again? [y/n]: {RESET}").strip().lower()
                if retry != "y":
                    print(f"\n{YELLOW}Goodbye! 👋{RESET}\n")
                    sys.exit(0)

        clear()
        banner()
        print(f"\n{DIM}Processing {len(files)} file(s) with {len(selected_algos)} algorithm(s)...{RESET}\n")
        all_results = {}
        for i, fp in enumerate(files, 1):
            bar = int((i / len(files)) * 40)
            print(
                f"  {CYAN}[{'█' * bar}{'░' * (40 - bar)}]{RESET}"
                f"  {i}/{len(files)}  {GRAY}{os.path.basename(fp)[:40]}{RESET}",
                end="\r"
            )
            all_results[fp] = hash_file(fp, selected_algos)
        print(" " * 80, end="\r")

        result_text = display_results(all_results)
        action = menu_after(result_text)

        if action == "restart":
            continue
        else:
            print(f"\n{GREEN}Thank you for using Hashify! 👋{RESET}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()