'''
old concept:

import tensorflow as tf

__old_int = int

class FlowedIntegerType(__old_int):
    def __add__(self, value):
        print('FlowedInteger: add %s, %s' % (self, value,))
        return __old_int.__add__(self, value)

    def __radd__(self, value):
        print('FlowedInteger: radd %s, %s' % (self, value,))
        return __old_int.__add__(self, value)

global int
int = FlowedIntegerType
'''

from flowforme.decorator import flowforme

