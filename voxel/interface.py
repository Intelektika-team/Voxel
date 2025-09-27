import os
import platform



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
    


class table:
    def __init__(self, size1, size2, data1, data2):
        self.size = [size1+2, size2+2, max(len(data1), len(data2))]
        self.data = [data1, data2]
        self.interface = {}
    
    def create(self, return_b :bool=True):
        self.interface[0] = f'╔{"═" * (self.size[0] + self.size[1] + 1)}╗'
        o = 0
        for i in range(self.size[2]):
            try: 
                text = self.data[1][o]
                length = len(text)
                oth = ' ' * (self.size[1] - length)
            except: text, oth = ' ' * (self.size[1] - 0), ''
            # теперь первый столбик
            try:
                text1 = self.data[0][o]
                length = len(text1)
                oth1 = ' ' * (self.size[0] - length)
            except: text1, oth1 = ' ' * (self.size[0] - 0), ''
            str = f"║{text1}{oth1}│{text}{oth}║"
            self.interface[i+3]=str
            o += 1
        self.interface[-1] = f'╚{"═" * (self.size[0] + self.size[1] + 1)}╝'
        if return_b:return self.interface
    
    def out(self):
        for i in self.interface:
            print(self.interface[i])

    def set(self, datanum, line, data):
        self.data[datanum][line] = data


class utils():
    def maxlen(data):
        out = []
        for i in data:
            out.append(len(str(i)))
        return max(out)
    
    def cls():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    



class interface():
    def __init__(self, 
                 lines :list=[''], 
                 data :list=[''], 
                 label :str='', 
                 descrition :str='', 
                 aftertable :str='',
                 color_table :str=color.BOLD):
        self.label = label
        self.description = descrition
        self.table = table(utils.maxlen(lines), utils.maxlen(data), lines, data)
        self.aftertable = aftertable
        if lines != [''] and data != ['']:
            self.table.create(return_b=False)
        else: self.table = ''

    def out(self):
        if self.label != '':
            print(self.label)
        if self.description != '':
            print(self.description)
        if self.table != '':
            self.table.out()
        if self.aftertable != '':
            print(self.aftertable)

    def interface_input_colored(self, input_ptompt = '-> ', *col):
        if not col:
            col = ['']
        inp = input(f"{''.join(col)}{input_ptompt}")
        print(color.RESET, end='')
        return inp

    def interface_input(self, input_ptompt = '-> ', *col):
        if not col:
            col = ['']
        inp = input(f"{''.join(col)}{input_ptompt}{color.RESET}")
        return inp
    





def test():
    utils.cls()
    label = """
██████╗░░█████╗░████████╗░█████╗░██╗░░██╗░██╗░░░░░░░██╗░█████╗░██████╗░██╗░░██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║░░██║░██║░░██╗░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╔╝███████║░░░██║░░░██║░░╚═╝███████║░╚██╗████╗██╔╝██║░░██║██████╔╝█████═╝░
██╔═══╝░██╔══██║░░░██║░░░██║░░██╗██╔══██║░░████╔═████║░██║░░██║██╔══██╗██╔═██╗░
██║░░░░░██║░░██║░░░██║░░░╚█████╔╝██║░░██║░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚██╗
╚═╝░░░░░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝
    """
    lines = [' 1', ' 2']
    data = ['Data 1', 'Data 2']
    i = interface(lines=lines, data=data, label=color.bold_green(label), descrition=color.set( "This is a patchwork, util for patch\n", color.BLUE, color.BOLD))
    i.out()
    while True:
        i.interface_input('->', color.RED)

