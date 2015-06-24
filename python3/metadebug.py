'''
    A generic class debugger using metaprogramming and decorators.
    Requires Python 3

    Dictionary Example:
        In [14]: dd = DebugDict({'one': 1, 'two': 2, 'three': 3})
        DEBUG: dict.__getattribute__
        DEBUG: dict.__getattribute__
        DEBUG: dict.__new__
        DEBUG: dict.__init__
        
        In [15]: dd.keys()
        DEBUG: dict.__getattribute__
        DEBUG: dict.keys
        Out[15]: dict_keys(['two', 'one', 'three'])
        
        In [16]: dd.get('two')
        DEBUG: dict.__getattribute__
        DEBUG: dict.get
        Out[16]: 2
        
        In [17]: dd.pop('two')
        DEBUG: dict.__getattribute__
        DEBUG: dict.pop
        Out[17]: 2
        
        In [18]: 'two' in dd
        DEBUG: dict.__contains__
        Out[18]: False

'''
from functools import wraps
import inspect

def _make_wrap(obj, method):
    return '{O}.{M} = debugwrap({O}.{M})'.format(O=obj, M=method)

def debugwrap(func):
    name = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("DEBUG:", name)
        return func(*args, **kwargs)
    return wrapper

class debugmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        # Wrap each method with our debug decorator
        routines = [name for name, obj in inspect.getmembers(clsobj) if inspect.isroutine(obj)]
        # Call exec with a manually created 'locals' dict so it can find our clsobj
        for routine in routines:
            exec(_make_wrap('clsobj', routine), globals(), {'clsobj': clsobj})
        return clsobj

# Example usage:
class DebugDict(dict, metaclass=debugmeta):
    pass

class DebugSet(set, metaclass=debugmeta):
    pass

class DebugTuple(tuple, metaclass=debugmeta):
    # doesn't work
    pass
