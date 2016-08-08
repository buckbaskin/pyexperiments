import ast
import inspect
import sys
import tensorflow as tf
'''
idea: add a decorator that tries the function call, and reraises the error or 
rewrites the stack trace so that it only shows the visit_* methods instead of also including the generic_visit and visit in the stack trace
'''


# use ast.NodeVisitor and ast.NodeTransformer to walk the ast
#  and rewrite the code with Tensorflow operations

class TFReviewer(ast.NodeVisitor):
    class StopVisitor(StopIteration):
        def __init__(self, result_node, inputs, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if result_node is None or not result_node:
                sys.stdout.flush()
                raise ValueError('Invalid result_node name while processing ast: %s' % (result_node,)) from self
            self.result_node = result_node
            self.inputs = inputs
    
    # special functions
    def __init__(self, default_dtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dtype = default_dtype
        self.__graph_elements = {}
        self.__input_set = set()
        self.__next = 0

    # helper functions
    def nextable(self):
        self.__next += 1
        return str(self.__next)

    def result_node(self):
        # print('graph at result -> %s' % (self.__graph_elements,))
        if 'result_node' in self.__graph_elements:
            return self.__graph_elements['result_node']
        else:
            return None
    
    def inputs(self):
        '''Return a list of input names that need to be placeholder-replaced'''
        # print('inputs to the graph? %s' % (self.__input_set,))
        return list(self.__input_set)

    def graph(self):
        return dict(self.__graph_elements)

    # override for behavior
    def traverse(self, node):
        try:
            result_node = ast.NodeVisitor.generic_visit(self, node)
            # This will only happen if the TFReviewer did not exit early
            # print('less happy path: %s' % (result_node,))
            return (result_node, [])
        except TFReviewer.StopVisitor as done_processing:
            # This is a happy path where the TFReviwer exited early
            # print('more happy path: %s %s' % (done_processing.result_node, done_processing.inputs,))
            return (self.__graph_elements[done_processing.result_node], done_processing.inputs, dict(self.__graph_elements))

    def generic_visit(self, node):
        # print('generic: %s' % (type(node).__name__,))
        # print('with info: %s' % (ast.dump(node),))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_args(self, func_args):
        # TODO(buckbaskin): implement this (see visit_FunctionDef)
        # print('visit_args -> %s' % (func_args,))
        # print(ast.dump(func_args))
        arg_names = []
        for arg in func_args.args:
            # print('visiting arg %s and adding a placeholder' % (arg.arg,))
            self.__graph_elements[arg.arg] = tf.placeholder(self.__dtype, name=arg.arg)
            arg_names.append(arg.arg)
        return arg_names

    def visit_BinOp(self, binop):
        # print('BinOp(expr left, operator op, expr right)')

        # print('binop -> %s' % (ast.dump(binop),))
        # print('expr left -> %s' % (ast.dump(binop.left),))
        left_id = self.visit(binop.left)
        # print('expr right -> %s' % (ast.dump(binop.right),))
        right_id = self.visit(binop.right)
        # print('operator op -> %s' % (ast.dump(binop.op),))
        if isinstance(binop.op, ast.Add):
            # print('this is where I will add %s and %s' % (left_id, right_id,))
            my_id = 'add%s' % (self.nextable(),)
            self.__graph_elements[my_id] = tf.add(self.__graph_elements[left_id], self.__graph_elements[right_id], name=my_id)
            return my_id

    def visit_body(self, func_body):
        for stmt in func_body:
            if isinstance(stmt, ast.Return):
                return self.visit_Return(stmt)
            else:
                ast.NodeVisitor.generic_visit(self, stmt)
        self.__graph_elements['None'] = None
        return 'None'

    def visit_FunctionDef(self, fdef):
        # print('FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns)')
        inputs = self.visit_args(fdef.args)
        result_node = self.visit_body(fdef.body)
        raise TFReviewer.StopVisitor(result_node=result_node, inputs=inputs)

    def visit_Name(self, name):
        # print('Name -> %s' % (ast.dump(name),))
        self.__input_set.add(name.id)
        if name.id not in self.__graph_elements:
            self.__graph_elements[name.id] = tf.placeholder(self.__dtype, name=name.id)
        return name.id

    def visit_Return(self, ret):
        # print('Return -> %s' % (ast.dump(ret),))
        return self.visit(ret.value)

def _buildTFGraph(func, default_dtype=tf.float32):
    func_source = inspect.getsource(func)
    func_ast = ast.parse(func_source)
    builder = TFReviewer(default_dtype)
    result_node, inputs, graph = builder.traverse(func_ast)
    # print('BuildGraph -> result %s and graph %s' % (result_node, graph,))
    return (result_node, inputs, graph,)

def flowforme(default_dtype=tf.float32):
    def flowforme_wrapper(func):
        (result_node, inputs, graph,) = _buildTFGraph(func, default_dtype)
        if result_node is None:
            def noner(*args, **kwargs):
                return None
            return noner
        def intermediate(*args, **kwargs):
            # print('intermediate args %s and kwargs %s' % (args, kwargs,))
            inputs_index = 0
            args_index = 0
            feed_dict = {}
            for arg in args:
                # print('the arg is real. The arg is %s' % (arg,))
                if default_dtype == tf.float32:
                    feed_dict[graph[inputs[inputs_index]]] = float(arg)
                else:
                    feed_dict[graph[inputs[inputs_index]]] = arg
                inputs_index += 1
            feed_dict.update(kwargs)
            with tf.Session() as sess:
                init = tf.initialize_all_variables()
                sess.run(init)
                return sess.run(result_node, feed_dict=feed_dict)
        intermediate.__name__ = func.__name__
        return intermediate
    return flowforme_wrapper

