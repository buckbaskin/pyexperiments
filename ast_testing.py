import ast
from ast import parse

from copy import deepcopy

import functools
from functools import partial

class PrintTreeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.state = {}
        self.state['top_level_funcs'] = 0
        self.state['func_count'] = 0

    def generic_visit(self, node):
        # print('generic_visit to: %s' % (type(node).__name__))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node):
        '''
        Known children:
        body (list of expressions?/statements?)
        '''
        print('override Module. begin test analysis')
        # print('body: %s' % node.body)
        self.state['module_name'] = 'a module has no name'
        for ast_obj in node.body:
            if isinstance(ast_obj, ast.FunctionDef):
                self.state['top_level_funcs'] += 1
        ast.NodeVisitor.generic_visit(self, node)

        # print('I found %d functions and %d top level functions to test' % 
        #     (self.state['func_count'], self.state['top_level_funcs'],))

    def visit_Load(self, node):
        pass

    def visit_FunctionDef(self, node):
        '''
        Known children:
        arguments
        arg
        body?
        '''
        self.state['func_count'] += 1
        # print('begin potential function test '+str(node.name))

        incoming_state = deepcopy(self.state)

        # print('incoming state %s' % self.state)

        self.state = {'inside': node.name}

        # print('"incoming" state %s' % self.state)
        ast.NodeVisitor.generic_visit(self, node)
        # print('end potential function test '+str(node.name))
        self.state = incoming_state

    def visit_If(self, node):
        print('at a branching point if')

        incoming_state = deepcopy(self.state)

        if 'inside' in self.state:
            print('if-branch in %s' % (self.state['inside']))
        else:
            self.state['inside'] = 'if'
        self.state = {'inside': self.state['inside']+'-if'}

        incoming_state2 = deepcopy(self.state)

        # print('if (%s):\n    %s' % (node.test, node.body,))
        # if len(node.orelse) > 0:
        #     print('else:\n    %s' % (node.orelse))

        self.state['possible_branches'] = 0
        body_branch_accum = 0
        for child in node.body:
            ast.NodeVisitor.visit(self, child)
            try:
                body_branch_accum += self.state['possible_branches']
            except KeyError:
                body_branch_accum += 1
        
        print('branches in body: %d' % (body_branch_accum))

        self.state = incoming_state2
        self.state['possible_branches'] = 0

        else_branch_accum = 0
        for child in node.orelse:
            ast.NodeVisitor.visit(self, child)
            try:
                else_branch_accum += self.state['possible_branches']
            except KeyError:
                else_branch_accum += 1
        
        print('branches in else: %d' % (else_branch_accum))

        self.state = incoming_state
        self.state['possible_branches'] = body_branch_accum + else_branch_accum
        if 'inside' in self.state:
            print('end if in %s, %d branches' % (self.state['inside'], self.state['possible_branches'],))
        else:
            print('end a branching point if, %d branches at this point.' % self.state['possible_branches'])

    def visit_Return(self, node):
        print('at return "leaf"')
        self.state['possible_branches'] = 1
        ast.NodeVisitor.generic_visit(self, node)

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