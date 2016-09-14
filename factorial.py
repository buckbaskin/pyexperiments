def fact(n: int, accum: int = 1) -> int:
    if n > 0:
        return fact(n-1, accum*n)
    else:
        return accum

import sys
from typing import IO
def get_sys_out(error: bool) -> IO[str]:
    if error:
        return sys.stderr
    else:
        return sys.stdout

if __name__ == '__main__':
    '''
    python3
    > 120
    mypy
    > (returns 0/no output)
    '''
    print(fact(5))

    '''
    python3
    > 'johnjohn'
    mypy
    > error: Argument 2 to "fact" has incompatible type "str"; expected "int"
    '''
    # print(fact(2, 'john'))
    print(get_sys_out(True))
    print(get_sys_out(False))
