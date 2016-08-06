import ast
import inspect
import tensorflow as tf

# use ast.NodeVisitor and ast.NodeTransformer to walk the ast
#  and rewrite the code with Tensorflow operations

class TFReviewer(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__graph_elements = {}
        self.__next = 0

    def nextable(self):
        self.__next += 1
        return str(self.__next)

    def generic_visit(self, node):
        print('generic: %s' % type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, fdef):
        print('FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns)')
        print('inputs -> %s' % (ast.dump(fdef.args,)))
        ast.NodeVisitor.generic_visit(self, fdef)

    def visit_Return(self, ret):
        print('Return -> %s' % (ast.dump(ret,)))
        ast.NodeVisitor.generic_visit(self, ret)

    def visit_BinOp(self, binop):
        print('BinOp(expr left, operator op, expr right)')

        left_id = binop.left.id
        right_id = binop.right.id
        if isinstance(binop.op, ast.Add):
            print('this is where I will add %s and %s' % (left_id, right_id,))
            self.__graph_elements['add%s' % (self.nextable(),)] = self.__graph_elements[left_id] + self.__graph_elements[right_id]

        print('binop -> %s' % (ast.dump(binop)))
        print('expr left -> %s' % (ast.dump(binop.left),))
        print('operator op -> %s' % (ast.dump(binop.op),))
        print('expr right -> %s' % (ast.dump(binop.right),))
        
    def result_node(self):
        print('graph at result -> %s' % (self.__graph_elements,))
        if 'result_node' in self.__graph_elements:
            return self.__graph_elements['result_node']
        else:
            return None
    
    def inputs(self):
        print('inputs to the graph?')
        return []

def _buildTFGraph(func):
    func_source = inspect.getsource(func)
    func_ast = ast.parse(func_source)
    builder = TFReviewer()
    builder.visit(func_ast)
    return (builder.result_node(), builder.inputs(),)

def flowforme(func):
    (result_node, inputs,) = _buildTFGraph(func)
    if result_node is None:
        def noner(*args, **kwargs):
            return None
        return noner
    def intermediate(*args, **kwargs):
        with tf.Session() as sess:
            init = tf.initialize_all_variables()
            sess.run(init)
            return sess.run(result_node)
    intermediate.__name__ = func.__name__
    return intermediate

