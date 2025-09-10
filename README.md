# Voxel Language | Intelektika-pt

Voxel is an imperative programming language inspired by Brainfuck, featuring an expanded syntax and the ability to be transpiled into Python code. The project includes an interpreter, a transpiler, and a full-featured command-line interface (CLI) for working with code.

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
3.  Install the package:
    *   **Linux/macOS:** Run `./setup-unix.sh`
    *   **Windows:** Run `setup-win.bat`

## Usage

### Via CLI
Launch the Voxel command shell:
```bash
voxel
```
Inside the CLI, the following commands are available:
*   `new <project_name>` — create a new project.
*   `build <input.vox> <output.py>` — compile a `.vox` file into `.py`.
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
