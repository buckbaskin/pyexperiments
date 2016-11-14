goal = '/home/buck/Github/pyexperiments/othernotself.py'

import os
from shutil import copyfile

try:
    f = open(goal, 'r')
    print('running in another location %s' % (os.path.abspath(__file__)))
except:
    print('Couldn\'t open goal. Will try to move self')
    print(os.path.abspath(__file__))
    copyfile(os.path.abspath(__file__), goal)
    os.system('python %s' % goal)
    os.remove(goal)
    import sys
    sys.exit(0)

