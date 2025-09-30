
class Void:
    _instance = None

    @property
    def set(self):
        return "VOID"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._VOID = object()  # Внутренний уникальный объект (не строка!)

    # Поглощение всех операций
    def __add__(self, other): return self
    __radd__ = __add__
    def __sub__(self, other): return self
    __rsub__ = __sub__
    def __mul__(self, other): return self
    __rmul__ = __mul__
    def __truediv__(self, other): return self
    __rtruediv__ = __truediv__
    def __floordiv__(self, other): return self
    __rfloordiv__ = __floordiv__
    def __mod__(self, other): return self
    __rmod__ = __mod__
    def __pow__(self, other): return self
    __rpow__ = __pow__
    def __and__(self, other): return self
    __rand__ = __and__
    def __or__(self, other): return self
    __ror__ = __or__
    def __xor__(self, other): return self
    __rxor__ = __xor__
    def __lshift__(self, other): return self
    __rlshift__ = __lshift__
    def __rshift__(self, other): return self
    __rrshift__ = __rshift__

    # Невозможность преобразования
    def __str__(self): 
        return "VOID" # Чтобы было возможно сделать вывод
    def __repr__(self): 
        raise TypeError("void cannot be represented")
    def __int__(self): 
        raise TypeError("void cannot be converted to int")
    def __float__(self): 
        raise TypeError("void cannot be converted to float")
    def __bool__(self): 
        return False  # Всегда False в логическом контексте

    # Уникальное поведение
    def __eq__(self, other): 
        return False  # Ничто не равно ничему
    def __hash__(self): 
        return 0  # Все void имеют одинаковый хэш (но не равны!)
    def __len__(self): 
        return 0  # Длина всегда 0
    def __iter__(self): 
        return iter(())  # Пустой итератор
    def __next__(self): 
        raise StopIteration
    def __getitem__(self, key): 
        return self  # Доступ по ключу → void
    def __setitem__(self, key, value): 
        pass  # Игнорируем установку
    def __delitem__(self, key): 
        pass  # Игнорируем удаление
    def __contains__(self, item): 
        return False  # void не содержит ничего
    def __call__(self, *args, **kwargs): 
        return self  # Вызов как функции → void
    def __getattr__(self, name): 
        return self  # Любой атрибут → void
    def __setattr__(self, name, value): 
        if name == '_instance' or name == '_VOID': 
            super().__setattr__(name, value)
        # Игнорируем остальные установки
    def __delattr__(self, name): 
        pass  # Игнорируем удаление атрибутов

    # Для контекстных менеджеров
    def __enter__(self): 
        return self
    def __exit__(self, *args): 
        pass

    # Дополнительные "поглотители"
    def __invert__(self): 
        return self  # ~void → void
    def __neg__(self): 
        return self  # -void → void
    def __pos__(self): 
        return self  # +void → void
    def __abs__(self): 
        return self  # abs(void) → void