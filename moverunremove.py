goal = '/home/buck/Github/pyexperiments/othernotself.py'

import os
from shutil import copyfile
import subprocess

try:
    f = open(goal, 'r')
    print('running in another location %s' % (os.path.abspath(__file__)))
except:
    print('Couldn\'t open goal. Will try to move self')
    print(os.path.abspath(__file__))
    copyfile(os.path.abspath(__file__), goal)
    print('copied file')
    subprocess.Popen(['python', goal], stdin=None, stdout=None, stderr=None, close_fds=True)
    import time
    time.sleep(1)
    os.remove(os.path.abspath(__file__))
