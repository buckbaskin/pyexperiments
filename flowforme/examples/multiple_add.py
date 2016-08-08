import sys
sys.path.append('/home/buck/Github/pyexperiments/flowforme')
import flowforme

@flowforme.flowforme()
def simpleExample(a, b, c):
    return a + b + c

print('run function ->')
print(simpleExample(1, 2, 3))

