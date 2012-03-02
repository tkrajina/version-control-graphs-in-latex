#!/usr/bin/python
# -*- coding: utf-8 -*-

ROW_COLUMN_SIZE = 400
NODE_RADIUS = 100

def row_column_to_coordinates( row, column ):
	return ( column * ROW_COLUMN_SIZE, row * ROW_COLUMN_SIZE )

def get_latex_point( node, height ):
	x, y = row_column_to_coordinates( node.row, node.column )

	color = ( 0, 0, 0 )

	result = '\\put(' + str( x - 50 ) + ',' + str( y + 100 ) + '){\\makebox(0,0)[lb]{\\smash{{\\SetFigFont{12}{14.4}{\\rmdefault}{\\mddefault}{\\updefault}{\\textit{' + node.label + '}}}}}}%\n'
	result += '{\\color[rgb]{' + str( color[ 0 ] ) + ',' + str( color[ 1 ] ) + ',' + str( color[ 2 ] ) + '}\\put(' + str( x ) + ',' + str( y ) + '){\\circle*{' + str( NODE_RADIUS ) + '}}}%\n'

	return result

def get_latex_arrow( node1, node2, height ):

	color = ( 0, 0, 0 )

	x1, y1 = row_column_to_coordinates( node1.row, node1.column )
	#x2, y2 = row_column_to_coordinates( node2.row, node2.column )

	vector_x = node2.column - node1.column
	vector_y = node2.row - node1.row

	if vector_x == 0:
		length = ROW_COLUMN_SIZE * abs( vector_y )
	else:
		length = ROW_COLUMN_SIZE * abs( vector_x )

	length = length * .9
	return '\\thicklines{\\color[rgb]{' + str( color[ 0 ] ) + ',' + str( color[ 1 ] ) + ',' + str( color[ 2 ] ) + '}\\put(' + str( x1 ) + ',' + str( y1 ) + '){\\vector(' + str( vector_x ) + ',' + str( vector_y ) + '){' + str( length ) + '}}}%\n'

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

	def get_latex_string( self, height ):
		return get_latex_point( self, height )

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

	def get_latex_string( self, height ):
		result = ''

		if self.branch_from:
			nodes = [ self.branch_from ] + self.__nodes
		else:
			nodes = self.__nodes

		for index, node in enumerate( nodes ):
			result += node.get_latex_string( height )

			if index > 0:
				previous_node = nodes[ index - 1 ]

				result += get_latex_arrow( previous_node, node, height )

		return result

	def __str__( self ):
		return '[branch:{0}:{1}]'.format( self.label, self.__nodes )

class Graph:

	__branches = None

	__arrows = None

	def __init__( self ):
		self.__branches = []
		self.__arrows = []

	def add_branch( self, branch ):
		self.__branches.append( branch )
		branch.reload_points_positions()

	def add_arrow( self, node1, node2 ):
		if not isinstance( node1, Node ):
			node1 = self.find_node( node1 )

		if not isinstance( node2, Node ):
			node2 = self.find_node( node2 )

		if not node1:
			raise Error( 'No node1 for arrow' )

		if not node2:
			raise Error( 'No node2 for arrow' )

		self.__arrows.append( [ node1, node2 ] )

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

		result = '\\setlength{\\unitlength}{4144sp}%\n'
		result += '\\begingroup\\makeatletter\\ifx\\SetFigFont\\undefined%\n'
		result += '\\gdef\\SetFigFont#1#2#3#4#5{%\n'
		result += '  \\reset@font\\fontsize{#1}{#2pt}%\n'
		result += '  \\fontfamily{#3}\\fontseries{#4}\\fontshape{#5}%\n'
		result += '  \\selectfont}%\n'
		result += '\\fi\\endgroup%\n'
		result += '\\begin{picture}(' + str( width ) + ',' + str( height ) + ')(0,0)%\n'


		for branch in self.__branches:
			result += branch.get_latex_string( height )

		for node1, node2 in self.__arrows:
			result += get_latex_arrow( node1, node2, height )

		result += '\\end{picture}\n'

		return result

	def __str__( self ):
		return '[graph:{0}]'.format( self.__branches )

if __name__ == '__main__':
	graph = Graph()

	graph.add_branch( Branch(
			label = 'eksperiment',
			nodes = 'abcdefgh' ) )

	graph.add_branch( Branch(
			label = 'eksperiment',
			row = 2,
			nodes = 'xyzqw',
			branch_from = graph.find_node( 'b' ) ) )

	graph.add_branch( Branch(
			label = 'eksperiment 2',
			row = 1,
			nodes = '1234',
			branch_from = graph.find_node( 'g' ) ) )

	graph.add_arrow( 'd', 'z' )
	graph.add_arrow( 'q', 'g' )

	# TODO: node color
	# TODO: branch color
	# TODO: branch label
	# TODO: arrow color

	print """\\documentclass[11pt,oneside,a4paper]{report}

\\linespread{1.2}

\\title{test fig}

\\usepackage[dvips]{color}
\\usepackage[croatian]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage{epsfig}
\\usepackage{makeidx}

\\addtolength{\\hoffset}{-1cm}
\\addtolength{\\voffset}{-3cm}
\\addtolength{\\textwidth}{3cm}
\\addtolength{\\textheight}{4cm}
\\pagestyle{empty}

\\begin{document}"""

	print graph.get_latex_string()

	print 'OK'

	print "\\end{document}"
