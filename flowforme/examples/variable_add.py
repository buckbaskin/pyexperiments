import sys
sys.path.append('/home/buck/Github/pyexperiments/flowforme')
import flowforme

@flowforme.flowforme()
def simpleExample(a, b):
    intermediate = a + b
    return intermediate

print('run function ->')
print(simpleExample(1, 2))

