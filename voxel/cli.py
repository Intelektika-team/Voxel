import voxel.lang as lang
import voxel.interface as i
import os
import platform
import time

def cls():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

p = lang.local_parser
l = lang.local_lang
h = lang.handle_error


ver_str = "v0.5.8 1st-alpha stable"

about_str = f"""
======= About =======
Voxel lang is a brainfuck's type lang by developers from Kvantorium73 - Intelektika.
Version: {ver_str}
======= About =======
"""

help_str = """
======= Help =======
new <name_of_ptoject> - create the project
build <file_voxel> <file_to_convert> - convert the voxel lang to pyhton
debug <file_vixel> - test voxel code with output
cd <dir> - change current dir
ls - show available files in current dir
restart - restart voxel cli
exit - exit from cli
help - show this massage
ver - show version
about - show about
======= Help =======
"""

logo = """
    ██╗░░░██╗░█████╗░██╗░░██╗███████╗██╗░░░░░
    ██║░░░██║██╔══██╗╚██╗██╔╝██╔════╝██║░░░░░
    ╚██╗░██╔╝██║░░██║░╚███╔╝░█████╗░░██║░░░░░
    ░╚████╔╝░██║░░██║░██╔██╗░██╔══╝░░██║░░░░░
    ░░╚██╔╝░░╚█████╔╝██╔╝╚██╗███████╗███████╗
    ░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚══════╝
"""
@h(exiting=False)
def __main__():
    while True:
        cls()
        home_dir = os.path.expanduser("~")
        os.chdir(home_dir)
        print(f"""

    Welcom to the ===========================

{i.color.set(logo, i.color.BRIGHT_GREEN, i.color.BOLD)}

    The voxel lang cli =====================
    Type '-h' for help
              """)
        prev = ['', '']
        while True:
            try:
                cpath = lang.color.blue(os.getcwd())
                inps = input(f"\n{cpath} => ")
                if inps == 'prev':
                    inps = prev[-1]

                inp = inps.split()

                if inp[0] in ['build', '-b']:
                    try:
                        path = f"{inp[1]}"
                        print(i.color.set(f'Building {path} to {inp[2]}...', i.color.YELLOW))
                        with open(path, 'r') as f:
                            file = f.read()
                            print(i.color.set(f'Open succes... \n Build...', i.color.YELLOW))
                            lang.builder(file, inp[2])
                            print(i.color.set(f'\nBuild succes...', i.color.GREEN))
                    except FileNotFoundError:
                        print(lang.Errors.SystemERROR(f'File not found.', False))


                    except Exception as e:
                        lang.Errors.SystemERROR(f'Error. {e}', False)

                elif inp[0] in ['-d', 'debug', 'deb']:
                    try:
                        path = f"{inp[1]}"
                        print(i.color.set('Debuging start ===', i.color.GREEN))
                        print(i.color.set(f'Opening {path}...', i.color.YELLOW))
                        with open(path, 'r') as f:
                            file = f.read()
                            print(i.color.set(f'Open succes... \nRuning...', i.color.YELLOW))
                            p.parse(file)
                            print(i.color.set(f'Running succes...', i.color.GREEN))
                        print(i.color.set(f'Debug succes =====', i.color.GREEN))
                    except FileNotFoundError:
                        lang.Errors.SystemERROR(f'File not found.', False)


                    except Exception as e:
                        lang.Errors.SystemERROR(f'Error. {e}', False)


                elif inp[0] == 'exit':
                    raise KeyboardInterrupt()

                elif inp[0] == 'cd':
                    os.chdir(inp[1])

                elif inp[0] == 'ls':
                    print(" | ".join(os.listdir(os.getcwd())))

                elif inp[0] in ['restart', 'reset']:
                    break

                elif inp[0] in ['cls', 'clear']:
                    break

                elif inp[0] in ['-h', '-H', 'help']:
                    print(help_str)

                elif inp[0] in ['-v', '-V', 'ver']:
                    print(ver_str)

                elif inp[0] in ['-a', '-A', 'about']:
                    print(about_str)

                elif inp[0] in ['-n', 'new']:
                    current = os.getcwd()
                    name = str(inp[1])
                    dir_path = os.path.join(os.getcwd(), name)
                    print(i.color.set('Creating project ===', i.color.GREEN))
                    print(i.color.set(f'Creating {name}...', i.color.YELLOW))

                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                        print(i.color.set(f"Directory '{dir_path}' created successfully.", i.color.YELLOW))
                    else:
                        lang.Errors.FileERROR('Directory already exists')
                        continue  # или return в зависимости от логики

                    os.chdir(name)
                    
                    # Создание основного файла
                    code = """= Hello_user!_That's_the_basic_structure_of_voxel_programm._We_recomended_to_write_code_like_that.;

:voxel-setup-{
    @start /:
    @include= tape /:
    @include= first_programm /:
    = Your_setup-voxel_here /:
};

:voxel-programm-{
    pyl= main('User') /:
    = Your_program-voxel_here /:
};

= Start;

:voxel-main-{
    use= setup /:
    use= programm /:
    = Your_main-voxel_here /:
};

use= main;
= End;"""

                    with open('main.vox', 'w') as file:
                        file.write(code)
                        print(i.color.set("File 'main.vox' created successfully.", i.color.YELLOW))

                    # Создание папки зависимостей
                    deps_path = os.path.join("_voxel_", "_dependencies_")
                    if not os.path.exists(deps_path):
                        os.makedirs(deps_path)
                        print(i.color.set(f"Directory '{deps_path}' created successfully.", i.color.YELLOW))
                        
                        # Создание тестового файла в папке зависимостей
                        code_dependencies = """
def main():
    print('Hello world')"""
                        
                        with open(os.path.join(deps_path, 'test.py'), 'w') as file:
                            file.write(code_dependencies)
                            print(i.color.set("Dependencies file 'test.py' created successfully.", i.color.YELLOW))
                    else:
                        print('Project dependencies folder already exists')

                    os.chdir(current)
                    print(i.color.set("Project created =====", i.color.GREEN))

                else:
                    print(i.color.set('Unknown command. Type "-h" for help', i.color.YELLOW))
                prev.append(inps)

            except KeyboardInterrupt:
                print(i.color.bold_blue('\n\nExit? y/n'))
                inp_e = input()
                if inp_e in ('', 'y'):
                    print(i.color.set('\n\nExtiting... ', i.color.BOLD, i.color.BRIGHT_RED))
                    time.sleep(1)
                    exit()
                else:
                    print(i.color.set('\n\nRestarting...', i.color.BOLD, i.color.BRIGHT_RED))
                    break

            except Exception as e:
                print(i.color.set(f'Error... {e}', i.color.RED))
                break


