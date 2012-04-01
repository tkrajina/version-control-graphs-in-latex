#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging as mod_logging

ROW_COLUMN_SIZE = 400
NODE_RADIUS = 100

def row_column_to_coordinates( row, column ):
	return ( column * ROW_COLUMN_SIZE, ROW_COLUMN_SIZE + row * ROW_COLUMN_SIZE )

def get_latex_point( node, height, color = None ):
	x, y = row_column_to_coordinates( node.row, node.column )

	if not color:
		color = ( 0, 0, 0 )

	result = '\\put(' + str( x - 50 ) + ',' + str( y + 100 ) + '){\\makebox(0,0)[lb]{\\smash{{\\SetFigFont{12}{14.4}{\\rmdefault}{\\mddefault}{\\updefault}{\\textit{' + node.label + '}}}}}}%\n'
	result += '{\\color[rgb]{' + str( color[ 0 ] ) + ',' + str( color[ 1 ] ) + ',' + str( color[ 2 ] ) + '}\\put(' + str( x ) + ',' + str( y ) + '){\\circle*{' + str( NODE_RADIUS ) + '}}}%\n'

	return result

def get_arrow_xy( x, y ):
	result_x = x
	result_y = y
	#if x == 2:import pdb;pdb.set_trace()
	for i in range( 2, 1 + min( abs( x ), abs( y ) ) ):
		mod_logging.debug( 'result_x:{0}, result_y:{1}, i:{2}'.format( result_x, result_y, i ) )
		if result_x % i == 0 and result_y % i == 0:
			mod_logging.debug( 'Skraćujemo s {0}'.format( i ) )
			result_x = result_x / i
			result_y = result_y / i
	return result_x, result_y

def get_latex_arrow( node1, node2, height, color = None ):

	if not color:
		color = ( 0, 0, 0 )

	x1, y1 = row_column_to_coordinates( node1.row, node1.column )
	#x2, y2 = row_column_to_coordinates( node2.row, node2.column )

	vector_x, vector_y = node2.column - node1.column, node2.row - node1.row

	if vector_x == 0:
		length = ROW_COLUMN_SIZE * abs( vector_y )
	else:
		length = ROW_COLUMN_SIZE * abs( vector_x )

	vector_x, vector_y = get_arrow_xy( vector_x, vector_y )

	length = length * .9
	return '\\thicklines{\\color[rgb]{' + str( color[ 0 ] ) + ',' + str( color[ 1 ] ) + ',' + str( color[ 2 ] ) + '}\\put(' + str( x1 ) + ',' + str( y1 ) + '){\\vector(' + str( vector_x ) + ',' + str( vector_y ) + '){' + str( length ) + '}}}%\n'

def get_latex_text( row, label ):
	y = ROW_COLUMN_SIZE + row * ROW_COLUMN_SIZE
	return '\\put(' + str( 0 ) + ',' + str( y ) + '){\\makebox(0,0)[lb]{\\smash{{\\SetFigFont{12}{14.4}{\\rmdefault}{\\mddefault}{\\updefault}{\\texttt{' + label + '}}}}}}%\n'

class Node:

	label = None

	row = None
	column = None

	color = None

	def __init__( self, label, color = None ):
		self.label = label if label else ''
		self.row = 0
		self.column = 0
		self.color = color

	def get_latex_string( self, height, color = None ):
		return get_latex_point( self, height, color = self.color if self.color else color )

	def __str__( self ):
		return '[node:{0}:{1},{2}]'.format( self.label, self.row, self.column )

class Branch:

	__nodes = None

	label = None
	nodes = None
	row = None
	branch_from = None
	color = None

	def __init__( self, label = None, nodes = None, row = None, branch_from = None, color = None ):
		self.label = label if label else ''
		self.row = row if row else 0
		self.branch_from = branch_from
		self.color = color if color else ( 0, 0, 0 )

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

	def reload_points_positions( self, column ):
		start_column = column

		if self.branch_from:
			start_column = self.branch_from.column + 1

		for index, node in enumerate( self.__nodes ):
			node.row = self.row
			node.column = start_column + index

	def get_latex_string( self, height, color = None ):
		result = ''

		if not color:
			color = self.color

		if self.branch_from:
			nodes = [ self.branch_from ] + self.__nodes
		else:
			nodes = self.__nodes

		for index, node in enumerate( nodes ):
			if node != self.branch_from and node.label != '-':
				result += node.get_latex_string( height, color = color )

			if index > 0:
				if nodes[ index - 1 ].label != '-':
					previous_node = nodes[ index - 1 ]
				if node.label != '-':
					result += get_latex_arrow( previous_node, node, height, color = self.color )

		return result

	def __str__( self ):
		return '[branch:{0}:{1}]'.format( self.label, self.__nodes )

class Graph:

	__branches = None

	__arrows = None

	column = None

	def __init__( self, column = None ):
		self.__branches = []
		self.__arrows = []
		self.column = column if column else 0

	def add_branch( self, branch ):
		"""
		if len( self.__branches ) == 0 and not branch.label:
			branch.label = 'master'
			"""

		self.__branches.append( branch )
		branch.reload_points_positions( self.column )

	def add_arrow( self, node1, node2, color = None ):

		if not color:
			color = ( 0, 0, 0 )

		if not isinstance( node1, Node ):
			node1 = self.find_node( node1 )

		if not isinstance( node2, Node ):
			node2 = self.find_node( node2 )

		if not node1:
			raise Error( 'No node1 for arrow' )

		if not node2:
			raise Error( 'No node2 for arrow' )

		self.__arrows.append( [ node1, node2, color ] )

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
		height = ( 3 + self.get_max_row() ) * ROW_COLUMN_SIZE 
		mod_logging.debug( 'height = {0}'.format( height ) )

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

		for branch in self.__branches:
			if branch.label:
				result += get_latex_text( branch.row, branch.label + ':' )

		for node1, node2, color in self.__arrows:
			result += get_latex_arrow( node1, node2, height, color = color )

		result += '\\end{picture}\n'

		return result

	def __str__( self ):
		return '[graph:{0}]'.format( self.__branches )
