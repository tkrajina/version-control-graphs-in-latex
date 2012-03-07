#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging as mod_logging

import vcgraphtex as mod_graph

if __name__ == '__main__':
	mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

	graph = mod_graph.Graph( column = 4 )

	graph.add_branch( mod_graph.Branch(
			nodes = 'abcdefgh' ) )

	graph.add_branch( mod_graph.Branch(
			label = 'eksperiment',
			row = 2,
			nodes = 'xyzqw',
			color = ( 0, 0, 1 ),
			branch_from = graph.find_node( 'b' ) ) )

	graph.add_branch( mod_graph.Branch(
			label = 'eksperiment 2',
			row = 1,
			nodes = [ '1', '2', '3', mod_graph.Node( '4', color = ( 0, 0, 1 ) ), '5' ],
			color = ( 1, 0, 0 ),
			branch_from = graph.find_node( 'g' ) ) )

	graph.add_arrow( 'd', 'z', color = ( 0, 1, 0 ) )
	graph.add_arrow( 'q', 'g' )

	# TODO: node color
	# TODO: branch label

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

	print
	print 'OK'
	print

	print graph.get_latex_string()

	print
	print 'OK'
	print

	print "\\end{document}"
