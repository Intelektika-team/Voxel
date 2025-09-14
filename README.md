# Voxel Language | Intelektika-pt

Voxel is an imperative programming language inspired by Brainfuck, featuring an expanded syntax and the ability to be transpiled into Python code. The project includes an interpreter, a transpiler, and a full-featured command-line interface (CLI) for working with code.

<img width="615" height="270" alt="Снимок экрана 2025-09-14 в 16 40 36" src="https://github.com/user-attachments/assets/a249f846-eba0-4c3a-a65e-e8f39e9c28ed" />


## Features

*   **Interpreter & Transpiler:** Voxel code can be executed directly by the interpreter or transpiled into an executable Python file.
*   **Tape-Based:** Like Brainfuck, the language uses an infinite tape (array) and a pointer for data manipulation.
*   **Extended Syntax:** Includes familiar commands (`>`, `<`, `+`, `-`) as well as more complex constructs (conditional jumps, macros, loops).
*   **Python Inline:** Allows direct insertion of Python code into a Voxel program using the `pyl` command.
*   **Library System:** Built-in libraries (`tape`, `stdio`) and support for custom imports.
*   **Command Line Interface (CLI):** Interactive shell for project creation, debugging, and code building.
*   **Cross-Platform:** Works on Windows and UNIX systems.

## Installation

1.  Ensure you have Python 3.6+ (3.9+ recomended) and `pip` installed.
2.  Download raw archive.
3.  Unzip archive in free folder
4.  Install the package:
    *   **Linux/macOS:** Run `bash setup-unix.sh`
    *   **Windows:** Open `setup-win.bat`
5.  Install VSCode extension:
    * Open folder with unziped archive in VSCode.
    * Open folder dist.
    * Right click on the file with the .vsix extension and select 'Install Extension VSIX'
<img width="520" height="551" alt="Снимок экрана 2025-09-14 в 16 47 33" src="https://github.com/user-attachments/assets/ad381729-1548-43a8-bebe-6e621ba1608a" />

## Usage

### Via CLI
Launch the Voxel command shell:
```bash
voxel
```
<img width="604" height="253" alt="Снимок экрана 2025-09-14 в 16 42 25" src="https://github.com/user-attachments/assets/4c99ac07-4830-4672-b237-24ede2029617" />

Inside the CLI, the following commands are available:
*   `new <project_name>` — create a new project.
*   `build <input.vox> <output.py>` — compile a `.vox` file into `.py`.
*   `builldstd` - compile a `main.vox` file into `_voxel_/build.py`.
*   `debug <input.vox>` — run code debugging.
*   `help` — show help for all commands.



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

or just
```voxel
pyl= print("Hello, //s world!");
```


---

Author - pt. 

Intelektika-team - 2025
