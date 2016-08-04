import ast
import inspect

# use ast.NodeVisitor and ast.NodeTransformer to walk the ast
#  and rewrite the code with Tensorflow operations

class TFReviewer(ast.NodeVisitor):
    def generic_visit(self, node):
        print('generic: %s' % type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Add(self, node):
        print('add')
        ast.NodeVisitor.generic_visit(self, node)


def flowforme(func):
    func_source = inspect.getsource(func)
    func_ast = ast.parse(func_source)
    TFReviewer().visit(func_ast)

    return func
