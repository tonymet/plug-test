#!/usr/bin/env python
# -*- coding: ascii -*-
"""
btree.py.  
Represent btree in python with subtree test. 

Usage: 
	from tonym import btree
	io = TreeIO()
	tree = io.build(file('tree.txt'))
	subtree = io.build(file('subtree.txt'))
	tree.contains(subtree)

OVERVIEW:
	
	Create n-ary tree in python.  tree stored using Node class with children in python list
	nodes contain a reference to a hashtable (dict) index of the node positions. This allows
	for O(1)-time lookup of subtree root nodes

TODO:
	* doctest on methods
	* consider lib for tree representation
	* 
""" 
import sys
__author__ = 'tonym@tonym.us'
__version__ = '1.0.0' 


class App:
	"""Contains app globals like tree root and main method"""

	def run(self, args):
		# TODO test args / use getopt
		io = TreeIO()
		(tree, subtree) = io.parse(file(args[1]))
		if(tree.contains(subtree) == tree.COMPARE_EQUAL):
			print "Yes"
		else:
			print "No"

class TreeIO:
	"""Parses csv representation of tree & subtree into two trees
		returns tuple (tree, subtree)"""
	def parse(self, f):
		"""read file f and build into tree"""
		# TODO error check on file/bounds/etc
		tree_list = ','.split(f.readline())
		subtree_list = ','.split(f.readline())
		return (self.build(tree_list), self.build(subtree_list))

	def build(self, tree_list):
		""" build tree from ordered list representation"""
		pass


class Index:
	"""hashtable index of node data -> node in tree"""
	def __init__(self):
		""" create new index with index in dict"""
		self.d = {}

	def add(self, data, node):
		"""add data->node ref"""
		# TODO error check clobber
		self.d[data] = node

	def contains(self, data):
		if self.get(data) is not None:
			return True
		return false

	def get(self,data):
		try:
			return self.d[data]
		except KeyError:
			# conceal the exception
			return None

class Node:
	"""Contains node data and refs to children. Also, ref to index """
	def __init__(self, data, index):
		# TODO: create real constructor. for now assign refs manually
		# contstants
		self.COMPARE_EQUAL = 0x01
		self.COMPARE_NOT_EQUAL = -0x01
		# consts for left/right and max index
		# TODO: make these static members (I forget)
		self.LEFT =  0x0 
		self.RIGHT =  0x1 
		self.MAX_INDEX  = 0x01
		self.MAX_SIZE   = self.MAX_INDEX + 1
		

		# index ref shared among nodes
		self.index = index
		# children list supports n-ary tree
		self.children = []
		self.data   = data

	def append(self, node):
		"""add child left, right. raise error if full"""
		if(len(self.children) == (self.MAX + 1)):
			raise InvalidArgumentError
		else:
			self.index.add(node.data, node)
			self.children.append(node)
	
	def iterNodes(self, root):
		if len(self.children) == 0:
			yield self.data
		else:
			yield iter(self.children)
		
	def contains(self, qnode):
		"""look up root node in index. Then recursive compare to children
		qnode is the root node of the query subtree
		"""
		# TODO bug if compareTo is called outside root this will compare outside tree

		# tnode is the target node in the main tree
		tnode = self.index.get(qnode.data)
		if tnode is None:
			return self.COMPARE_NOT_EQUAL

		# traverse query and target "subtrees" into lists for easy compare
		# this does cost one extra traversal of the subtree but it's more pythonic
		qnode_list = [n for n in qnode]
		tnode_list = [n for n in tnode]
		if qnode_list == tnode_list:
			return self.COMPARE_EQUAL
		return self.COMPARE_NOT_EQUAL
		
if __name__=='__main__':
	app = App()
	app.run(sys.argv)
