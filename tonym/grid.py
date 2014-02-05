#!/usr/bin/env python
# -*- coding: ascii -*-

"""
grid.py
Read grid from file and print out path in serpentine pattern
Usage:
	from tonym import btree
	io = GridIO()
	grid = io.build(file('grid.txt'))
	l = grid.clockwise()
	pprint(l)


OVERVIEW: 
		My thoughts here were to treat this as a pathfinding problem The "map"
	would be stored in a dict of coordinate tuples, i.e. (x,y) -> data. Deleting
	nodes from a dict is easier to manage than nested lists The nodes could be
	traversed w,s,e,n (clockwise) which is conceptually easier than an odd nested
	loop. Nodes will be removed from the map when visited

"""
import sys
import logging
from pprint import pformat,pprint
__author__ = 'tonym@tonym.us'
__version__ = '1.0.0' 
class App:
	"""Contains app globals like tree root and main method"""
	def run(self, args):
		# TODO test args / use getopt
		io = GridIO()
		grid = io.build(file(args[1]))
		print "original view of grid:"
		pprint(grid)
		print "clockwise traversal of grid"
		pprint(grid.clockwise())
		

class GridIO:
	""" parses file into grid"""
	def build(self, f):
		"""read file f and build into tree"""
		# TODO error check on file/bounds/etc
		# read file data in order into grid (x,y)
		return Grid()

class Grid:
	"""Contains node data and refs to children. Also, ref to index """
	def __init__(self):
		# TODO: create real constructor. for now assign refs manually
		# contstants
		self.map = {}
		
		# active coord for iterator
		self.cur = ()

	def set(self, coord, data):
		""" set data on map for x,y """
		if type(coord) is not tuple:
			raise TypeError
		# TODO: check clobber
		self.map[coord] = data
		
	def get(self, coord):
		""" get data at coord (tuple)"""	
		if type(coord) is not tuple:
			raise TypeError
		try:
			return self.map[coord]
		except KeyError:
			return None
	
	def iterSouth(self, origin):
		if type(origin) is not tuple:
			raise TypeError
		""" return iterator south from tuple origin"""
		try:
			(x,y) = origin
			while 1:
				yield self.map[(x,y)] 
				# now delete the node we've visited
				del self.map[(x,y)]
				y += 1
		except KeyError:
			self.cur = (x,y)
			return

	def iterNorth(self, origin):
		if type(origin) is not tuple:
			raise TypeError
		try:
			(x,y) = origin
			while 1:
				yield self.map[(x,y)]
				del self.map[(x,y)]
				y -= 1
		except KeyError:
			self.cur = (x,y)
			return

	def iterEast(self, origin):
		if type(origin) is not tuple:
			raise TypeError
		try:
			(x,y) = origin
			while 1:
				yield self.map[(x,y)]
				del self.map[(x,y)]
				x += 1
		except KeyError:
			self.cur = (x,y)
			return

	def iterWest(self, origin):
		if type(origin) is not tuple:
			raise TypeError
		try:
			(x,y) = origin
			while 1:
				yield self.map[(x,y)] 
				del self.map[(x,y)]
				x -= 1
		except KeyError:
			self.cur = (x,y)
			return

	def clockwise(self):
		""" return iterator of clockwise traversal""" 
		# use a nested generator to iterate e,s,w,n
		# TODO: self.cur model is a sloppy dependency
		self.cur = (0,0)
		while 1:
			# base case
			if len(self.map) is 0:
				return
			yield iterEast(self.cur)
			yield iterSouth(self.cur)
			yield iterWest(self.cur)
			yield iterNorth(self.cur)

if __name__=='__main__':
	app = App()
	app.run(sys.argv)
