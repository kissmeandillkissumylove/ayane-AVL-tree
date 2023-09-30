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

	def _update_height(self) -> None:
		"""update height after insertion. complexity: O(1)."""
		if not self.left and not self.right:
			self._height = 0
		elif self.right and not self.left:
			self._height = self.right._height + 1
		elif self.left and not self.right:
			self._height = self.left._height + 1
		else:
			self._height = max(self.left._height, self.right._height) + 1

	def _check_balance(self) -> int:
		"""checking the balance. if the output is negative, then the tree is unbalanced
		to the left and vice versa. complexity: O(1)."""
		if not self.left and not self.right:
			return 0
		elif self.right and not self.left:
			return self.right._height
		elif self.left and not self.right:
			return -self.left._height
		else:
			return self.right._height - self.left._height


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
			pass

	@staticmethod
	def _left_rotate(parent: Node, node: Node) -> None:
		"""left rotation relative to node. complexity: O(1)."""
		tmp_x, tmp_y = node, node.right
		if tmp_x.data < parent.data:
			parent.left = tmp_y
			AVLTree._swap_left(tmp_x, tmp_y)
		elif tmp_x.data > parent.data:
			parent.right = tmp_y
			AVLTree._swap_left(tmp_x, tmp_y)

	@staticmethod
	def _right_rotate(parent: Node, node: Node) -> None:
		"""right rotation relative to node. complexity: O(1)."""
		tmp_x, tmp_y = node, node.left
		if tmp_x.data < parent.data:
			parent.left = tmp_y
			AVLTree._swap_right(tmp_x, tmp_y)
		elif tmp_x.data > parent.data:
			parent.right = tmp_y
			AVLTree._swap_right(tmp_x, tmp_y)

	@staticmethod
	def _swap_left(tmp_x: Node, tmp_y: Node) -> None:
		"""helper for _left_rotation. complexity: O(1)."""
		tmp_x.right = tmp_y.left
		tmp_y.left = tmp_x

	@staticmethod
	def _swap_right(tmp_x: Node, tmp_y: Node) -> None:
		"""helper for _right_rotation. complexity: O(1)."""
		tmp_x.left = tmp_y.right
		tmp_y.right = tmp_x
