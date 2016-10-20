def jane(a, b):
    return a + b

# print('dir(jane)')
# print(dir(jane))
# print('dir(jane.__code__)')
# print(dir(jane.__code__))
# print('jane.__code__.__doc__')
# print(jane.__code__.__doc__)

# print(jane.__class__)
# print(jane.__code__.__class__)

print(type(jane).__doc__)

from types import CodeType, FunctionType

''' code(argcount, kwonlyargcount, nlocals, stacksize, flags, codestring,
      constants, names, varnames, filename, name, firstlineno,
            lnotab[, freevars[, cellvars]])
'''
co = jane.__code__
for item in dir(jane.__code__):
    print('%s -> %s' % (item, getattr(jane.__code__, item)))

codestring = co.co_code
constants = co.co_consts
print('stack size of jane: %d' % (int(co.co_stacksize),))
code_ = CodeType(
    co.co_argcount+1,
    co.co_kwonlyargcount,
    co.co_nlocals,
    co.co_stacksize,
    co.co_flags,
    codestring,
    constants,
    co.co_names,
    co.co_varnames,
    'this_moved.java',
    'function function',
    co.co_firstlineno,
    co.co_lnotab,
    co.co_freevars,
    co.co_cellvars)

# function(code, globals[, name[, argdefs[, closure]]])
# print('jane.__globals__')
# print(jane.__globals__)
print('annotations')
print(jane.__annotations__)
print('closure')
print(jane.__closure__)
print('defaults')
print(jane.__defaults__)
print('kwdefaults')
print(jane.__kwdefaults__)

for item in dir(jane):
    break
    print(item)

improved = FunctionType(code = code_, globals = jane.__globals__, name = 'johnny3tears')
print('improved')
print(improved)
print(improved.__name__)

from typing import Dict, Tuple

def def_explained(name, args, kwargs, function_body, globals_:Dict, closure:Tuple=None):
    argcount = len(args)
    kwonlyargcount = len(kwargs) # this might be wrong
    nlocals = argcount + kwonlyargcount # this is probably wrong
    # this is most definitely wrong, but I don't know how to calculate it yet
    stacksize = 9001
    # this is almost certainly wrong, but I don't know how to calculate it yet
    flags = 0
    codestring = function_body
    constants = (None,) # from example, maybe not correct
    names = () # from example, maybe not correct
    varnames = args
    filename = 'get_this_filename.py'
    # name = name
    this_line = 10 # wrong in most cases
    firstlineno = int(this_line)
    lnotab = b'\x00\x01' # from example, probably not correct
    code = CodeType(argcount, kwonlyargcount, nlocals, stacksize, flags,
                    codestring, constants, names, varnames, filename, name,
                    firstlineno, lnotab, freevars, cellvars)
    argdefs = None
    return FunctionType(code, globals_, name, argdefs, closure)

