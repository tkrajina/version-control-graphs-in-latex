#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging as mod_logging
import math as mod_math

import cvgraphtex as mod_graph

if __name__ == '__main__':
	mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

	padding = 1200

	graph = mod_graph.Graph( left_padding = padding )

	master_branch = mod_graph.Branch( title = 'master:' )
	master_branch.add_nodes( 'abcdefghij' )
	graph.add_branch( master_branch )

	branch1 = mod_graph.Branch( title = 'development:', start_node = master_branch.get_node( 1 ) )
	branch1.add_nodes( [ 'x', mod_graph.Node( 'y', color = ( .2, .4, .6 ) ), 'z', 'q' ] )
	graph.add_branch( branch1 )

	short_branch = mod_graph.Branch( title = 'short branch', start_node = master_branch.find_node( 'e' ), color = ( 1, 0, 0 ) )
	short_branch.add_nodes( '12' )
	graph.add_branch( short_branch )

	branch2 = mod_graph.Branch( title = 'experiment:', start_node = master_branch.get_node( 5 ) )
	branch2.add_node( mod_graph.Node( 'š' ) )
	branch2.add_node( mod_graph.Node( 'č' ) )
	branch2.add_node( mod_graph.Node( 'ć' ) )
	graph.add_branch( branch2 )

	graph.add_arrow( 'c', 'z', color = ( .7, .7, .7 ) )
	graph.add_arrow( 'q', 'g' )
	graph.add_arrow( 'j', 'ć' )

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

\\begin{document}
"""

	print graph.to_latex_string()

	print 'OK'

	print "\\end{document}"
