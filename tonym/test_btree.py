from cStringIO import StringIO

import btree
from pprint import pprint
import unittest


RELATED_TREES = """1,5,4,,3,2,5,,,,,,,0,8
4,2,5
"""

UNRELATED_TREES = """1,5,4,,3,2,9,,,,,,,0,8
4,2,5
"""

class BtreeTest(unittest.TestCase):

	def setUp(self):
		self.RELATED_TREES = """1,5,4,,3,2,5,,,,,,,0,8
		4,2,5
		"""

		self.UNRELATED_TREES = """1,5,4,,3,2,9,,,,,,,0,8
		4,2,5
		"""
		self.io = btree.TreeIO()


	def create_file_object(self,data):
		file_ = StringIO()
		file_.write(data)
		file_.reset()
		return file_


	def testTop(self):
		tree_a, tree_b = self.io.parse(self.create_file_object(self.RELATED_TREES))
		self.assertEquals(tree_a.data, '1')
		self.assertEquals(tree_a.l.data, '5')
		self.assertEquals(tree_a.r.data, '4')
		self.assertEquals(tree_a.l.l.data, '')
		self.assertEquals(tree_a.l.r.data, '3')


	def testComplete(self):
		i = btree.Index()
		n = btree.Node(5, i)
		n.append(3)
		n.append(6)
		self.assertTrue(n.complete())
		n = btree.Node(5,i)
		self.assertFalse(n.complete())


	def test_related_trees(self):
		io = self.io
		tree_a, tree_b = io.parse(self.create_file_object(self.RELATED_TREES))
		self.assertTrue(tree_a.contains(tree_b))


	def test_unrelated_trees(self):
		io = self.io
		tree_a, tree_b = io.parse(self.create_file_object(self.UNRELATED_TREES))
		self.assertFalse(tree_a.contains(tree_b))


if __name__ == '__main__':
	unittest.main()
