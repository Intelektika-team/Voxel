# Voxel Language | Intelektika-pt
> Voxel language official repository.

[![Vxl](https://img.shields.io/badge/Vxl-tool-brightgreen?style=for-the-badge)](https://github.com/Intelektika-team/vxl)
[![Voxel Lang](https://img.shields.io/badge/Voxel-Lang-orange?style=for-the-badge)](https://github.com/Intelektika-team/Voxel)
[![inf](https://img.shields.io/badge/Version-0.7.2-blue?style=for-the-badge)](#)
[![inf](https://img.shields.io/badge/Join-us-red?style=for-the-badge)](https://intelektika-team.github.io/)


Voxel is an imperative programming language inspired by Brainfuck, featuring an expanded syntax and the ability to be transpiled into Python code. The project includes an interpreter, a transpiler, and a full-featured command-line interface (CLI) for working with code.

<img width="615" height="270" alt="Voxel Language Overview" src="https://github.com/user-attachments/assets/a249f846-eba0-4c3a-a65e-e8f39e9c28ed" />

## Features

*   **Interpreter & Transpiler:** Voxel code can be executed directly by the interpreter or transpiled into an executable Python file.
*   **Tape-Based:** Like Brainfuck, the language uses an infinite tape (array) and a pointer for data manipulation.
*   **Extended Syntax:** Includes familiar commands (`>`, `<`, `+`, `-`) as well as more complex constructs (conditional jumps, macros, loops).
*   **Python Inline:** Allows direct insertion of Python code into a Voxel program using the `pyl` command.
*   **Library System:** Built-in libraries (`tape`, `stdio`, `base`) and support for custom imports.
*   **Package Manager:** The `vxl` tool allows you to install and manage libraries from official and third-party repositories.
*   **Command Line Interface (CLI):** Interactive shell for project creation, debugging, and code building.
*   **Cross-Platform:** Works on Windows and UNIX systems.

## Installation

1.  Ensure you have Python 3.6+ (3.9+ recommended) and `pip` installed.
2.  Download raw archive.
3.  Unzip archive in free folder
4.  Install the package:
    *   **Linux/macOS:** Run `bash setup-unix.sh`
    *   **Windows:** Open `setup-win.bat`
5.  Install VSCode extension:
    * Open folder with unzipped archive in VSCode.
    * Open folder dist.
    * Right click on the file with the .vsix extension and select 'Install Extension VSIX'
<img width="520" height="551" alt="VSCode Extension Installation" src="https://github.com/user-attachments/assets/ad381729-1548-43a8-bebe-6e621ba1608a" />

## Usage

### Via Interactive CLI
Launch the Voxel command shell:
```bash
voxel
```
<img width="604" height="253" alt="Voxel CLI Interface" src="https://github.com/user-attachments/assets/4c99ac07-4830-4672-b237-24ede2029617" />

Inside the CLI, the following commands are available:
*   `new <project_name>` — create a new project.
*   `build <input.vox> <output.py>` — compile a `.vox` file into `.py`.
*   `buildstd` - compile a `main.vox` file into `_voxel_/build.py`.
*   `debug <input.vox>` — run code debugging.
*   `help` — show help for all commands.

### Via VXL Tool (Package Manager)

The `vxl` tool is a powerful package manager and build tool for Voxel projects:

**Creating a new project:**
```bash
vxl -n my_project
```

**Building a Voxel file:**
```bash
vxl -b main.vox output.py
```

**Building and running immediately:**
```bash
vxl -br main.vox output.py
```

**Installing packages from official repository:**
```bash
vxl -i package_name
```

**Installing packages from custom GitHub repositories:**
```bash
vxl -if user/repo package_name
```

**Additional commands:**
```bash
vxl -cl          # Clear all build files
vxl -clc         # Clear cache files
vxl -v           # Show version
vxl -h           # Show help
```

Example of using an installed package:
```voxel
@include= tape;
@include= stdio;
@import= http_utils, http;

:voxel-main-{
    pyl= data = http.get("https://api.example.com/data") /:
    pyl= print(data) /:
};

use= main;
```

## Code Example

Example "Hello World" program:
```voxel
@include= stdio;
@include= tape;

:voxel-main-{
    set= 72 /: out.char/: set= 101 /: out.char /: set= 108 /: out.char /: out.char /: set= 111 /: out.char /:
    set= 32 /: out.char /:
    set= 87 /: out.char /: set= 111 /: out.char /: set= 108 /: out.char /: set= 108 /: out.char /: set= 100 /: out.char /:
    set= 33 /: out.char /: out.next
};

use= main;
```

or just:
```voxel
pyl= print("Hello, //s world!");
```

## Package Repository

Discover and share packages through our official repository:
[VXL Official Package Repository](https://github.com/Intelektika-team/vxl-packages)

Contribute your own packages by submitting pull requests to the repository!

---

Author - pt. 

Intelektika-team - 2025
