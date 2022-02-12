from printer.tree_printer import Node, TreePrinter

n1 = Node(1)
n3 = Node(3, left=n1)
n6 = Node(6)
n8 = Node(8)
n14 = Node(14)
n4 = Node(4, left=n3, right=n6)
n10 = Node(10, left=n8, right=n14)
n7 = Node(7, left=n4, right=n10)

tv = TreePrinter(n7)
print(tv)