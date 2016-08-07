import sys
sys.path.append('/home/buck/Github/pyexperiments/flowforme')
import flowforme

print(dir(flowforme))

# I want this to become a tf graph with two variables a, b
#  that get added with a tf.add(a, b)
# Then, similar to couchpotato, when the value is actually used,
#  its value is evaluated (but this time with tf)
@flowforme.flowforme()
def simpleExample(a, b):
    return a + b

print('run function ->')
print(simpleExample(1, 2))

