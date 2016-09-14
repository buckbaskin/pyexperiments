def fact(n: int, accum: int = 1) -> int:
    if n > 0:
        return fact(n-1, accum*n)
    else:
        return accum

# print('Hi, my name is (what?)\nMy name is (who?)\nMy name is %s' % (__name__,))
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
    print(fact(2, 'john'))
