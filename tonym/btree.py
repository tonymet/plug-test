#!/usr/bin/env python
# -*- coding: ascii -*-
"""
btree.py.  
Represent btree in python with subtree test. 

Usage: 
	from tonym import btree
	io = TreeIO()
	(tree,subtree) = io.parse(file('tree.txt'))
	tree.contains(subtree)

OVERVIEW:
	
Create n-ary tree in python.  tree stored using Node class with children in python list
nodes are indexed in a  hashtable (dict) of the node positions. This allows
for O(1)-time lookup of subtree root nodes

TODO:
	* doctest on methods
	* consider lib for tree representation
	* 
""" 
import sys
import logging
from pprint import pprint,pformat
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
		tree_list = f.readline().strip().split(',')
		subtree_list = f.readline().strip().split(',')
		return (self.build(tree_list), self.build(subtree_list))

	def build(self, tree_list):
		""" build tree from ordered list representation"""
		index = Index()
		root = Node(None, index)
		root.append(tree_list.pop(0))
		cur = root
		while 1:
			try:
				cur = cur.append(tree_list.pop(0))
			except IndexError:
				break
		return root



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
	
	def __setitem__(self, k, v):
		self.add(k,v)

class Node:
	"""Contains node data and refs to children. Also, ref to index """
	def __init__(self, data, index):
		# TODO: create real constructor. for now assign refs manually
		# contstants
		self.COMPARE_EQUAL = 0x01
		self.COMPARE_NOT_EQUAL = -0x01
		# consts for left/right and max index
		# TODO: make these static members (I forget)
		

		# index ref shared among nodes
		self.index = index
		self.r = None
		self.l = None
		self.data   = data

	def append(self, data):
		"""add child left, right. raise error if full"""
		if self.data is None:
			self.data = data
			self.index[data] = self
			return self
		elif self.l is None:
			self.l = Node(None, self.index)
			self.l.append(data)
			return self.l
		elif self.r is None:
			self.r = Node(None, self.index)
			self.r.append(data)
			return self.r

	def __str__(self):
		l = []
		for i in self.iterNodes():
			l.append(i)
		return ' '.join(l)

	def iterNodes(self):
		yield self.data
		if self.l is not None:
			for e in self.l.iterNodes():
				yield e
		if self.r is not None:
			for e in self.l.iterNodes():
				yield e

	def fiterNodes(self,f):
		f( self.data)
		if self.l is not None:
			self.l.fiterNodes(f)
		if self.r is not None:
			self.r.fiterNodes(f)
		
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
		qnode_list = [n for n in qnode.iterNodes()]
		tnode_list = [n for n in tnode.iterNodes()]
		if qnode_list == tnode_list:
			return self.COMPARE_EQUAL
		return self.COMPARE_NOT_EQUAL
		
if __name__=='__main__':
	app = App()
	app.run(sys.argv)
