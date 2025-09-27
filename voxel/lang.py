from voxel.interface import *

ver_str = "v0.7.8 1st-beta prod"
devmode = False


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

    def ParseERROR(text :str, exiting :bool=True, fullexit :bool=False):
        print(color.set(f"\nParser error - {text}", color.YELLOW))
        if exiting: raise SystemError()
        if fullexit: exit(100)
    
    def DevERROR(text :str, exiting :bool=True, fullexit :bool=False):
        print(color.set(f"\nDeveloper error - {text}", color.YELLOW))
        if exiting: raise SystemError()
        if fullexit: exit(100)
    
    def ErrorERROR(text :str, exiting :bool=True):raise SystemError()

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


class Develop:
    def DevlogFUNCTION(text :str, colors :list = [color.BLUE]):
        if devmode: print(f'{"".join(colors)}===--- DEVELOP: {text}{color.RESET}')
    
    def DevfunctionPARSE(com:str):
        Develop.DevlogFUNCTION(com)
        if com == '?':
            print(f'DEVMODE: {devmode}')
        elif com == 'f':
            devmode = False
            print(f'DEVMODE: {devmode}')
        elif com == 't':
            devmode = True
            print(f'DEVMODE: {devmode}')
        else:
            Errors.DevERROR(f'UNKNOWN DEV COMMAND: {com}')


constants = {}
points = {}
params = {}
pythonlines = {}
logs = []
logcount = 0


def none(*args, **kwargs):
    pass


