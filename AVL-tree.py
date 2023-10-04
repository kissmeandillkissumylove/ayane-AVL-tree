"""avl-tree implementation.
09.30.2023 https://github.com/kissmeandillkissumylove"""

from __future__ import annotations
from typing import Union, NoReturn


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
		"""get current node's height. complexity: O(1)."""
		return self._height

	def is_balance(self) -> bool:
		"""check node's balance. complexity: O(1)."""
		return abs((self.left.get_height() if self.left is not None else -1) - (
			self.right.get_height() if self.right is not None else -1)) >= 2

	def update_height(self) -> None:
		"""update node's height after inserting. complexity: O(1)."""
		self._height = max((self.left.get_height() if self.left is not None else -1), (
			self.right.get_height() if self.right is not None else -1)) + 1


class AVLTree(object):
	"""AVL-tree class."""

	def __init__(self):
		"""AVLTree __init__."""
		self._root = None

	def search(self, data: Union[int, float, str]) -> Union[Node, None]:
		"""method for searching an element in the tree. returns node if node exists or
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

	def insert(self, data: Union[int, float, str]) -> NoReturn:
		"""insert new element in the tree. complexity: O(log n)."""
		if self._root is None:
			self._root = Node(data)  # no root in the tree
		else:
			self._root = self._insert(data, self._root)  # find and insert new node

	def _insert(self, data: Union[int, float, str], node: Node) -> Node:
		"""helper for insert() method. complexity: O(log n)."""
		if node is None:  # found suitable location
			node = Node(data)
		elif data < node.data:  # if new node is lower than current node
			node.left = self._insert(data, node.left)
			if node.is_balance():  #  if no balance after inserting
				if data < node.left.data:  # check pos
					node = self._right_rotate(node)
				else:
					node = self._left_right_rotate(node)
		elif data > node.data:  # if new node is higher than current node
			node.right = self._insert(data, node.right)
			if node.is_balance():  #  if no balance after inserting
				if data < node.right.data:  # check pos
					node = self._right_left_rotate(node)
				else:
					node = self._left_rotate(node)
		node.update_height()
		return node

	def _right_left_rotate(self, node: Node) -> Node:
		"""right rotate for node then left rotate for node.right. complexity: O(1)."""
		node.right = self._right_rotate(node.right)
		return self._left_rotate(node)

	def _left_right_rotate(self, node: Node) -> Node:
		"""left rotate for node then right rotate for node.right. complexity: O(1)."""
		node.left = self._left_rotate(node.left)
		return self._right_rotate(node)

	@staticmethod
	def _left_rotate(node: Node) -> Node:
		"""left rotate for node. complexity: O(1)."""
		node_left = node
		node = node.right
		node_left.right = node.left
		node.left = node_left
		node_left.update_height()
		node.update_height()
		return node

	@staticmethod
	def _right_rotate(node: Node) -> Node:
		"""right rotate for node. complexity: O(1)."""
		node_right = node
		node = node.left
		node_right.left = node.right
		node.right = node_right
		node_right.update_height()
		node.update_height()
		return node

	def delete(self, data) -> None:
		"""delete node from the AVL-tree. complexity: O(log n)."""
		self._root = self._delete(data, self._root)

	def _delete(self, data: Union[int, float, str], node: Node) -> Union[Node, None]:
		"""recursive method to delete an element. complexity: O(log n)."""
		if node is None:  # no such node in the tree
			print("can't find {}".format(data))
			return node

		elif data < node.data:  # continue searching in left side
			node.left = self._delete(data, node.left)
			if node.is_balance():
				if node.right.left.get_height() > node.right.right.get_height():
					node = self._right_left_rotate(node)
				else:
					node = self._left_rotate(node)
			node.update_height()

		elif data > node.data:  # continue searching in right side
			node.right = self._delete(data, node.right)
			if node.is_balance():
				if node.left.right.get_height() > node.left.left.get_height():
					node = self._left_right_rotate(node)
				else:
					node = self._right_rotate(node)
			node.update_height()

		elif node.data == data:  # found the element for deletion
			if node.left and node.right:
				if node.left.get_height() >= node.right.get_height():
					# balance is off to the left
					max_node = node.left
					# find the successor for the element
					while max_node.right is not None:
						max_node = max_node.right
					node.data = max_node.data
					node.left = self._delete(node.data, node.left)
				else:
					# balance is off to the right
					min_node = node.right
					# find the successor for the element
					while min_node.left is not None:
						min_node = min_node.left
					node.data = min_node.data
					node.right = self._delete(node.data, node.right)
				node.update_height()
			else:
				if node.left:  # node has only left child
					node = node.left  # just replace it
				elif node.right:  # node has only right child
					node = node.right  # just replace it
				else:  # node has no child
					node = None  # set None
		return node

	def out(self) -> None:
		"""output a tree in width. complexity: O(n)."""
		print("{", end=" ")
		queue = [self._root]
		while len(queue) > 0:
			node = queue.pop(0)
			print(node.data, end=" ")
			if node.left is not None:
				queue.append(node.left)
			if node.right is not None:
				queue.append(node.right)
		print("}\n")

	def out_graphical(self) -> None:
		"""print tree. complexity: O(n^2)."""
		nodes, height = [self._root], 90
		while nodes:
			for node in nodes:
				if node:
					if node == "S":
						print(" ", end=" ")
					else:
						print(" " * height, node.data, end=" " * height)
				else:
					print(" " * height, " ", end=" " * height)
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
	tree.delete(15)
	tree.out()
	tree.out_graphical()
	tree.delete(99)


if __name__ == "__main__":
	main()
