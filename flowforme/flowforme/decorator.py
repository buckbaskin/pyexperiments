'''
idea: add a decorator that tries the function call, and reraises the error or
rewrites the stack trace so that it only shows the visit_* methods instead of
also including the generic_visit and visit in the stack trace
'''

import ast
import inspect
import sys
import tensorflow as tf

# use ast.NodeVisitor and ast.NodeTransformer to walk the ast
#  and rewrite the code with Tensorflow operations

class TFReviewer(ast.NodeVisitor):
    '''
    Use to walk the ast, building up a TF graph that matches the ast
    '''
    class StopVisitor(StopIteration):
        '''
        Use in place of a StopIteration to stop processing the ast early
        '''
        def __init__(self, result_node, inputs, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if result_node is None or not result_node:
                sys.stdout.flush()
                raise ValueError(
                    'Invalid result_node name while processing ast: %s' %
                    (result_node,)) from self
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
        '''Keep an incrementing counter to uniquely name graph items'''
        self.__next += 1
        return str(self.__next)

    def result_node(self):
        '''Return the node for TF can use to calculate the value of the func'''
        if 'result_node' in self.__graph_elements:
            return self.__graph_elements['result_node']
        else:
            return None

    def inputs(self):
        '''Return a list of input names that need to be placeholder-replaced'''
        return list(self.__input_set)

    def graph(self):
        '''Return the dict mapping to the TF graph elements'''
        return dict(self.__graph_elements)

    # override for behavior
    def traverse(self, node):
        '''The unique call to start parsing the ast that handles StopVisitor'''
        try:
            result_node = ast.NodeVisitor.generic_visit(self, node)
            return (result_node, [])
        except TFReviewer.StopVisitor as done_processing:
            return (self.__graph_elements[done_processing.result_node],
                    done_processing.inputs,
                    dict(self.__graph_elements),)

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)


    # pylint: disable=invalid-name
    # it incorrectly identifies these overridden methods as invalid names
    def visit_args(self, func_args):
        '''"visit" the arguments node for an ast.FunctionDef'''
        arg_names = []
        for arg in func_args.args:
            self.__graph_elements[arg.arg] = tf.placeholder(self.__dtype, name=arg.arg)
            arg_names.append(arg.arg)
        return arg_names

    def visit_BinOp(self, binop):
        '''Write a BinOp into the TF graph after processing subtrees'''
        left_id = self.visit(binop.left)
        right_id = self.visit(binop.right)
        if isinstance(binop.op, ast.Add):
            my_id = 'add%s' % (self.nextable(),)
            self.__graph_elements[my_id] = tf.add(
                self.__graph_elements[left_id],
                self.__graph_elements[right_id],
                name=my_id)
            return my_id

    def visit_body(self, func_body):
        '''"visit" the body (list of statement nodes) for an ast.FunctionDef'''
        for stmt in func_body:
            if isinstance(stmt, ast.Return):
                return self.visit_Return(stmt)
            else:
                ast.NodeVisitor.generic_visit(self, stmt)
        self.__graph_elements['None'] = None
        return 'None'

    def visit_FunctionDef(self, fdef):
        '''Visit the one FunctionDef in an ast for a decorator'''
        inputs = self.visit_args(fdef.args)
        result_node = self.visit_body(fdef.body)
        raise TFReviewer.StopVisitor(result_node=result_node, inputs=inputs)

    def visit_Name(self, name):
        '''
        Visit a (variable) Name in the ast
        This may create a variable or read from a variable
        TODO(buckbaskin): known issue: this doesn't do var assignment yet '''
        self.__input_set.add(name.id)
        if name.id not in self.__graph_elements:
            self.__graph_elements[name.id] = tf.placeholder(self.__dtype, name=name.id)
        return name.id

    def visit_Return(self, ret):
        '''
        Visit a return variable to identify the return value
        This identifies the node that will be evaluated in the TF graph to
        get the value for the rewritten function to return
        '''
        return self.visit(ret.value)
    # it incorrectly identifies these overridden methods as invalid names
    # pylint: enable=invalid-name

def _build_tf_graph(func, default_dtype=tf.float32):
    func_source = inspect.getsource(func)
    func_ast = ast.parse(func_source)
    builder = TFReviewer(default_dtype)
    result_node, inputs, graph = builder.traverse(func_ast)
    return (result_node, inputs, graph,)

def flowforme(default_dtype=tf.float32):
    '''
    Decorator to rewrite the function implementation as a TF graph
    Args:
    - default_dtype: A tf.DType used to initialize all placeholders
    Returns:
    - a function/callable. This may be rewritten to use @couchpotato.lazy so
        the value is only calculated if it is used.
    '''
    def flowforme_wrapper(func):
        '''
        Actual decorator that takes in the function and returns the function
        that uses TF to do the code evaluation
        '''
        (result_node, inputs, graph,) = _build_tf_graph(func, default_dtype)
        def intermediate(*args, **kwargs):
            '''This is programmatically overwritten. Rewritten with TF'''
            inputs_index = 0
            feed_dict = {}
            for arg in args:
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
        intermediate.__doc__ = func.__doc__
        return intermediate
    return flowforme_wrapper
