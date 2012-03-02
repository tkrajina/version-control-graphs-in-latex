#!/usr/bin/python
# -*- coding: utf-8 -*-

ROW_COLUMN_SIZE = 500

def row_column_to_coordinates( row, column ):
	return ( row * ROW_COLUMN_SIZE, column * ROW_COLUMN_SIZE )

def get_latex_point( node, height ):
	pass

def get_latex_arrow( node1, node2, height ):
	pass

def get_latex_text( row, column, label, height ):
	pass

class Node:

	label = None

	row = None
	column = None

	def __init__( self, label ):
		self.label = label if label else ''
		self.row = 0
		self.column = 0

	def get_latex_string( self ):
		result = ''

		result += 'latex({0},{1})'.format( self.row, self.column )

		return result

	def __str__( self ):
		return '[node:{0}:{1},{2}]'.format( self.label, self.row, self.column )

class Branch:

	__nodes = None

	label = None
	nodes = None
	row = None
	branch_from = None

	def __init__( self, label = None, nodes = None, row = None, branch_from = None ):
		self.label = label if label else ''
		self.row = row if row else 0
		self.branch_from = branch_from

		self.__nodes = []

		if nodes:
			for node in nodes:
				self.add_node( node )

	def add_node( self, node ):
		""" Node may be instance of Node or string (note label) """
		if isinstance( node, Node ):
			self.__nodes.append( node )
		else:
			self.__nodes.append( Node( label = str( node ) ) )

	def find_node( self, node_label ):
		for node in self.__nodes:
			if node.label == node_label:
				return node
		return None

	def reload_points_positions( self ):
		start_column = 0

		if self.branch_from:
			start_column = self.branch_from.column + 1

		for index, node in enumerate( self.__nodes ):
			node.row = self.row
			node.column = start_column + index

	def get_latex_string( self ):
		result = ''

		if self.branch_from:
			nodes = [ self.branch_from ] + self.__nodes
		else:
			nodes = self.__nodes

		for node in nodes:
			result += node.get_latex_string()

		return result

	def __str__( self ):
		return '[branch:{0}:{1}]'.format( self.label, self.__nodes )

class Graph:

	__branches = None

	def __init__( self ):
		self.__branches = []

	def add_branch( self, branch ):
		self.__branches.append( branch )
		branch.reload_points_positions()

	def find_node( self, node_label ):
		for branch in self.__branches:
			node = branch.find_node( node_label )
			if node:
				return node

		return None

	def get_max_row( self ):
		result = 0

		for branch in self.__branches:
			if branch.row > result:
				result = branch.row

		return result

	def get_latex_string( self ):
		width = 2000
		height = self.get_max_row() * ROW_COLUMN_SIZE

		result = ''

		for branch in self.__branches:
			result += branch.get_latex_string()

		return result

	def __str__( self ):
		return '[graph:{0}]'.format( self.__branches )

if __name__ == '__main__':
	graph = Graph()

	master_branch = Branch(
			label = 'eksperiment',
			nodes = 'abcdefgh' )
	graph.add_branch( master_branch )

	branch1 = Branch(
			label = 'eksperiment',
			row = 2,
			nodes = 'xyzqw',
			branch_from = graph.find_node( 'b' ) )
	graph.add_branch( branch1 )

	branch2 = Branch(
			label = 'eksperiment 2',
			row = 1,
			nodes = 'šđčćž',
			branch_from = graph.find_node( 'g' ) )
	graph.add_branch( branch2 )

	print graph.get_latex_string()