class VoxelParser:
    def __init__(self):
        self.commands={'NONE':{'f':none, 'a':'', 'la':True, 'br':True}}
    
    def add_command(self, command :str, function :object, args :list=None, langargs :bool=False, bracketsavailable :bool=False):
        self.commands[command] = {'f':function, 'a':args, 'la':langargs, 'br':bracketsavailable}
    
    def printallcommands(self):
        now = 0
        for i in self.commands:
            now+=1
            f:object = self.commands[i]["f"]
            print(f'Command {now}: {i}, func: {f}')
    
    def parser(self, i :str, code, raw :str=None, index :int=0):
        if i.strip() != '': 
            try:
                command = i.split('=', 1)[0] # Parse command
                args = str(i.split('=', 1)[1]).replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"') # Parse arguments
            except:
                error = 'NONE'
                try:
                    if i.endswith(')'):pass
                    else:Errors.ErrorERROR()
                    spl = i.split('(', 1)
                    Develop.DevlogFUNCTION(spl, [color.RED])
                    ncommand = spl[0] # Parse command
                    if raw is None:
                        nargs = str(spl[0:-1]).replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"').replace("//(", ')') # Parse arguments
                    else: # Block in development
                        nargs = str(spl[1][0:-1]).replace('//s', ' ').replace('//n', '\n').replace('//tab', '    ').replace('//-', '=').replace("//'", '"').replace("//(", ')') # Parse arguments
                        Develop.DevlogFUNCTION(f'{index}: {code[index]}', [color.GREEN])
                    Develop.DevlogFUNCTION(ncommand, nargs)
                    if ncommand in self.commands:
                        cinfo = self.commands[ncommand]
                        Develop.DevlogFUNCTION(cinfo, [color.GREEN])
                        if cinfo['br']:
                            args = nargs
                            command = ncommand
                        else: 
                            textoferror = 'Error in arguments finder. Command is not support "()"'
                            Errors.ErrorERROR()
                            error = textoferror
                    else:
                        Errors.ErrorERROR()

                except: 
                    if error == 'NONE': pass
                    else: Errors.ParseERROR(error)
                    Develop.DevlogFUNCTION('NONEPARSE')
                    command = i
                    args = ''
        else:
            command = 'NONE'
            args = ''
        try: db = self.commands[command]
        except: db = 'NONE'
        Develop.DevlogFUNCTION(f'Parse log- \nline: {i}, \nargs & command: {args, command}\n debug: {db}')
        return command, args
    
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
                command, args = self.parser(i, code, rawcode, now)
            

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
                
                elif command.startswith('NONE'): 
                    worked = True
                    pass
                
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
                        Develop.DevlogFUNCTION(body, pythonlines)
                    except Exception as e:
                        raise SystemError(f"Error in 'pyl' parser: {e}")
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
                Errors.ErrorHANDLER(f"Error in line {now} ({i}) - {e}")



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
        self.libs = {"tape":{"lib":f"""tape= {self.tape}""", "used":False},
"base":{"lib":
"""
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

def wait(delay:int):
    time.sleep(delay*0.001)

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
def handle_error(exiting=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise SystemError(str(e))
                if exiting: exit()
        return wrapper
    return decorator
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
    def tapeload(self, arg_str :str=''):
        try:
            import _voxel_._system_.tape as t
            self.tape = t.tape
        except:
            try:
                import _system_.tape as t
                self.tape = t.tape
            except Exception as e: print(f"EXCEPT: {e}")
        self.code.append('''
try: 
    import _system_.tape as t 
    tape = t.tape 
except: print("EXCEPT")
''')
    
    @handle_error()
    def tapesave(self, arg_str :str=''):
        with open('_voxel_/_system_/tape.py', 'w') as tape:
            tape.write(f'tape = {self.tape}')
        self.code.append("""try: 
    with open('_system_/tape.py', 'w') as tp: 
        tp.write(f'tape = {tape}')
except: 
    with open('_voxel_/_system_/tape.py', 'w') as tp: 
        tp.write(f'tape = {tape}')""")
    
    @handle_error()
    def tapeinclude(self, arg_str :str=''):
        try:
            import _voxel_._system_.tape as t
            t.tape = self.tape
        except:
            try:
                import _system_.tape as t
                t.tape = self.tape
            except Exception as e: print(f"EXCEPT: {e}")
        self.code.append("""try:
    with open('_system_/tape.py', 'r') as tp:
        tape = tp.read()
except:print("EXCEPT")""")
    
    @handle_error()
    def tapereset(self, arg_str :str=''):
        self.retape(100001)
        self.code.append(f"""try:
    with open('_system_/tape.py', 'w') as tp:
        tape = tp.write('{self.tape}')
except:print("EXCEPT")""")
    
    @handle_error()
    def delay(self, arg_str :str=''):
        try:
            delay = int(arg_str) * 0.001
            self.code.append(f'time.sleep({delay})')
        except Exception as e:
            Errors.SyntaxERROR(f"Error in 'delay' with args [{arg_str}]: {e}")
    
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
        result = "\n".join([f"'''\n=== LOGS ===\n{logsr}\n=== LOGS ===\n'''", '# MARK: Constants', f'AUTHOR = "{author}"; VERSION = "{version}"; LANGUAGE = "{verlang}"; PATH = "{projpath}"; pos = {self.pos}', f"DESCRIPTION = '''{description}'''", '# MARK: Code', code])
        
        with open(full_file_path, 'w') as f:
            f.write(result)
        
        print(f'Done. File saved to: {full_file_path}')
    

def init(dlocal_lang :VoxelLang, d2local_parser :VoxelParser):
    # Регистрируем команды
    def drelog(arg_str :str=""):
        global logs
        logs = []
    
    def dstart(arg_str :str=""):
        global params
        global points
        global constants
        points = {}
        params = {}
        constants = {}
        dlocal_lang.reset()
    
    def duse(arg_str: str=""):
        if arg_str in points:
            d2local_parser.parse(points[arg_str].replace('{', '').replace('}', ''), sep='/:')
        else:
            Errors.NotFoundERROR(f"Voxel '{arg_str}' is not found.")

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

    def dfori(arg_str :str=""):
        inp = arg_str.split(',')
        u = int(dlocal_lang.data(inp[0]))
        f = inp[1]
        for i in range(u):
            duse(f)
    
    @handle_error()
    def djz(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] == 0:
            duse(arg_str)
    
    @handle_error()
    def djnz(arg_str: str=""):
        if dlocal_lang.tape[dlocal_lang.pos] != 0:
            duse(arg_str)
    
    # Base comands
    d2local_parser.add_command('nxt', dlocal_lang.next, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('prv', dlocal_lang.prev, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pls', dlocal_lang.plus, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('mns', dlocal_lang.minus, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('set', dlocal_lang.set, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('ers', dlocal_lang.erase, langargs=True, bracketsavailable=True)
    # Io
    d2local_parser.add_command('out.char', dlocal_lang.output_char, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('out.now', dlocal_lang.output_now, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('out.str', dlocal_lang.print, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('out.next', dlocal_lang.output_next, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('out.ptype', dlocal_lang.type_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('in.char', dlocal_lang.input_char, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('in.num', dlocal_lang.input_num, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('in.str', dlocal_lang.input_str, langargs=True, bracketsavailable=True)
    # Commands
    d2local_parser.add_command('mov', dlocal_lang.copy, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pyl', dlocal_lang.python_line, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jmp', dlocal_lang.tp, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('mlt', dlocal_lang.multyply, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('dvs', dlocal_lang.divission, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('ppl', dlocal_lang.plus_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pmn', dlocal_lang.minus_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pst', dlocal_lang.set_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pdv', dlocal_lang.divission_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pmp', dlocal_lang.minus_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('ptp', dlocal_lang.topython_param, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('bash', dlocal_lang.bash, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('delay', dlocal_lang.delay, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('pylpaste', dlocal_lang.code_append, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('plps', dlocal_lang.code_append, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('use', duse, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jnz', djnz, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jz', djz, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jno', djno, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jo', djo, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jnf', djnf, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('jf', djf, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('for', dfori, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('swp', dlocal_lang.swap, langargs=True, bracketsavailable=True)
    # Aliases & symbols
    d2local_parser.add_command('', dlocal_lang.comentary, langargs=True)
    d2local_parser.add_command('@', dlocal_lang.delay, langargs=True, bracketsavailable=True)
    d2local_parser.add_command('//', dlocal_lang.comentary, langargs=True)
    d2local_parser.add_command('?', dlocal_lang.where, args='')
    d2local_parser.add_command('!', dlocal_lang.ndata, args='')
    d2local_parser.add_command('>/', dlocal_lang.copy, langargs=True)
    d2local_parser.add_command('*', dlocal_lang.multyply, langargs=True)
    d2local_parser.add_command('/', dlocal_lang.divission, langargs=True)
    d2local_parser.add_command('<>', dlocal_lang.swap, langargs=True)
    d2local_parser.add_command('!0', dlocal_lang.erase, args='')
    d2local_parser.add_command('+', dlocal_lang.plus, langargs=True)
    d2local_parser.add_command('-', dlocal_lang.minus, langargs=True)
    d2local_parser.add_command('>', dlocal_lang.next, langargs=True)
    d2local_parser.add_command('<', dlocal_lang.prev, langargs=True)
    # System commands
    d2local_parser.add_command('@include', dlocal_lang.include, langargs=True)
    d2local_parser.add_command('@import', dlocal_lang.import_func, langargs=True)
    d2local_parser.add_command('@retape', dlocal_lang.retape, langargs=True)
    d2local_parser.add_command('@updata', dlocal_lang.data, args='update') #for update data
    d2local_parser.add_command('@relog', drelog, langargs=True)
    d2local_parser.add_command('@start', dstart, args='')
    # Tapefile
    d2local_parser.add_command('@tload', dlocal_lang.tapeload, args='') # ALPHA VERSION
    d2local_parser.add_command('@tsave', dlocal_lang.tapesave, args='') # ALPHA VERSION
    d2local_parser.add_command('@tinclude', dlocal_lang.tapeinclude, args='') # ALPHA VERSION
    d2local_parser.add_command('@treset', dlocal_lang.tapereset, args='') # ALPHA VERSION
    # Developer commands
    d2local_parser.add_command('!dev', Develop.DevfunctionPARSE, langargs=True, bracketsavailable=True) # ALPHA VERSION
    return dlocal_lang, d2local_parser

    
local_lang = VoxelLang(100001)
local_parser = VoxelParser()
local_lang, local_parser = init(local_lang, local_parser)


@handle_error()
def builder(text: str, path: str = 'build.py'):
    dlocal_lang = VoxelLang(100001)
    dlocal_parser = VoxelParser()
    
    dlocal_lang, dlocal_parser = init(dlocal_lang, dlocal_parser)

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
!dev(t);
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
bash(echo //s zxy);
delay=1000;
!0; out.str(TEST TEXT);
""")
    local_parser.printallcommands()
    """
Command 1: NONE
Command 2: nxt
Command 3: prv
Command 4: pls
Command 5: mns
Command 6: set
Command 7: ers
Command 8: out.char
Command 9: out.now
Command 10: out.str
Command 11: out.next
Command 12: out.ptype
Command 13: in.char
Command 14: in.num
Command 15: in.str
Command 16: mov
Command 17: pyl
Command 18: jmp
Command 19: mlt
Command 20: dvs
Command 21: ppl
Command 22: pmn
Command 23: pst
Command 24: pdv
Command 25: pmp
Command 26: ptp
Command 27: bash
Command 28: delay
Command 29: pylpaste
Command 30: plps
Command 31: use
Command 32: jnz
Command 33: jz
Command 34: jno
Command 35: jo
Command 36: jnf
Command 37: jf
Command 38: for
Command 39: swp
Command 40: 
Command 41: @
Command 42: //
Command 43: ?
Command 44: !
Command 45: >/
Command 46: *
Command 47: /
Command 48: <>
Command 49: !0
Command 50: +
Command 51: -
Command 52: >
Command 53: <
Command 54: @include
Command 55: @import
Command 56: @retape
Command 57: @updata
Command 58: @relog
Command 59: @start
Command 60: @tload
Command 61: @tsave
Command 62: @tinclude
Command 63: @treset
Command 64: !dev, func: <function Develop.DevfunctionPARSE at 0x110e79a20>
"""