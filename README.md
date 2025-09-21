# Voxel Language | Intelektika-pt
> Voxel language official repository.

[![Vxl](https://img.shields.io/badge/Vxl-tool-brightgreen?style=for-the-badge)](https://github.com/Intelektika-team/vxl)
[![Voxel Lang](https://img.shields.io/badge/Voxel-Lang-orange?style=for-the-badge)](https://github.com/Intelektika-team/Voxel)
[![Version](https://img.shields.io/badge/Version-0.7.2-blue?style=for-the-badge)](#)
[![Join](https://img.shields.io/badge/Join-us-red?style=for-the-badge)](https://intelektika-team.github.io/)
[![Team](https://img.shields.io/badge/Our-team-yellow?style=for-the-badge)](https://github.com/Intelektika-team)


Voxel is an imperative programming language inspired by Brainfuck, featuring an expanded syntax and the ability to be transpiled into Python code. The project includes an interpreter, a transpiler, and a full-featured command-line interface (CLI) for working with code.

<img width="922" height="445" alt="Снимок экрана 2025-09-21 в 21 02 11" src="https://github.com/user-attachments/assets/f398b34c-69ad-463d-8ca3-ce5de8185453" />

## Features

*   **Interpreter & Transpiler:** Voxel code can be executed directly by the interpreter or transpiled into an executable Python file.
*   **Tape-Based:** Like Brainfuck, the language uses an infinite tape (array) and a pointer for data manipulation.
*   **Extended Syntax:** Includes familiar commands (`>`, `<`, `+`, `-`) as well as more complex constructs (conditional jumps, macros, loops).
*   **Python Inline:** Allows direct insertion of Python code into a Voxel program using the `pyl` command.
*   **Library System:** Built-in libraries (`tape`, `stdio`, `base`) and support for custom imports.
*   **Package Manager:** The `vxl` tool allows you to install and manage libraries from official and third-party repositories.
*   **Command Line Interface (CLI):** Interactive shell for project creation, debugging, and code building.
*   **Cross-Platform:** Works on Windows and UNIX systems.

## Why is it needed?

- **Scripting**: Voxel is a lightweight and embedded language that translates directly into Python, making it ideal for writing small (and large) scripts.
- **Development at the junction**: With Voxel, you can create applications that use low-level tape and high-level Python at the same time.
- **Smart Database**: Voxel allows you to move projects to a special folder _voxel_/_dependencies_ and use it as a package manager, and also provides the ability to treat the ribbon as a huge database with cells.

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

## Usage

### Via Interactive CLI
Launch the Voxel command shell:
```bash
voxel
```
<img width="1006" height="492" alt="Снимок экрана 2025-09-21 в 20 58 02" src="https://github.com/user-attachments/assets/40256597-2d93-439f-8664-197ca0db6463" />

Inside the CLI, the following commands are available:
*   `new <project_name>` — create a new project.
*   `build <input.vox> <output.py>` — compile a `.vox` file into `.py`.
*   `buildstd` - compile a `main.vox` file into `_voxel_/build.py`.
*   `debug <input.vox>` — run code debugging.
*   `help` — show help for all commands.

### Via VXL Tool (Package Manager)

The `vxl` tool is a powerful package manager and build tool for Voxel projects:

<img width="1067" height="694" alt="Снимок экрана 2025-09-21 в 20 57 45" src="https://github.com/user-attachments/assets/c1b9e18b-e18f-4ea9-8796-c766f830a51e" />

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

:pyl-get-{
    pyl= data = http.get("https://api.example.com/data") 
    pyl= print(data)
}; pylpaste= get;
```

## Syntax

Voxel combines the low-level tape manipulation of Brainfuck with high-level constructs, offering a unique and powerful syntax for various programming tasks.

### Basic Structure
- **Commands** are separated by semicolons `;`.
- **Comments** start with `//=` and end with a semicolon:  
  `//= This is a comment;`
- **Voxels** (reusable code blocks) are defined with `:voxel-name-{...}` and called with `use= name`.
- **Parameters** (variables) are defined with `:param-name=value`.
- **Constants** are defined with `:const-NAME=value`.

### Core Commands

#### Tape Manipulation
| Command | Alias | Description |
| :--- | :--- | :--- |
| `nxt= N` | `>` | Move pointer right by `N` steps (default: 1) |
| `prv= N` | `<` | Move pointer left by `N` steps (default: 1) |
| `jmp= N` | | Move pointer to absolute position `N` |
| `pls= N` | `+` | Increase current cell value by `N` (default: 1) |
| `mns= N` | `-` | Decrease current cell value by `N` (default: 1) |
| `set= VALUE` | | Set current cell to `VALUE` (number, string, or expression) |
| `ers` | `!0` | Set current cell to 0 |
| `mov= N` | `>/` | Copy current cell value to position `N` |
| `swp= N` | `<>` | Swap values between current cell and cell at `N` |
| `mlt= N` | `*` | Multiply current cell by `N` |
| `dvs= N` | `/` | Divide current cell by `N` |

#### I/O Operations
| Command | Description |
| :--- | :--- |
| `out.char` | Output current cell value as ASCII character |
| `out.now` | Output raw current cell value |
| `out.str= TEXT` | Output text string (use `//s` for spaces, `//n` for newlines) |
| `out.next` | Output newline character |
| `in.char` | Read input character and store its ASCII value |
| `in.num` | Read input number |
| `in.str` | Read input string |

#### Flow Control
| Command | Description |
| :--- | :--- |
| `jz= LABEL` | Jump to voxel if current cell == 0 |
| `jnz= LABEL` | Jump to voxel if current cell != 0 |
| `jo= LABEL` | Jump to voxel if current cell == 1 |
| `jno= LABEL` | Jump to voxel if current cell != 1 |
| `jf= A,B` | Jump to voxel B if current cell == value A |
| `jnz= A,B` | Jump to voxel B if current cell != value A |
| `for= N,LABEL` | Execute voxel `N` times |

### Advanced Features

#### Meta-Commands
| Command | Description |
| :--- | :--- |
| `@include= LIB` | Include standard library (`tape`, `stdio`, `base`) |
| `@import= MOD,ALIAS` | Import Python module as alias |
| `@retape= SIZE` | Resize tape to new length |
| `@start` | Reset tape and pointer |
| `@relog` | Clear log buffer |

#### Special Constructs
```voxel
//= Define reusable code block;
:voxel-print_hello-{
    out.str= Hello//sWorld!/: out.next/:
};

//= Define parameter with value;
:param-count= 10; //= Type: int (10);
:param-message= Hello; //= Type: str ('Hello');
:param-message= f10; //= Type: float (10.0);

//= Define constant value;
:const-TIMEOUT= 1000;

//= Multi-line Python integration;
:pyl-math_code-{
    result = 2 + 2 * 2
    print(f"Result: {result}")
};

//= System output;
:sys.out(Text with spaces);

//= Logging;
:log.new(Operation completed);
:log.out; // Output all logs
```

#### Python Integration
```voxel
//= Single line Python;
pyl= print("Inline Python code");

//= Multi-line Python block;
:pyl-custom_logic-{
    import requests
    response = requests.get('https://api.example.com')
    print(response.status_code)
};

//= Use defined Python code;
pylpaste= custom_logic;
```

#### Expressions and Variables
```voxel
//= Use current position (?);
:param-current_pos=?;

//= Use current cell value (!);
:param-cell_value=!;

//= List with dynamic values;
:param-data=[1, ?, !, 'text'];

//= Parameter math operations;
ppl= count, 1;    //= count += 1;
pmn= count, 1;    //= count -= 1;
pmp= count, 2;    //= count *= 2;
pdv= count, 2;    //= count /= 2;

//= Type checking;
out.ptype= param_name;  //= Output parameter type;
```





## Package Repository

Discover and share packages through our official repository:
[VXL Official Package Repository](https://github.com/Intelektika-team/vxl)

Contribute your own packages by submitting pull requests to the repository!

---

Author - pt. 

Intelektika-team - started at 2025 - VoxelLang
