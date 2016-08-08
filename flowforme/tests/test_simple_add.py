import sys
sys.path.append('/home/buck/Github/pyexperiments/flowforme')
import flowforme
from hypothesis import given
from hypothesis.strategies import floats, integers
from nose.tools import assert_equal

def simpleExample(a, b):
    return a + b

tfSimple = flowforme.flowforme(simpleExample)

@given(integers())
def test_simple_eqi(a, b):
    assert_equal(tfSimple(a, b), simpleExample(a, b))

@given(floats())
def test_simple_eqf(a, b):
    assert_equal(tfSimple(a, b), simpleExample(a, b))

