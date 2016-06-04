def hello_world(a, b):
    '''
    This is still wrong, because the code 
    '''
    if a:
        g = 1
    else:
        g = 0
    # the code actually will never run past this point (4 branches)
    if b:
        return 2*g
    else:
        return -2*g