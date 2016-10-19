def jane(a, b):
    return a + b

print('dir(jane)')
print(dir(jane))
print('dir(jane.__code__)')
print(dir(jane.__code__))
print('jane.__code__.__doc__')
print(jane.__code__.__doc__)

print(jane.__class__)
print(jane.__code__.__class__)

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
    co.co_filename,
    'function function',
    co.co_firstlineno,
    co.co_lnotab,
    co.co_freevars,
    co.co_cellvars)

# function(code, globals[, name[, argdefs[, closure]]])
improved = FunctionType(code = code_, globals = jane.__globals__, name = 'johnny3tears')
print('improved')
print(improved)
