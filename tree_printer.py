from __future__ import annotations
from collections import defaultdict
import itertools
from typing import Callable, Iterable, List, Tuple

class Node:
    def __init__(self, value, left: Node = None, right: Node = None):
        self._value = str(value)
        self._left = left
        self._right = right

    def get_left(self) -> Node:
        return self._left

    def get_right(self) -> Node:
        return self._right

    def get_value(self):
        return self._value

    def __repr__(self) -> str:
        return f"Node({self._value})"

class TreePrinter:
    """
        n0
       /  \\
      n1    n2
       \\   | \\
        n3  n4 n5

    >>> n3 = Node(123)
    >>> n4 = Node('56789')
    >>> n5 = Node('789')
    >>> n1 = Node(12, right=n3)
    >>> n2 = Node(1234, left=n4, right=n5)
    >>> n0 = Node('1', left=n1, right=n2)
    >>> tv = TreePrinter(n0)
    >>> tv._find_max_value_len()
    5
    >>> list(tv._get_inorder_listinfo())
    [(1, Node(12)), (2, Node(123)), (0, Node(1)), (2, Node(56789)), (1, Node(1234)), (2, Node(789))]
    >>> print(tv)
                1  
              /   \\
       -------     -------   
      |                   |  
      12                 1234
        \\               /   \\
         --           --     --   
           |         |         |  
          123      56789      789
    """
    VALUE_MAX_LEN = 80

    def __init__(self, root: Node):
        self._root = root
        self._max_value_len = max(2, self._find_max_value_len())
        self._inorder_listinfo = self._get_inorder_listinfo()


    def _get_inorder_listinfo(self) -> Iterable[Tuple[int, Node]]:
        """return the in-order list of nodes in the form (height_of_node, Node)
        """
        def wrapped(cur_node: Node, level: int) -> Iterable[Tuple[int, Node]]:
            if cur_node is None:
                return []

            left_iter = wrapped(cur_node.get_left(), level + 1)
            right_iter = wrapped(cur_node.get_right(), level + 1)

            return itertools.chain(left_iter, [(level, cur_node)], right_iter)


        return wrapped(self._root, 0)

    def _find_max_value_len(self) -> int:
        """return the max length of all the values inside the tree
        """
        def wrapped(cur_node: Node):
            return -TreePrinter.VALUE_MAX_LEN if cur_node is None else \
                max(len(cur_node.get_value()), wrapped(cur_node.get_left()), wrapped(cur_node.get_right()))

        return wrapped(self._root)

    def _get_centered_node_value(self, node: Node) -> str:
        return node.get_value().center(self._max_value_len)

    def _left_pad_node_using_offset(self, offset: int, node: Node) -> str:
        return offset * (' ' * self._max_value_len) + self._get_centered_node_value(node)

    def _format_tree_line_with_offsets(self, tree_line: List[Tuple[int, Node]], \
        format_action: Callable[[int, Node], str]) -> str:
        last_position_offset = 0
        line = ''
        for position, node in tree_line:
            line += format_action(position - last_position_offset, node)
            last_position_offset = position + 1

        return line

    def _build_tree_scheleton(self, tree_lines: List[List[Tuple[int, Node]]]) -> List[str]:
        """return the stringed version of the tree without links. Each node value is centered in a
        space given by `self._max_value_len`. The result is like a list where elements are placed 
        on different levels, that correspond to the height of each node.
        For example this tree:

                 1  
         12         123 
            1234

        corresponds to

           1
         /  \\
        12   123
         \\
         1234
        """
        num_levels = len(tree_lines)

        lines = [''] * num_levels
        for i in range(num_levels):
            lines[i] = self._format_tree_line_with_offsets(tree_lines[i], \
                lambda offset, node: self._left_pad_node_using_offset(offset, node))

        return lines

    def _get_first_line_below_tree_line(self, tree_line: List[Tuple[int, Node]]) -> str:
        """It is the first line after a tree_line, which is a line containing nodes value
        """
        return self._format_tree_line_with_offsets(tree_line, \
            lambda offset, node: offset * (' ' * self._max_value_len) + \
                ('/' if node.get_left() is not None else ' ') + \
                (' ' * (self._max_value_len - 2)) + \
                ('\\' if node.get_right() is not None else ' '))

    def _get_second_line_below_tree_line(self, tree_line_above: List[Tuple[int, Node]], \
        tree_line_below: List[Tuple[int, Node]]) -> str:
        line_blocks_length = max(tree_line_above[-1][0], tree_line_below[-1][0])
        line_blocks = [' ' * self._max_value_len] * line_blocks_length
        def fill_line_blocks(start: int, end: int, is_left_child: bool):
            """fills line_blocks with links in the range [start, end[ if left child,
            ]start, end] if right child"""
            half_max_len = self._max_value_len // 2
            if is_left_child:
                line_blocks[start:end] = [' ' * (self._max_value_len - half_max_len) + '-' * half_max_len] +\
                    ['-' * self._max_value_len] * (end - start - 1)
            else:
                line_blocks[start + 1:end + 1] = ['-' * self._max_value_len] * (end - start - 1) + \
                    ['-' * half_max_len + ' ' * (self._max_value_len - half_max_len)]

        for parent_index, node in tree_line_above:
            if node.get_left() is not None:
                left_child_index = next(filter(lambda x: x[1] == node.get_left(), tree_line_below))[0]
                fill_line_blocks(left_child_index, parent_index, True)

            if node.get_right() is not None:
                right_child_index = next(filter(lambda x: x[1] == node.get_right(), tree_line_below))[0]
                fill_line_blocks(parent_index, right_child_index, False)

        return ''.join(line_blocks)

    def _get_third_line_below_tree_line(self, tree_line_below: List[Tuple[int, Node]]) -> str:
        half_max_len = self._max_value_len // 2
        return self._format_tree_line_with_offsets(tree_line_below, \
            lambda offset, node: offset * (' ' * self._max_value_len) + \
                ' ' * half_max_len + \
                '|' + \
                ' ' * (self._max_value_len - half_max_len - 1))

    def __str__(self) -> str:
        lines_dict = defaultdict(lambda: list())
        for i, nodeinfo in enumerate(self._inorder_listinfo):
            lines_dict[nodeinfo[0]].append((i, nodeinfo[1]))

        tree_lines = [lines_dict[k] for k in sorted(lines_dict)]
        scheleton_lines = self._build_tree_scheleton(tree_lines)
        first_lines_below_tree_lines = [self._get_first_line_below_tree_line(tl) for tl in tree_lines]
        second_lines_below_tree_lines = [\
            self._get_second_line_below_tree_line(tl, tree_lines[i + 1]) \
            for i, tl in enumerate(tree_lines[:-1])] + ['']
        third_lines_below_tree_lines = [self._get_third_line_below_tree_line(tl) for tl in tree_lines[1:]] + ['']

        return "\n".join(map(lambda x: f"{x[0]}\n{x[1]}\n{x[2]}\n{x[3]}", \
            zip(scheleton_lines, first_lines_below_tree_lines, second_lines_below_tree_lines, \
                third_lines_below_tree_lines))).rstrip()


if __name__ == '__main__':
    import doctest
    doctest.testmod()