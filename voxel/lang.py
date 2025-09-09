from voxel.interface import *


class Errors:
    def SyntaxERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSyntax Error - {text}"))
        if exiting: exit()

    def SystemERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSystem Error - {text}"))
        if exiting: exit()

    def ErrorHANDLER(text :str, exiting :bool=True):
        print(color.set(f"Handled Error - {text}", color.YELLOW))
        if exiting: exit()
    
    def NotFoundERROR(text :str, exiting :bool=True):
        print(color.set(f"Not found - {text}", color.YELLOW))
        if exiting: exit()
    
    def IncludeERROR(text :str, exiting :bool=True):
        print(color.set(f"Error in include - {text}", color.YELLOW))
        if exiting: exit()

    def FileERROR(text :str, exiting :bool=True):
        print(color.set(f"File error - {text}", color.YELLOW))
        if exiting: exit()

def handle_error(exiting=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Errors.ErrorHANDLER(f"{str(e)} in {func}", False)
                if exiting: exit()
        return wrapper
    return decorator

def spacedelete(code):
    return code.replace(' ', '').replace('\n', '')


points = {}

class VoxelParser:
    def __init__(self):
        self.commands={}
    
    def add_command(self, command :str, function :object, args :list=None, langargs :bool=False):
        self.commands[command] = {'f':function, 'a':args, 'la':langargs}
    
    def parse(self, code :str, sep :str=';'):
        code = spacedelete(code).split(sep)
        now = 0
        for i in code:
            now += 1
            worked = False
            try:
                try:
                    command = i.split('=')[0]
                    args = i.split('=')[1]
                except:
                    command = i
                    args = ''
                if command.startswith(':voxel'):
                    try:
                        splitted = i.split('-', 2)
                    except:
                        raise SystemError()
                    points[splitted[1]] = splitted[2]
                    worked = True
                elif command in self.commands:
                    self.commands[command]['f']("".join(self.commands[command]['a']) if not self.commands[command]['la'] else args)
                    worked = True
                elif worked == False:
                    Errors.SyntaxERROR(f"Unknown keyword '{command}' in line {now}")
            except Exception as e:
                Errors.ErrorHANDLER(f"Error in line {now} - {e}")



class VoxelLang:
    def __init__(self, length: int):
        self.length = length
        self.reset()

    def reset(self):
        self.tape = {}
        # Создаем ленту с индексами от -length/2 до length/2
        self.gentape(self.length)
        self.pos = 0  # Стартовая позиция в середине ленты
        self.code = []
        self.libs = {"tape":{"lib":f"tape, pos = {self.tape}, {self.pos}", "used":False},"stdio":
        {"lib":"""

# MARK: Standart pyl library 
class color:
    # Базовые цвета
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Яркие цвета
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Стили текста
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def green(text):
        return f"{color.BRIGHT_GREEN}{text}{color.RESET}"
    
    @staticmethod
    def bold_green(text):
        return f"{color.BOLD}{color.BRIGHT_GREEN}{text}{color.RESET}"
    
    @staticmethod
    def underline_green(text):
        return f"{color.UNDERLINE}{color.BRIGHT_GREEN}{text}{color.RESET}"
    
    @staticmethod
    def red(text):
        return f"{color.BRIGHT_RED}{text}{color.RESET}"
    
    @staticmethod
    def bold_red(text):
        return f"{color.BOLD}{color.BRIGHT_RED}{text}{color.RESET}"
    
    @staticmethod
    def underline_red(text):
        return f"{color.UNDERLINE}{color.BRIGHT_RED}{text}{color.RESET}"
    


    
    @staticmethod
    def blue(text):
        return f"{color.BRIGHT_BLUE}{text}{color.RESET}"
    
    @staticmethod
    def bold_blue(text):
        return f"{color.BOLD}{color.BRIGHT_BLUE}{text}{color.RESET}"
    
    @staticmethod
    def underline_blue(text):
        return f"{color.UNDERLINE}{color.BRIGHT_BLUE}{text}{color.RESET}"
    
    @staticmethod
    def set(text, *col):
        return f"{' '.join(col)}{text}{color.RESET}"
   

class Errors:
    def SyntaxERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSyntax Error - {text}"))
        if exiting: exit()

    def SystemERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSystem Error - {text}"))
        if exiting: exit()

    def ErrorHANDLER(text :str, exiting :bool=True):
        print(color.set(f"Handled Error - {text}", color.YELLOW))
        if exiting: exit()
    
    def NotFoundERROR(text :str, exiting :bool=True):
        print(color.set(f"Not found - {text}", color.YELLOW))
        if exiting: exit()
    
    def IncludeERROR(text :str, exiting :bool=True):
        print(color.set(f"Error in include - {text}", color.YELLOW))
        if exiting: exit()

    def FileERROR(text :str, exiting :bool=True):
        print(color.set(f"File error - {text}", color.YELLOW))
        if exiting: exit()

def cls():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def handle_error(exiting=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Errors.ErrorHANDLER(str(e), False)
                if exiting: exit()
        return wrapper
    return decorator


@handle_error()
def getpos():
    return pos

@handle_error()
def setpos(new_pos):
    global pos
    pos = new_pos

@handle_error()
def find_value(value):  # Поиск значения на ленте
    for key, val in tape.items():
        if val == value:
            return key
    return None

@handle_error()
def tape_range():  # Диапазон занятых ячеек
    return min(tape.keys()), max(tape.keys())


@handle_error()
def data():
    return tape[pos]

@handle_error()
def set(arg):
    tape[pos] = arg

def wait(delay:int):
    time.sleep(delay*0.001)

""", "used":False},



"first_programm":{"lib":
"""
def main(user :str='Guest'):
    print(f'Hello, {user}!')
""", "used":False}
}
        

        self.code.append(f"\n # MARK: System")
        self.code.append(
"""
import os, platform, time
""")
        
    
    @handle_error()
    def gentape(self, length :int):
        for i in range(length):
            self.tape[i-(length//2)] = 0

    @handle_error()
    def include(self, arg_str :str=''):
        try: 
            if arg_str in self.libs:
                using = self.libs[arg_str]['used']
                if using==False:
                    self.code.append(self.libs[arg_str]['lib'])
                    self.libs[arg_str]['used'] = True
                elif using==True:
                    Errors.IncludeERROR(f'Library {self.used} - Already use: {using}')
            else:
                Errors.NotFoundERROR(f"Library {arg_str} isn't found.")
        except Exception as e:
            Errors.IncludeERROR(f'Include error: {e}')

    @handle_error()
    def import_func(self, arg_str :str=''):
        inp = arg_str.split()
        try: 
            self.code.append(f'import _dependencies_.{inp[0]}')
        except Exception as e:
            Errors.IncludeERROR(f'Import error: {e}')

    @handle_error()
    def next(self, arg_str: str = ""):
        steps = 1 if arg_str == "" else int(arg_str)
        self.pos += steps
        self.code.append(f"pos += {steps}")
    
    @handle_error()
    def prev(self, arg_str: str = ""):
        steps = 1 if arg_str == "" else int(arg_str)
        self.pos -= steps
        self.code.append(f"pos -= {steps}")
    
    @handle_error()
    def plus(self, arg_str: str = ""):
        n = 1 if arg_str == "" else int(arg_str)
        self.tape[self.pos] += n
        self.code.append(f"tape[pos] += {n}")
    
    @handle_error()
    def minus(self, arg_str: str = ""):
        n = 1 if arg_str == "" else int(arg_str)
        self.tape[self.pos] -= n
        self.code.append(f"tape[pos] -= {n}")
    
    @handle_error()
    def set(self, arg_str: str):
        self.tape[self.pos] = int(arg_str)
        self.code.append(f"tape[pos] = {int(arg_str)}")
    
    @handle_error()
    def erase(self, arg_str: str = ""):
        self.tape[self.pos] = 0
        self.code.append(f"tape[pos] = 0")
    
    @handle_error()
    def getnow(self):
        self.code.append(f"print(tape[pos])")
        return self.tape[self.pos]
    
    @handle_error()
    def output_char(self, arg_str: str = ""):
        t = chr(self.tape[self.pos])
        print(t, end='')
        self.code.append(f"print(chr(tape[pos]), end='')")
    
    @handle_error()
    def output_num(self, arg_str: str = ""):
        t = self.tape[self.pos]
        print(t, end='')
        self.code.append(f"print(tape[pos], end='')")

    @handle_error()
    def output_next(self, arg_str: str = ""):
        print()
        self.code.append(f"print()")

    @handle_error()
    def print(self, arg_str: str = ""):
        self.code.append(f"print({arg_str}, end='')")
        print(arg_str)
    
    @handle_error()
    def copy(self, arg_str: str = ""):
        pos = int(arg_str)
        self.tape[pos] = self.tape[self.pos]
        self.code.append(f"tape[{pos}] = tape[pos]")
    
    @handle_error()
    def python_line(self, arg_str: str = ""):
        arg_str = arg_str.replace('//n', '\n').replace('//tab', '    ').replace('//s', ' ').replace('//-', '=')
        self.code.append(f"{arg_str}")
    
    @handle_error()
    def input_char(self, arg_str: str = ""):
        char = ord(input()[0])
        self.tape[self.pos] = ord(char)
        self.code.append(f"tape[pos] = ord(input()[0])")
    
    @handle_error()
    def input_num(self, arg_str: str = ""):
        self.tape[self.pos] = int(input())
        self.code.append(f"tape[pos] = int(input())")

    @handle_error()
    def comentary(self, arg_str: str = ""):
        self.code.append(f"# {arg_str}")
        pass

    @handle_error()
    def multyply(self, arg_str: str = ""):
        self.tape[self.pos] *= int(arg_str)
        self.code.append(f"tape[pos] *= {arg_str}")

    @handle_error()
    def divission(self, arg_str: str = ""):
        self.tape[self.pos] //= int(arg_str)
        self.code.append(f"tape[pos] //= {arg_str}")
    
    @handle_error()
    def tp(self, arg_str: str = ""):
        self.pos = int(arg_str)
        self.code.append(f"pos = {arg_str}")
        

    @handle_error()
    def where(self, arg_str: str = ""):
        self.code.append(f"print(pos, end='')")
        print(self.pos, end='')
    
    @handle_error()
    def data(self, arg_str: str = ""):
        self.code.append(f"print(tape[pos], end='')")
        print(self.tape[self.pos], end='')
    
    @handle_error()
    def getcode(self):
        return self.code
    
    @handle_error()
    def printcode(self):
        print("\n".join(self.code))
    
    @handle_error()
    def build(self, path: str = 'cache.py'):
        import os
        
        # Создаем директорию для системы
        cache_dir = os.path.join(os.getcwd(), '_voxel_')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Формируем полный путь к файлу внутри директории кэша
        full_file_path = os.path.join(cache_dir, path)
        
        # Генерируем и записываем код
        code = "\n".join(self.getcode())
        
        with open(full_file_path, 'w') as f:
            f.write(code)
        
        print(f'Done. File saved to: {full_file_path}')
    
    
    
local_lang = VoxelLang(100001)
local_parser = VoxelParser()
    
# Регистрируем команды
local_parser.add_command('nxt', local_lang.next, langargs=True)
local_parser.add_command('prv', local_lang.prev, langargs=True)
local_parser.add_command('>', local_lang.next, langargs=True)
local_parser.add_command('<', local_lang.prev, langargs=True)
local_parser.add_command('pl', local_lang.plus, langargs=True)
local_parser.add_command('mn', local_lang.minus, langargs=True)
local_parser.add_command('+', local_lang.plus, langargs=True)
local_parser.add_command('-', local_lang.minus, langargs=True)
local_parser.add_command('set', local_lang.set, langargs=True)
local_parser.add_command('erase', local_lang.erase, langargs=True)
local_parser.add_command('!0', local_lang.erase, langargs=True)
local_parser.add_command('out.char', local_lang.output_char, langargs=True)
local_parser.add_command('out.num', local_lang.output_num, langargs=True)
local_parser.add_command('out.str', local_lang.print, langargs=True)
local_parser.add_command('out.next', local_lang.output_next, langargs=True)
local_parser.add_command('in.char', local_lang.input_char, langargs=True)
local_parser.add_command('in.num', local_lang.input_num, langargs=True)
local_parser.add_command('', local_lang.comentary, langargs=True)
local_parser.add_command('?', local_lang.where, langargs=True)
local_parser.add_command('!', local_lang.data, langargs=True)
local_parser.add_command('>/', local_lang.copy, langargs=True)
local_parser.add_command('mov', local_lang.copy, langargs=True)
local_parser.add_command('pyl', local_lang.python_line, langargs=True)
local_parser.add_command('jmp', local_lang.tp, langargs=True)
local_parser.add_command('mlt', local_lang.multyply, langargs=True)
local_parser.add_command('dvs', local_lang.divission, langargs=True)
local_parser.add_command('*', local_lang.multyply, langargs=True)
local_parser.add_command('/', local_lang.divission, langargs=True)
local_parser.add_command('@include', local_lang.include, langargs=True)
local_parser.add_command('@import', local_lang.import_func, langargs=True)
def use(arg_str: str=""):
    if arg_str in points:
        local_parser.parse(points[arg_str].replace('{', '').replace('}', ''), sep='/:')
local_parser.add_command('use', use, langargs=True)

@handle_error()
def jz(arg_str: str=""):
    if local_lang.tape[local_lang.pos] == 0:
        use(arg_str)

@handle_error()
def jnz(arg_str: str=""):
    if local_lang.tape[local_lang.pos] != 0:
        use(arg_str)
local_parser.add_command('jnz', jnz, langargs=True)
local_parser.add_command('jz', jz, langargs=True)

@handle_error()
def djo(arg_str: str=""):
    if local_lang.tape[local_lang.pos] == 1:
        use(arg_str)

@handle_error()
def djno(arg_str: str=""):
    if local_lang.tape[local_lang.pos] != 1:
        use(arg_str)
local_parser.add_command('jno', djno, langargs=True)
local_parser.add_command('jo', djo, langargs=True)
def fori(arg_str :str=""):
    inp = arg_str.split(',')
    u = int(inp[0])
    f = inp[1]
    for i in range(u):
        use(f)
local_parser.add_command('for', fori, langargs=True)
def start(arg_str :str=""):
    points = {}
local_parser.add_command('@start', start, langargs=True)

@handle_error()
def builder(text: str, path: str = 'build.py'):
    dlocal_lang = VoxelLang(100001)
    dlocal_parser = VoxelParser()
    
    # Регистрируем команды
    dlocal_parser.add_command('nxt', dlocal_lang.next, langargs=True)
    dlocal_parser.add_command('prv', dlocal_lang.prev, langargs=True)
    dlocal_parser.add_command('>', dlocal_lang.next, langargs=True)
    dlocal_parser.add_command('<', dlocal_lang.prev, langargs=True)
    dlocal_parser.add_command('pl', dlocal_lang.plus, langargs=True)
    dlocal_parser.add_command('mn', dlocal_lang.minus, langargs=True)
    dlocal_parser.add_command('+', dlocal_lang.plus, langargs=True)
    dlocal_parser.add_command('-', dlocal_lang.minus, langargs=True)
    dlocal_parser.add_command('set', dlocal_lang.set, langargs=True)
    dlocal_parser.add_command('erase', dlocal_lang.erase, langargs=True)
    dlocal_parser.add_command('!0', dlocal_lang.erase, langargs=True)
    dlocal_parser.add_command('out.char', dlocal_lang.output_char, langargs=True)
    dlocal_parser.add_command('out.num', dlocal_lang.output_num, langargs=True)
    dlocal_parser.add_command('out.str', dlocal_lang.print, langargs=True)
    dlocal_parser.add_command('out.next', dlocal_lang.output_next, langargs=True)
    dlocal_parser.add_command('in.char', dlocal_lang.input_char, langargs=True)
    dlocal_parser.add_command('in.num', dlocal_lang.input_num, langargs=True)
    dlocal_parser.add_command('', dlocal_lang.comentary, langargs=True)
    dlocal_parser.add_command('?', dlocal_lang.where, langargs=True)
    dlocal_parser.add_command('!', dlocal_lang.data, langargs=True)
    dlocal_parser.add_command('>/', dlocal_lang.copy, langargs=True)
    dlocal_parser.add_command('mov', dlocal_lang.copy, langargs=True)
    dlocal_parser.add_command('pyl', dlocal_lang.python_line, langargs=True)
    dlocal_parser.add_command('jmp', dlocal_lang.tp, langargs=True)
    dlocal_parser.add_command('mlt', dlocal_lang.multyply, langargs=True)
    dlocal_parser.add_command('dvs', dlocal_lang.divission, langargs=True)
    dlocal_parser.add_command('*', dlocal_lang.multyply, langargs=True)
    dlocal_parser.add_command('/', dlocal_lang.divission, langargs=True)
    dlocal_parser.add_command('@include', dlocal_lang.include, langargs=True)
    dlocal_parser.add_command('@import', dlocal_lang.include, langargs=True)

    def dstart(arg_str :str=""):
        points = {}
    dlocal_parser.add_command('@start', dstart, langargs=True)

    def duse(arg_str: str=""):
        if arg_str in points:
            dlocal_parser.parse(points[arg_str].replace('{', '').replace('}', ''), sep='/:')
    dlocal_parser.add_command('use', duse, langargs=True)
    
    @handle_error()
    def djz(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] == 0:
            duse(arg_str)
    
    @handle_error()
    def djnz(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] != 0:
            duse(arg_str)
    dlocal_parser.add_command('jnz', djnz, langargs=True)
    dlocal_parser.add_command('jz', djz, langargs=True)

    @handle_error()
    def djo(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] == 1:
            duse(arg_str)
    
    @handle_error()
    def djno(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] != 1:
            duse(arg_str)
    dlocal_parser.add_command('jno', djno, langargs=True)
    dlocal_parser.add_command('jo', djo, langargs=True)

    def dfori(arg_str :str=""):
        inp = arg_str.split(',')
        u = int(inp[0])
        f = inp[1]
        for i in range(u):
            duse(f)
    dlocal_parser.add_command('for', dfori, langargs=True)
    
    dstart()
    dlocal_parser.parse(text)
    dlocal_lang.build(path)



if __name__=="__main__":
    local_parser.parse(
    """
set=42;>/=100; = Копируем_в_ячейку_100;
pyl=print(f"Значение://s{tape[100]}");out.next;
pyl=tape[150] //- tape[100] * 2; = Умножаем_и_сохраняем;
pyl=print(f"Удвоенное://s{tape[150]}");
:voxel-test-{
    set=65 /:
    out.char
};
>;jz=test;
    """)
