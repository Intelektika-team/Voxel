from voxel.interface import *

ver_str = "v0.7.5 1st-beta stable"


class Errors:
    def SyntaxERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSyntax Error - {text}"))
        if exiting: raise SystemError()

    def SystemERROR(text :str, exiting :bool=True):
        print(color.red(f"\nSystem Error - {text}"))
        if exiting: raise SystemError()

    def ErrorHANDLER(text :str, exiting :bool=True):
        print(color.set(f"\nHandled Error - {text}", color.YELLOW))
        if exiting: raise SystemError()
    
    def NotFoundERROR(text :str, exiting :bool=True):
        print(color.set(f"\nNot found - {text}", color.YELLOW))
        if exiting: raise SystemError()
    
    def IncludeERROR(text :str, exiting :bool=True):
        print(color.set(f"\nError in include - {text}", color.YELLOW))
        if exiting: raise SystemError()

    def FileERROR(text :str, exiting :bool=True):
        print(color.set(f"\nFile error - {text}", color.YELLOW))
        if exiting: raise SystemError()

    def ParamERROR(text :str, exiting :bool=True):
        print(color.set(f"\nParameter error - {text}", color.YELLOW))
        if exiting: raise SystemError()

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
    return code.replace(' ', '')

constants = {}
points = {}
params = {}
pythonlines = {}
logs = []
logcount = 0

class VoxelParser:
    def __init__(self):
        self.commands={}
    
    def add_command(self, command :str, function :object, args :list=None, langargs :bool=False):
        self.commands[command] = {'f':function, 'a':args, 'la':langargs}
    
    def parse(self, code :str, sep :str=';'):
        rawcode = code.split(sep)
        code = code.replace(' ', '').split(sep) # Delete space and newlines from code
        newcode = []
        for i in code:
            newcode.append(i.replace('\n', ''))
        now = 0 # Line counter
        for i in newcode:
            now += 1
            worked = False
            try:
                try:
                    command = i.split('=', 1)[0] # Parse command
                    args = i.split('=', 1)[1] # Parse arguments
                except:
                    command = i
                    args = ''
                if command.startswith(':voxel'): # Parse voxels
                    try:
                        splitted = i.split('-', 2) # Split input
                    except:
                        raise SystemError()
                    points[splitted[1]] = splitted[2] # Set points[name] = function_body
                    worked = True
                
                
                elif command.startswith(':param'): # Parse parameters
                    try:
                        splitted = i.split('-', 1)
                        splitted1 = splitted[1].split('=', 1)
                        name = splitted1[0]
                        data = splitted1[1] # Data can be str (just string, like 'test'), int (just int, like '1'), or float (must start with 'f', like 'f10.14')
                        # Data convert from string
                        try: data = int(data)
                        except:
                            try: data = float(data.replace('f', '')) # Parse to float
                            except: data = str(data)
                    except Exception as e:
                        raise SystemError(f"Error in 'params' parser: {e}")
                    params[name] = data
                    
                    worked = True
                
                elif command.startswith(':const'): # Parse constants
                    try:
                        splitted = i.split('-', 1)
                        splitted1 = splitted[1].split('=', 1)
                        name = splitted1[0]
                        data = splitted1[1] # Data can be str (just string, like 'test'), int (just int, like '1') list (just array), or float (must starts with 'f', like 'f10.14')
                        # Data convert from string
                        try: data = int(data)
                        except:
                            try: data = float(data.replace('f', '')) # Parse to float
                            except: data = str(data)
                    except Exception as e:
                        raise SystemError(f"Error in 'const' parser: {e}")
                    constants[name] = data
                    
                    worked = True
                
                elif command.startswith(':pyl'): # Parse python multyline code
                    try:
                        splitted = rawcode[now-1].split('-', 2)
                        body = splitted[2].replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"').replace('/:', '\n').replace('}', '').replace('{', '')
                        name = splitted[1]
                        pythonlines[name] = body
                    except Exception as e:
                        raise SystemError(f"Error in 'math' parser: {e}")
                    constants[name] = data
                    worked = True
                
                elif command.startswith(':log.new'):  # Parse log.new
                    try:
                        global logcount
                        global logs
                        splitted = i.split('(', 1)
                        if splitted[1].endswith(')'): pass
                        else: Errors.SyntaxERROR("Log.new error: log new must be look like ':log.new(text)'.")
                        info = rawcode[now-1].split('(')[1].replace(')', '').replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"')
                        text = f'=== log {logcount}: {info} ==='
                        logs.append(text)
                        logcount += 1
                    except Exception as e:
                        raise SystemError(f"Error in 'log.new' parser: {e}")
                    worked = True
                
                elif command.startswith(':log.out'):  # Parse log.output
                    try:
                        print("\n".join(logs))
                    except Exception as e:
                        raise SystemError(f"Error in 'log.out' parser: {e}")
                    worked = True

                elif command.startswith(':sys.out'):  # Parse system.output
                    try:
                        splitted = i.split('(', 1)
                        if splitted[1].endswith(')'): pass
                        else: Errors.SyntaxERROR("Sys.out error: sys out must be look like ':sys.out(text)'.")
                        info = rawcode[now-1].split('(')[1].replace(')', '').replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"')
                        print(info, end='')
                        
                    except Exception as e:
                        raise SystemError(f"Error in 'sys.out' parser: {e}")
                    worked = True
                
                elif command.startswith(':exit'):  # Parse exit
                    break

                elif command in self.commands:
                    self.commands[command]['f']("".join(self.commands[command]['a']) if not self.commands[command]['la'] else args)
                    worked = True
                elif worked == False:
                    Errors.SyntaxERROR(f"Unknown keyword '{command}' in line {now}")
                else:
                    Errors.SystemERROR("PARSE ERROR.")
            except Exception as e:
                Errors.ErrorHANDLER(f"Error in line {now} - {e}")



