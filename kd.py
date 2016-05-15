'''
Implement a general kdtree
'''

def generate_tree(data_class):
    '''
    generates a tree 
    '''
    class KDTree(data_class):
        def __init__(self, *args, **kwargs):
            super(self, KDNode).__init__(*args, **kwargs)
            self.__kd_left = None
            self.__kd_right = None
            self.__kd_parent = None
            self.__kd_depth = None

        def __kd_set_parent(self, parent):
            self.__kd_parent = parent
            self.__kd_depth = parent.__kd_depth + 1

        def __kd_set_left(self, left):
            self.__kd_left = left

        def __kd_set_right(self, right):
            self.__kd_right = right

        def __kd_find_down(self, node):
            '''
            Iteratively searches the tree
            '''
            level_node = self

            while True:
                if (new_node.at_depth(level_node.__kd_depth) < 
                    level_node.at_depth(level_node.__kd_depth)):
                    # left
                    side = 'left'
                else:
                    side = 'right'

                if getattr(level_node, '__kd_'+side) is None:
                    return level_node
                else:
                    if level_node is getattr(level_node, '__kd_'+side):
                        # if the node has itself as a child, remove the cycle
                        setattr(level_node, '__kd_'+side, None)
                        return level_node
                    else:
                        level_node = getattr(level_node, '__kd_'+side)

        def __kd_add_node(self, new_node):
            '''
            Iteratively adds down the tree until it finds the place to put it
            '''
            level_node = self
            while(True):
                if (new_node.at_depth(level_node.__kd_depth) < level_node.at_depth(level_node.__kd_depth)):
                    # left
                    side = 'left'
                else:
                    side = 'right'

                if getattr(level_node, '__kd_'+side) is None:
                    new_node.__kd_set_parent(level_node)
                    setattr(level_node, '__kd_set_'+side, new_node)
                    return True
                else:
                    if level_node is getattr(level_node, '__kd_'+side):
                        # if the node has itself as a child, remove the cycle
                        setattr(level_node, '__kd_'+side, None)
                        return False
                    else:
                        level_node = getattr(level_node, '__kd_'+side)

            return False
