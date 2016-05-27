def hello_world(a, b):
    '''
    This is still wrong, because the code 
    '''
    if a:
        if a and b:
            return 1
        elif 1 == a:
            return 0
        else:
            return -1
    else:
        return 0
    if b:
        return 2
    else:
        return -2