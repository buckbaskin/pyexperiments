

def fixer(module):
    def print_mod(function):
        def inner_function(*args, **kwargs):
            print('%s%s' % (function, tuple(args)))
            return function(*args, **kwargs)
        return inner_function

    for item_name in dir(module):
        if hasattr(getattr(module, item_name), '__call__'):
            setattr(module, item_name, print_mod(getattr(module, item_name)))

    return module

if __name__ == '__main__':
    import math
    math = fixer(math)

    print(math.cos(0))
    print(math.sin(0))
    print(math.exp(2.0))