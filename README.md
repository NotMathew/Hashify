# Hashify 🔐

**📋 Description**

An interactive, terminal-based Python utility designed to quickly and efficiently compute file hashes. Whether you are verifying file integrity, analyzing malware payloads, or conducting digital forensics, Hashify provides a sleek, color-coded UI to make the process seamless. 

**🎯 Key Features**

- **Extensive Algorithm Support:** Computes hashes using MD5, SHA-1, SHA-2 (224, 256, 384, 512), SHA-3, BLAKE2b/s, and SHAKE.
- **Flexible Target Selection:** - Scan a single file or seamlessly select multiple files.
  - Auto-read all files in a specific directory.
  - Perform deep recursive scans across folders and subfolders.
  - Built-in interactive file and folder browser.
- **Interactive Terminal UI:** Clean, color-coded navigation menus with real-time progress bars for heavy workloads.
- **Export Capabilities:** Instantly generate and save comprehensive hash reports into `.txt` files for documentation or forensic logging.
- **Performance Optimized:** Processes files in chunks (64KB) to maintain low memory usage, even when analyzing massive files like virtual machine images or raw disk dumps.

**📁 Supported Platforms**

- Windows
- Linux
- macOS

**📦 Dependencies**

None! Hashify is built entirely using Python's standard library.

## Installation on Windows 10/11
Go to [Releases](https://github.com/NotMathew/Hashify/releases) and download the latest version, or run the script directly via Python.

## Installation on Linux & macOS
```bash
git clone https://github.com/NotMathew/Hashify.git
cd Hashify
python Hashify.py
