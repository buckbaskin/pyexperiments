'''
Implement a general kdtree
'''

def generate_tree_class(data_class):
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

        def __kd_find_down(self, near_to):
            '''
            Iteratively searches the tree
            '''
            level_node = self

            while True:
                if (near_to.at_depth(level_node.__kd_depth) < 
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

        def __kd_find_up(self, near_to, best):
            '''
            Once I've found the bottom, go back up the kd-tree and try to find
            a better node
            '''
            # best = current best node, leaf of the tree when this is called
            level_node = best.__kd_parent
            best_distance = near_to.distance(best)

            while (level_node is not None) and (level_node.__kd_depth >= 0):
                # check if the level node axis is closer than the best distance
                depth = level_node.__kd_depth
                min_potential_dist = near_to.at_depth(depth) - level_node.at_depth(depth)
                if abs(min_potential_dist) < best_distance:
                    # it could be closer
                    if min_potential_dist < 0.0:
                        side = 'left'
                    else:
                        side = 'right'

                    # is the level_node a better option?
                    if near_to.distance(level_node) < best_distance:
                        # if the level_node is closer, update best, best_distance
                        best = level_node
                        best_distance = near_to.distance(level_node)

                    # try to find a closer option
                    other_side_best = getattr(self, '__kd_'+side).kd_find_node(near_to)
                    if near_to.distance(other_side_best) < best_distance:
                        # if the option is closer, update best, best_distance
                        best = other_side_best
                        best_distance = near_to.distance(other_side_best)
                
                # move up
                level_node = level_node.__kd_parent

            return best

        def kd_find_node(self, near_to):
            leaf_estimate = self.__kd_find_down(near_to)
            return self.__kd_find_up(near_to, leaf_estimate)

        def kd_add_node(self, new_node):
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

    return KDTree
