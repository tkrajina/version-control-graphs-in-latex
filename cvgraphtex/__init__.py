#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging as mod_logging
import math as mod_math

NODE_RADIUS = 150

ROW_COLUMN_SIZE = 500

def distance( x1, y1, x2, y2 ):
	return mod_math.sqrt( ( x2 - x1 ) ** 2 + ( y2 - y1 ) ** 2 )

def get_latex_arrow( node1, node2, left_padding, color = None ):
	color = color if color else ( 0, 0, 0 )

	x1 = node1.x
	y1 = node1.y
	x2 = node2.x
	y2 = node2.y

	vector_x = ( x2 - x1 ) / ROW_COLUMN_SIZE
	vector_y = ( y2 - y1 ) / ROW_COLUMN_SIZE

	if vector_x == 0:
		length = ROW_COLUMN_SIZE * abs( vector_y )
	else:
		length = ROW_COLUMN_SIZE * abs( vector_x )

	length = length * .9

	return '\\thicklines{\\color[rgb]{' + str( color[ 0 ] ) + ',' + str( color[ 1 ] ) + ',' + str( color[ 2 ] ) + '}\\put(' + str( left_padding + x1 ) + ',' + str( y1 ) + '){\\vector(' + str( vector_x ) + ',' + str( vector_y ) + '){' + str( length ) + '}}}%\n'

class Node:
	
	label = None

	# x and y will be set only at the moment the LaTeX string is built:
	x = None
	y = None

	color = None

	def __init__( self, label, color = None ):
		self.label = label
		self.x = None
		self.y = None

		self.color = color if color else ( 0, 0, 0, )

	def to_latex_string( self, x, y, left_padding ):
		self.x = x
		self.y = y

		mod_logging.debug( 'Node {0} to ({1},{2})'.format( self.label, self.x, self.y ) )

		result = '\\put(' + str( left_padding + x - 50 ) + ',' + str( y + 140 ) + '){\\makebox(0,0)[lb]{\\smash{{\\SetFigFont{12}{14.4}{\\rmdefault}{\\mddefault}{\\updefault}{\\textit{' + self.label + '}}}}}}%\n'
		result += '{\\color[rgb]{' + str( self.color[ 0 ] ) + ',' + str( self.color[ 1 ] ) + ',' + str( self.color[ 2 ] ) + '}\\put(' + str( left_padding + x ) + ',' + str( y ) + '){\\circle*{' + str( NODE_RADIUS ) + '}}}%\n'

		return result

	def __str__( self ):
		return '[node:{0},{1}]'.format( self.x, self.y )

class Branch:

	title = None

	__nodes = None

	start_node = None

	color = None

	def __init__( self, title = None, start_node = None, color = None ):
		self.title = title
		self.__nodes = []
		self.start_node = start_node
		self.color = color if color else ( 0, 0, 0 )

	def add_node( self, node ):
		""" Node may be instance of Node or string (note label) """
		if isinstance( node, Node ):
			self.__nodes.append( node )
		else:
			self.__nodes.append( Node( node, color = self.color ) )

	def add_nodes( self, nodes ):
		for node in nodes:
			self.add_node( node )

	def get_node( self, index ):
		return self.__nodes[ index ]

	def find_node( self, node_label ):
		for node in self.__nodes:
			if node.label == node_label:
				return node

		return None

	def to_latex_string( self, y, left_padding ):
		result = ''

		mod_logging.debug( 'Branch starting at {0}'.format( y ) )

		if self.start_node:
			start_x = self.start_node.x + ROW_COLUMN_SIZE
		else:
			start_x = 0
		start_y = y

		if self.title:
			result = '\\put(' + str( 0 ) + ',' + str( y ) + '){\\makebox(0,0)[lb]{\\smash{{\\SetFigFont{12}{14.4}{\\rmdefault}{\\mddefault}{\\updefault}{\\textit{' + self.title + '}}}}}}%\n'

		# Nodes:
		for index, node in enumerate( self.__nodes ):
			result += node.to_latex_string( x = start_x + index * ROW_COLUMN_SIZE, y = start_y, left_padding = left_padding )

		#Arrows
		for index, node in enumerate( self.__nodes ):
			if index < len( self.__nodes ) - 1:
				next_node = self.__nodes[ index + 1 ]
				result += get_latex_arrow( node, next_node, left_padding = left_padding, color = self.color )

		if self.start_node:
			mod_logging.debug( "start node:" + str( self.start_node ) )
			mod_logging.debug( "first node:" + str( self.__nodes[ 0 ] ) )
			result += get_latex_arrow( self.start_node, self.__nodes[ 0 ], left_padding = left_padding, color = self.color )

		return result

class Graph:

	__branches = None

	__arrows = None

	left_padding = None

	def __init__( self, left_padding = None ):
		self.__branches = []
		self.left_padding = left_padding if left_padding else 0
		self.__arrows = []

	def find_node( self, node_label ):
		for branch in self.__branches:
			node = branch.find_node( node_label )
			if node:
				return node
		return None

	def add_branch( self, branch ):
		self.__branches.append( branch )

	def get_branch( self, index ):
		return self.__branches[ index ]

	def add_arrow( self, node1, node2, color = None ):
		if not isinstance( node1, Node ):
			node1 = self.find_node( node1 )
		if not isinstance( node2, Node ):
			node2 = self.find_node( node2 )

		self.__arrows.append( [ node1, node2, color ] )

	def to_latex_string( self ):
		width = 2000
		height = len( self.__branches ) * ROW_COLUMN_SIZE

		result = '\\setlength{\\unitlength}{4144sp}%\n'
		result += '\\begingroup\\makeatletter\\ifx\\SetFigFont\\undefined%\n'
		result += '\\gdef\\SetFigFont#1#2#3#4#5{%\n'
		result += '  \\reset@font\\fontsize{#1}{#2pt}%\n'
		result += '  \\fontfamily{#3}\\fontseries{#4}\\fontshape{#5}%\n'
		result += '  \\selectfont}%\n'
		result += '\\fi\\endgroup%\n'
		result += '\\begin{picture}(' + str( width ) + ',' + str( height ) + ')(0,0)%\n'

		start_y = height

		for index, branch in enumerate( self.__branches ):
			result += branch.to_latex_string( y = start_y - index * ROW_COLUMN_SIZE, left_padding = self.left_padding )

		for arrow in self.__arrows:
			arrow_x, arrow_y, color = arrow
			mod_logging.debug( 'arrow color: {0}'.format( color ) )
			result += get_latex_arrow( arrow_x, arrow_y, color = color, left_padding = self.left_padding )

		result += '\\end{picture}\n'

		return result

	def get_latex_arrow( self, node1, node2 ):
		return get_latex_arrow( node1, node2, left_padding = self.left_padding )