import ast
from ast import parse

import functools
from functools import partial

def inject_state_into_object(object, new_state):
    print('inject state')
    for element in dir(object):
        if element[0]==('_'):
            continue
        if element == 'visit':
            continue
        if hasattr(getattr(object, element), '__call__'):
            intermediate = partial(getattr(object, element), state=new_state)
            setattr(object, element, intermediate)

class PrintTreeVisitor(ast.NodeVisitor):
    def generic_visit(self, node, state=None):
        print('generic_visit to: %s' % (type(node).__name__))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node, state=None):
        '''
        Known children:
        body (list of expressions?/statements?)
        '''
        print('override Module. begin test analysis')
        print('body: %s' % node.body)
        if state is None:
            state = {}
        state['module_name'] = 'a module has no name'
        inject_state_into_object(self, state)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node, state=None):
        pass

    def visit_FunctionDef(self, node, state=None):
        '''
        Known children:
        arguments
        arg
        body?
        '''
        print('begin potential function test '+str(node.name))
        print('incoming state %s' % state)
        ast.NodeVisitor.generic_visit(self, node)
        print('end potential function test '+str(node.name))

    # def visit_If(self, node):
    #     print('at a branching point if')
    #     ast.NodeVisitor.generic_visit(self, node)
    #     print('end a branching point if')

    # def visit_Return(self, node):
    #     print('at function return')
    #     ast.NodeVisitor.generic_visit(self, node)
    #     print('end a function return')

    # def visit_BinOp(self, node):
    #     print(type(node))
    #     print(dir(node))
    #     print(node.left)
    #     ast.NodeVisitor.generic_visit(self, node)

visitor = PrintTreeVisitor()

fileContents = open('ast_test_file.py').read()
tree = parse(fileContents, '<string>', 'exec')

print(tree)

visitor.visit(tree)