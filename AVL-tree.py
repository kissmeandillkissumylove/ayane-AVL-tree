"""avl-tree implementation.
09.30.2023. https://github.com/kissmeandillkissumylove"""

from __future__ import annotations
from typing import Union


class Node(object):
	"""node class for a tree. args: data (int, float, str), height (int), left (Node), right
	(Node)."""

	def __init__(
			self,
			data: Union[int, float, str],
			left: Union[Node, None] = None,
			right: Union[Node, None] = None):
		"""node __init__."""
		self.data = data
		self.left = left
		self.right = right
		self._height = 0

	def get_height(self) -> int:
		"""returns node's height. complexity: O(1)."""
		return self._height

	def update_height(self):
		"""update height after insertion. complexity: O(1)."""
		if not self.left and not self.right:
			self._height = 0
		elif self.right and not self.left:
			self._height = self.right._height + 1
		elif self.left and not self.right:
			self._height = self.left._height + 1
		else:
			self._height = max(self.left._height, self.right._height) + 1

	def check_balance(self) -> int:
		"""checking the balance. if the output is negative, then the tree is unbalanced
		to the left and vice versa. complexity: O(1)."""
		return abs(self.left._height if self.left is not None else 0 - (
			self.right._height if self.right is not None else 0)) >= 2


class AVLTree(object):
	"""AVL-tree class."""

	def __init__(self):
		"""AVLTree __init__."""
		self._root = None

	def search(self, data: Union[int, float, str]) -> Union[Node, None]:
		"""method for searching an element in the tree. returns node if node is exists or
		None if no such node in the tree. complexity: O(log n)."""
		node = self._root
		while node:
			if data == node.data:
				return node
			elif data > node.data:
				node = node.right
			else:
				node = node.left
		return

	def insert(self, data: Union[int, float, str]) -> None:
		"""method for inserting a new element into the tree. returns nothing.
		complexity: O(log n)."""
		if not self._root:  # if no root in the tree
			self._root = Node(data)
		else:  # if tree is not empty
			self._root = self._insert(data, self._root)

	def _insert(self, data: Union[int, float, str], node: Node) -> Node:
		"""helper for insert(). complexity: O(log n)."""
		if not node:  # no node
			node = Node(data)
		elif data < node.data:  # continue in left side
			node.left = self._insert(data, node.left)
			if node.check_balance():
				if data < node.left.data:  # need right rotate for node
					node = self._right_rotate(node)
				else:  # need left-right rotate for node
					node = self._left_right_rotate()
		elif data > node.data:  # continue in right side
			node.right = self._insert(data, node.right)
			if node.check_balance():
				if data < node.right.data:  # need right-left rotate for node
					node.right = self._right_left_rotate(node)
				else:
					node = self._left_rotate(node)
		node.update_height()  # last update height for node
		return node

	def _left_right_rotate(self, node: Node):
		"""swap nodes positions. complexity: O(1)."""
		node.left = self._left_rotate(node.right)
		return self._right_rotate(node)

	def _right_left_rotate(self, node: Node):
		"""swap nodes positions. complexity: O(1)."""
		node.right = self._right_rotate(node.right)
		return self._left_rotate(node)

	@staticmethod
	def _right_rotate(node: Node) -> Node:
		"""swap nodes positions. complexity: O(1)."""
		noder = node  #change positions
		node = node.left
		noder.left = node.right
		node.right = noder
		node.update_height()  # update heights
		noder.update_height()
		return node

	@staticmethod
	def _left_rotate(node: Node) -> Node:
		"""swap nodes positions. complexity: O(1)."""
		nodel = node  #change positions
		node = node.right
		nodel.right = node.left
		node.left = nodel
		node.update_height()  # update heights
		nodel.update_height()
		return node

	def out(self):
		"""output a tree in width. complexity: O(n)."""
		queue = [self._root]
		while len(queue) > 0:
			node = queue.pop(0)
			print("node={}".format(node.data))
			if node.left is not None:
				queue.append(node.left)
			if node.right is not None:
				queue.append(node.right)

	def out_graphical(self):
		"""print tree. complexity: O(n)."""
		nodes, height = [self._root], 90
		while nodes:
			for node in nodes:
				if node:
					if node == "S":
						print(" ", end=" ")
					else:
						print(" " * height, node.data, end=" " * height)
			print("\n")
			for elt in range(0, len(nodes)):
				node = nodes.pop(0)
				if node:
					if node == "S":
						nodes.append("S")
						if len(nodes) == nodes.count(nodes[0]):
							nodes = []
							break
					else:
						nodes.append(node.left)
						nodes.append(node.right)
				else:
					nodes.append("S")
					nodes.append("S")
			height //= 2


def main():
	"""main function"""
	tree = AVLTree()
	for _ in range(0, 21):
		tree.insert(_)
	tree.out()
	tree.out_graphical()


if __name__ == "__main__":
	main()