class VoxelLang:
    def __init__(self, length: int):
        self.length = length
        self.reset()

    def reset(self):
        self.tape = {}
        # Create tape with -(length/2) to length/2 indexes
        self.gentape(self.length)
        self.pos = 0  # Start position in centre of tape
        self.code = []
        self.variables = {}
        self.libs = {"tape":{"lib":f"""tape, pos = {self.tape}, {self.pos}


@handle_error()
def getpos():
    return pos

@handle_error()
def setpos(new_pos):
    global pos
    pos = new_pos

@handle_error()
def find_value(value):  # Find value in tape
    for key, val in tape.items():
        if val == value:
            return key
    return None

@handle_error()
def tape_range():  
    return min(tape.keys()), max(tape.keys())


@handle_error()
def data():
    return tape[pos]

@handle_error()
def set(arg):
    tape[pos] = arg
""", "used":False},"base":{"lib":
"""
def wait(delay:int):
    time.sleep(delay*0.001)

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

def cls():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

""", "used":False}, "stdio":
        {"lib":"""

# Standart pyl library 
class color:
    # Base colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Text styles
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

""", "used":False},



"first_program":{"lib":
"""
def main(user :str='Guest'):
    print(f'Hello, {user}!')
""", "used":False}
}
        

        self.code.append(
"""
import os, platform, time
""")

    @handle_error()
    def optimal_type(self, rawdata: str):
        data = rawdata.strip()  # Удаляем лишние пробелы
    
        # Обработка списков/выражений с квадратными скобками
        if data.startswith('[') and data.endswith(']'):
            try:
                # Безопасная замена специальных символов
                parsed_data = data.replace('?', str(self.pos))\
                                .replace('!', str(self.tape[self.pos]))
                # Используем ast.literal_eval вместо eval для безопасности
                import ast
                result = ast.literal_eval(parsed_data)
            except (ValueError, SyntaxError, IndexError):
                result = data
            return result

        # Обработка чисел с плавающей точкой
        if '.' in data:
            try:
                return float(data)
            except ValueError:
                return data

        # Обработка целых чисел и строк
        try:
            return int(data)
        except ValueError:
            return rawdata

    @handle_error()
    def calc_variables(self):
        variables = {}
        self.alreadywas = []
        
        # Обрабатываем параметры (должны быть в нижнем регистре)
        for key in params:
            if key != key.lower():
                raise SystemError('Params must be lowercased.')
            variables[key.lower()] = params[key]
        
        # Обрабатываем константы (должны быть в верхнем регистре)
        for key in constants:
            if key != key.upper():
                raise SystemError('Constants must be uppercased')
            value = constants[key]
            variables[key.upper()] = value
            
            # Форматируем значение в зависимости от типа
            if isinstance(value, str):
                # Экранирование специальных символов для строк
                if '\n' in value:
                    formatted_value = f"'''{value}'''"
                formatted_value = repr(value)
            else:
                formatted_value = str(value)
            
            if key.upper() in self.alreadywas: pass
            else: self.code.append(f"{key.upper()} = {formatted_value}")
            self.alreadywas.append(key.upper()) 
        
        return variables

    @handle_error()
    def data(self, arg_str:str =""):
        self.variables = self.calc_variables()
        result = arg_str
        if arg_str in self.variables:
            data = self.variables[arg_str]
            if data == "?":
                result = self.pos
            elif data == "!":
                result = self.tape[self.pos]
            else:
                result = data
            return self.optimal_type(str(result))
        else:
            return str(result)

    
    @handle_error()
    def gentape(self, length :int):
        for i in range(length):
            self.tape[i-(length//2)] = 0
        
    @handle_error()
    def code_append(self, arg_str :str=''):
        if arg_str in pythonlines:
            self.code.append(pythonlines[arg_str])
        else:
            pass

    @handle_error()
    def include(self, arg_str :str=''):
        try: 
            if arg_str in self.libs:
                using = self.libs[arg_str]['used']
                if using==False:
                    self.code.append(self.libs[arg_str]['lib'])
                    self.libs[arg_str]['used'] = True
                elif using==True:
                    Errors.IncludeERROR(f'Library {self.libs[arg_str]} - Already use: {using} in {arg_str}')
            else:
                Errors.NotFoundERROR(f"Library {arg_str} isn't found.")
        except Exception as e:
            Errors.IncludeERROR(f'Include error: {e}, in {arg_str}')

    @handle_error()
    def import_func(self, arg_str :str=''):
        inp = arg_str.split(',')
        try: 
            self.code.append(f'import _dependencies_.{inp[0]} as {inp[1]}')
        except Exception as e:
            Errors.IncludeERROR(f'Import error: {e}')
    
    @handle_error()
    def retape(self, arg_str :str=''):
        n = self.data(arg_str)
        self.gentape(int(n))
        self.code.append(f"tape = {self.tape}")

    @handle_error()
    def next(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.pos += n
        self.code.append(f"pos += {n}")
    
    @handle_error()
    def prev(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.pos -= n
        self.code.append(f"pos -= {n}")
    
    @handle_error()
    def plus(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.tape[self.pos] += n
        self.code.append(f"tape[pos] += {n}")
    
    @handle_error()
    def minus(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))

        self.tape[self.pos] -= n
        self.code.append(f"tape[pos] -= {n}")
    
    @handle_error()
    def set(self, arg_str: str):
        start = arg_str.startswith("\"")
        args = arg_str.replace('\"', '').replace('//s', ' ').replace('//tab', '    ').replace('//n', '\n').replace('//-', '=') if start else self.data(arg_str)
        self.tape[self.pos] = args
        self.code.append(f"tape[pos] = {args}")
    
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
        t = chr(int(self.tape[self.pos]))
        print(t, end='')
        self.code.append(f"print(chr(int(tape[pos])), end='')")
    
    @handle_error()
    def output_now(self, arg_str: str = ""):
        t = self.tape[self.pos]
        print(t, end='')
        self.code.append(f"print(tape[pos], end='')")

    @handle_error()
    def output_next(self, arg_str: str = ""):
        print()
        self.code.append(f"print()")

    @handle_error()
    def print(self, arg_str: str = ""):
        start = arg_str.startswith("\"")
        form = arg_str.startswith("//form")
        if start:
            args = arg_str.replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace('\"', '').replace("//'", '"')
        elif form:
            data = str(self.data(arg_str.replace("//form", '')))
            args = data.replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace('\"', '').replace("//'", '"')
        else:
            args = self.data(arg_str)
        self.code.append(f"print('{args}', end='')")
        print(args, end='')
    
    @handle_error()
    def copy(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.tape[n] = self.tape[self.pos]
        self.code.append(f"tape[{n}] = tape[pos]")
    
    @handle_error()
    def python_line(self, arg_str: str = ""):
        if arg_str == "": s = ''
        else:
            s = str(self.data(arg_str))
        arg_str = s.replace('//n', '\n').replace('//tab', '    ').replace('//s', ' ').replace('//-', '=')
        self.code.append(f"{arg_str}")
    
    @handle_error()
    def input_char(self, arg_str: str = ""):
        char = ord(input(arg_str)[0])
        self.tape[self.pos] = char
        self.code.append(f"tape[pos] = ord(input({arg_str})[0])")
    
    @handle_error()
    def set_param(self, arg_str: str=""):
        inp = arg_str.split(',')
        if inp[0] in params:
            try: params[inp[0]] = inp[1]
            except Exception as e:
                Errors.SystemERROR(f"{e}")
        else:
            Errors.ParamERROR(f"Parameter {inp[0]} not found.")

    @handle_error()
    def topython_param(self, arg_str: str = ""):
        self.data('update')
        if arg_str in self.variables:
            types = str(type(params[arg_str])).replace("<class '", '').replace("'>", '')
            if types == 'str':
                self.code.append(f"{arg_str} = '''{params[arg_str]}'''")
            else:
                self.code.append(f"{arg_str} = {params[arg_str]}")
        else:
            Errors.ParamERROR(f"Parameter {arg_str} not found.")

    @handle_error()
    def plus_param(self, arg_str: str=""):
        inp = arg_str.split(',')
        if inp[0] in params:
            datan = self.data(inp[0])
            datan1 = self.data(inp[1])
            try:
                params[inp[0]] = int(datan) + int(datan1)
            except Exception as e:
                try: params[inp[0]] += datan1
                except:
                    Errors.SystemERROR(f"{e}")
        else:
            Errors.ParamERROR(f"Parameter {inp[0]} not found.")
    
    @handle_error()
    def minus_param(self, arg_str: str=""):
        inp = arg_str.split(',')
        if inp[0] in params:
            try: params[inp[0]] -= int(self.data(inp[1])) if isinstance(params[inp[0]], int) or isinstance(params[inp[0]], float) else self.data(inp[1])
            except Exception as e:
                Errors.SystemERROR(f"{e}")
        else:
            Errors.ParamERROR(f"Parameter {inp[0]} not found.")
    
    @handle_error()
    def divission_param(self, arg_str: str=""):
        inp = arg_str.split(',')
        if inp[0] in params:
            try: params[inp[0]] /= int(self.data(inp[1])) if isinstance(params[inp[0]], int) or isinstance(params[inp[0]], float) else self.data(inp[1])
            except Exception as e:
                Errors.SystemERROR(f"{e}")
        else:
            Errors.ParamERROR(f"Parameter {inp[0]} not found.")
    
    @handle_error()
    def multiply_param(self, arg_str: str=""):
        inp = arg_str.split(',')
        if inp[0] in params:
            try: params[inp[0]] *= int(self.data(inp[1])) if isinstance(params[inp[0]], int) or isinstance(params[inp[0]], float) else self.data(inp[1])
            except Exception as e:
                Errors.SystemERROR(f"{e}")
        else:
            Errors.ParamERROR(f"Parameter {inp[0]} not found.")
    
    @handle_error()
    def type_param(self, arg_str: str=""):
        self.data('update')
        if arg_str in self.variables:
            types = str(type(self.data(arg_str))).replace("<class '", '').replace("'>", '')
            print(types, end='')
            self.code.append(f"print({types}, end='')")
        else:
            Errors.ParamERROR(f"Parameter {arg_str} not found.")
    
    @handle_error()
    def input_num(self, arg_str: str = ""):
        self.tape[self.pos] = int(input(arg_str))
        self.code.append(f"tape[pos] = int(input({arg_str}))")
    
    @handle_error()
    def input_str(self, arg_str: str = ""):
        self.tape[self.pos] = str(input(arg_str))
        self.code.append(f"tape[pos] = str(input({arg_str}))")

    @handle_error()
    def comentary(self, arg_str: str = ""):
        self.code.append(f"# {arg_str}")

    @handle_error()
    def multyply(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.tape[self.pos] *= n
        self.code.append(f"tape[pos] *= {n}")
    
    @handle_error()
    def bash(self, arg_str: str = ""):
        try:
            command = arg_str.replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace('\"', '').replace("//'", '"')
            os.system(command)
            self.code.append(f'os.system({command})')
        except Exception as e:
            print(f"Error in 'bash':{e}")

    @handle_error()
    def divission(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.tape[self.pos] //= int(n)
        self.code.append(f"tape[pos] //= {n}")
    
    @handle_error()
    def tp(self, arg_str: str = ""):
        if arg_str == "": n = 1 
        else:
            n = int(self.data(arg_str))
        self.pos = n
        self.code.append(f"pos = {n}")
        
    @handle_error()
    def swap(self, arg_str: str=""):
        if arg_str == "": pos = 1 
        else:
            pos = int(self.data(arg_str))
        current = self.tape[self.pos]
        new = self.tape[pos]
        self.tape[self.pos] = new
        self.tape[pos] = current
        self.code.append(f"""
_current = tape[pos]
_new = tape[{pos}]
tape[pos] = _new
tape[{pos}] = _current
""")


    @handle_error()
    def where(self, arg_str: str = ""):
        self.code.append(f"print(pos, end='')")
        print(self.pos, end='')
    
    @handle_error()
    def ndata(self, arg_str: str = ""):
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
        
        # Create system dit
        cache_dir = os.path.join(os.getcwd(), '_voxel_')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Make full path
        full_file_path = os.path.join(cache_dir, path)
        full_config_path = os.path.join(os.getcwd(), 'init.voxel')

        with open(full_config_path, 'r') as f:
            file = f.read()
            config = file.split(';')
        print('Configurating... \n=', end='')
        result = []
        try:
            description = config[5].split('-', 1)[1] ;print('=', end='')
            description = description[1:] if description[0] == ' ' else description ;print('=', end='')
            author = config[4].split('-', 1)[1] ;print('=', end='')
            author = author[1:] if author[0] == ' ' else author ;print('=', end='')
            version = config[3].split('-', 1)[1] ;print('=', end='')
            version = version[1:] if version[0] == ' ' else version ;print('=', end='')
            verlang = config[2].split('-', 1)[1] ;print('=', end='')
            verlang = verlang[1:] if verlang[0] == ' ' else verlang ;print('=', end='')
            projpath = config[0].split('-', 1)[1] ;print('=', end='')
            projpath = projpath[1:] if projpath[0] == ' ' else projpath ;print('=', end='')
        except Exception as e: 
            if str(e).strip() == 'list index out of range'.strip(): Errors.FileERROR(f"\nConfig is so old or incorrect")
            else: Errors.FileERROR(f"\nConfig parse error: {e}")
        if verlang.strip() != ver_str.strip(): Errors.SystemERROR(f"\nLanguage version isn't support. Current version: {ver_str}")
        print('\nConfigure compleate...')


        # Generate and write code to build file
        code = "\n".join(self.getcode())
        logsr = '\n'.join(logs)
        result = "\n".join([f"'''\n=== LOGS ===\n{logsr}\n=== LOGS ===\n'''", '# MARK: Constants', f'AUTHOR = "{author}"; VERSION = "{version}"; LANGUAGE = "{verlang}"; PATH = "{projpath}"', f"DESCRIPTION = '''{description}'''", '# MARK: Code', code])
        
        with open(full_file_path, 'w') as f:
            f.write(result)
        
        print(f'Done. File saved to: {full_file_path}')
    
    
    
local_lang = VoxelLang(100001)
local_parser = VoxelParser()
    
# Регистрируем команды
local_parser.add_command('nxt', local_lang.next, langargs=True)
local_parser.add_command('prv', local_lang.prev, langargs=True)
local_parser.add_command('swp', local_lang.swap, langargs=True)
local_parser.add_command('pls', local_lang.plus, langargs=True)
local_parser.add_command('mns', local_lang.minus, langargs=True)
local_parser.add_command('set', local_lang.set, langargs=True)
local_parser.add_command('ers', local_lang.erase, langargs=True)
local_parser.add_command('mov', local_lang.copy, langargs=True)
local_parser.add_command('pyl', local_lang.python_line, langargs=True)
local_parser.add_command('jmp', local_lang.tp, langargs=True)
local_parser.add_command('mlt', local_lang.multyply, langargs=True)
local_parser.add_command('dvs', local_lang.divission, langargs=True)
local_parser.add_command('ppl', local_lang.plus_param, langargs=True)
local_parser.add_command('pmn', local_lang.minus_param, langargs=True)
local_parser.add_command('pst', local_lang.set_param, langargs=True)
local_parser.add_command('pdv', local_lang.divission_param, langargs=True)
local_parser.add_command('pmp', local_lang.minus_param, langargs=True)
local_parser.add_command('ptp', local_lang.topython_param, langargs=True)
local_parser.add_command('bash', local_lang.bash, langargs=True)
local_parser.add_command('pylpaste', local_lang.code_append, langargs=True)
local_parser.add_command('plps', local_lang.code_append, langargs=True)
local_parser.add_command('>', local_lang.next, langargs=True)
local_parser.add_command('<', local_lang.prev, langargs=True)
local_parser.add_command('+', local_lang.plus, langargs=True)
local_parser.add_command('-', local_lang.minus, langargs=True)
local_parser.add_command('?', local_lang.where, langargs=True)
local_parser.add_command('!', local_lang.ndata, langargs=True)
local_parser.add_command('>/', local_lang.copy, langargs=True)
local_parser.add_command('*', local_lang.multyply, langargs=True)
local_parser.add_command('/', local_lang.divission, langargs=True)
local_parser.add_command('<>', local_lang.swap, langargs=True)
local_parser.add_command('!0', local_lang.erase, langargs=True)
local_parser.add_command('out.char', local_lang.output_char, langargs=True)
local_parser.add_command('out.now', local_lang.output_now, langargs=True)
local_parser.add_command('out.str', local_lang.print, langargs=True)
local_parser.add_command('out.next', local_lang.output_next, langargs=True)
local_parser.add_command('out.ptype', local_lang.type_param, langargs=True)
local_parser.add_command('in.char', local_lang.input_char, langargs=True)
local_parser.add_command('in.num', local_lang.input_num, langargs=True)
local_parser.add_command('in.str', local_lang.input_str, langargs=True)
local_parser.add_command('', local_lang.comentary, langargs=True)
local_parser.add_command('//', local_lang.comentary, langargs=True)
local_parser.add_command('@include', local_lang.include, langargs=True)
local_parser.add_command('@import', local_lang.import_func, langargs=True)
local_parser.add_command('@retape', local_lang.retape, langargs=True)
local_parser.add_command('@updata', local_lang.data, args='update') #for update data

def use(arg_str: str=""):
    if arg_str in points:
        local_parser.parse(points[arg_str].replace('{', '').replace('}', ''), sep='/:')
    else:
        Errors.NotFoundERROR(f"Voxel {arg_str} is not found.")
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
def jo(arg_str: str=""):
    if local_lang.tape[local_lang.pos] == 1:
        use(arg_str)

@handle_error()
def jno(arg_str: str=""):
    if local_lang.tape[local_lang.pos] != 1:
        use(arg_str)
@handle_error()
def jf(arg_str :str=""):
    inp = arg_str.split(',')
    if local_lang.tape[local_lang.pos] == local_lang.data(inp[0]):
        use(inp[1])

@handle_error()
def jnf(arg_str: str = ""):
    inp = arg_str.split(',')
    if local_lang.tape[local_lang.pos] != local_lang.data(inp[0]):
        use(inp[1])
local_parser.add_command('jno', jno, langargs=True)
local_parser.add_command('jo', jo, langargs=True)
local_parser.add_command('jnf', jnf, langargs=True)
local_parser.add_command('jf', jf, langargs=True)
def fori(arg_str :str=""):
    inp = arg_str.split(',')
    u = int(local_lang.data(inp[0]))
    f = inp[1]
    for i in range(u):
        use(f)
def drelog(arg_str :str=""):
    global logs
    logs = []
    
    local_lang.reset()
local_parser.add_command('@relog', drelog)
local_parser.add_command('for', fori, langargs=True)
def start(arg_str :str=""):
    global params
    global points
    global constants
    points = {}
    constants = {}
    params = {}
    local_lang.reset()
local_parser.add_command('@start', start, langargs=True)


@handle_error()
def builder(text: str, path: str = 'build.py'):
    dlocal_lang = VoxelLang(100001)
    dlocal_parser = VoxelParser()
    
    # Регистрируем команды
    dlocal_parser.add_command('nxt', dlocal_lang.next, langargs=True)
    dlocal_parser.add_command('prv', dlocal_lang.prev, langargs=True)
    dlocal_parser.add_command('>', dlocal_lang.next)
    dlocal_parser.add_command('<', dlocal_lang.prev)
    dlocal_parser.add_command('pls', dlocal_lang.plus, langargs=True)
    dlocal_parser.add_command('mns', dlocal_lang.minus, langargs=True)
    dlocal_parser.add_command('+', dlocal_lang.plus, langargs=True)
    dlocal_parser.add_command('-', dlocal_lang.minus, langargs=True)
    dlocal_parser.add_command('set', dlocal_lang.set, langargs=True)
    dlocal_parser.add_command('ers', dlocal_lang.erase, langargs=True)
    dlocal_parser.add_command('!0', dlocal_lang.erase, langargs=True)
    dlocal_parser.add_command('out.char', dlocal_lang.output_char, langargs=True)
    dlocal_parser.add_command('out.now', dlocal_lang.output_now, langargs=True)
    dlocal_parser.add_command('out.str', dlocal_lang.print, langargs=True)
    dlocal_parser.add_command('out.next', dlocal_lang.output_next, langargs=True)
    dlocal_parser.add_command('in.char', dlocal_lang.input_char, langargs=True)
    dlocal_parser.add_command('in.num', dlocal_lang.input_num, langargs=True)
    dlocal_parser.add_command('in.str', dlocal_lang.input_str, langargs=True)
    dlocal_parser.add_command('', dlocal_lang.comentary, langargs=True)
    dlocal_parser.add_command('//', dlocal_lang.comentary, langargs=True)
    dlocal_parser.add_command('?', dlocal_lang.where, langargs=True)
    dlocal_parser.add_command('!', dlocal_lang.ndata, langargs=True)
    dlocal_parser.add_command('>/', dlocal_lang.copy, langargs=True)
    dlocal_parser.add_command('mov', dlocal_lang.copy, langargs=True)
    dlocal_parser.add_command('pyl', dlocal_lang.python_line, langargs=True)
    dlocal_parser.add_command('jmp', dlocal_lang.tp, langargs=True)
    dlocal_parser.add_command('mlt', dlocal_lang.multyply, langargs=True)
    dlocal_parser.add_command('dvs', dlocal_lang.divission, langargs=True)
    dlocal_parser.add_command('ppl', dlocal_lang.plus_param, langargs=True)
    dlocal_parser.add_command('pmn', dlocal_lang.minus_param, langargs=True)
    dlocal_parser.add_command('pst', dlocal_lang.set_param, langargs=True)
    dlocal_parser.add_command('pdv', dlocal_lang.divission_param, langargs=True)
    dlocal_parser.add_command('pmp', dlocal_lang.minus_param, langargs=True)
    dlocal_parser.add_command('ptp', dlocal_lang.topython_param, langargs=True)
    dlocal_parser.add_command('bash', dlocal_lang.bash, langargs=True)
    dlocal_parser.add_command('pylpaste', dlocal_lang.code_append, langargs=True)
    dlocal_parser.add_command('plps', dlocal_lang.code_append, langargs=True)
    dlocal_parser.add_command('out.ptype', dlocal_lang.type_param, langargs=True)
    dlocal_parser.add_command('*', dlocal_lang.multyply, langargs=True)
    dlocal_parser.add_command('/', dlocal_lang.divission, langargs=True)
    dlocal_parser.add_command('<>', dlocal_lang.swap, langargs=True)
    dlocal_parser.add_command('swp', dlocal_lang.swap, langargs=True)
    dlocal_parser.add_command('@include', dlocal_lang.include, langargs=True)
    dlocal_parser.add_command('@import', dlocal_lang.import_func, langargs=True)
    dlocal_parser.add_command('@retape', dlocal_lang.retape, langargs=True)
    dlocal_parser.add_command('@updata', dlocal_lang.data, args='update') #for update data
    def drelog(arg_str :str=""):
        global logs
        logs = []
    dlocal_parser.add_command('@relog', drelog)

    def dstart(arg_str :str=""):
        global params
        global points
        global constants
        points = {}
        params = {}
        constants = {}
        
        dlocal_lang.reset()
    dlocal_parser.add_command('@start', dstart, langargs=True)

    def duse(arg_str: str=""):
        if arg_str in points:
            dlocal_parser.parse(points[arg_str].replace('{', '').replace('}', ''), sep='/:')
        else:
            Errors.NotFoundERROR(f"Voxel '{arg_str}' is not found.")
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

    @handle_error()
    def djf(arg_str :str=""):
        inp = arg_str.split(',')
        if dlocal_lang.tape[dlocal_lang.pos] == dlocal_lang.data(inp[0]):
            duse(inp[1])

    @handle_error()
    def djnf(arg_str: str = ""):
        inp = arg_str.split(',')
        if dlocal_lang.tape[dlocal_lang.pos] != dlocal_lang.data(inp[0]):
            duse(inp[1])
    dlocal_parser.add_command('jno', djno, langargs=True)
    dlocal_parser.add_command('jo', djo, langargs=True)
    dlocal_parser.add_command('jnf', djnf, langargs=True)
    dlocal_parser.add_command('jf', djf, langargs=True)

    def dfori(arg_str :str=""):
        inp = arg_str.split(',')
        u = int(dlocal_lang.data(inp[0]))
        f = inp[1]
        for i in range(u):
            duse(f)
    dlocal_parser.add_command('for', dfori, langargs=True)
    

    dlocal_parser.parse(text)
    dlocal_lang.build(path)



if __name__=="__main__":
    local_parser.parse(
"""
//= Start;
:log.new(STARTING...);
nxt=10; pls=12;
:param-test=?;
:param-f=10;
out.str=test; out.next;
:voxel-print_a-{
    out.str=A /:
};
for=f, print_a; out.next;
out.ptype=f; 
out.next;
:param-float=f10.7;
out.ptype=float;
out.next; @start;
:param-move=11;
?; !; nxt=move; 
out.next; @start;
:param-count=26;
:param-char=65; 
:voxel-print_char-{
    set=char /:
    out.char /:
    ppl=char, 1 /:
};
for=count, print_char; 
out.next; @start; 
:param-int=10; out.ptype=int;
:param-float=f6.16; out.ptype=float;
:param-str=//n test //s string; out.ptype=str; out.str=//form str;
out.next; @start;
//= Hello_user!_That's_the_basic_structure_of_voxel_programm._We_recomended_to_write_code_like_that.;

:voxel-setup-{
    @include= tape /:
    @include= first_program /:
    :param-test=10 /:
};
:voxel-s-{
    out.str=test /:
};

:voxel-main-{
    use= setup/:
    use= s/:
};
out.str= "test";
use= main;
@start;
>; >; ?; out.next;
:param-list=[1, ?, 'value'];
out.str=list; out.ptype=list; out.str="//n text //s value";
:const-TEST=19; out.ptype = TEST;
out.str=//form TEST; :const-TEST2=10; @updata;
:sys.out(Some text);
:log.new(ENDING...);
:sys.out(\n); :log.out;
//= End;

//= WARNING - comentary always must starts from //= and ends with;
//= WARNING - comments like '// ...' do not exist;
:voxel-if_zero-{
    out.str="Zero!" /:+
};

:voxel-if_not_zero-{
    out.str="Not zero!" /:-
};
jz=if_zero;
jnz=if_not_zero; 
@start;
:pyl-new-{
e = 2+1
print(e)
}; pylpaste = new;
bash= echo //s zxy;
""")
