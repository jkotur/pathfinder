import sys

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

INSIDE = 0 # 0000
LEFT   = 1 # 0001
RIGHT  = 2 # 0010
BOTTOM = 4 # 0100
TOP    = 8 # 1000

class Block( Drawable ) :
	def __init__( self , beg , end = None ) :
		self.beg = beg
		self.end = end if end != None else beg

	def set_beg( self , beg ) :
		self.beg = beg

	def set_end( self , end ) :
		self.end = end

	def gfx_init( self ) :
		pass 

	def draw( self ) :
		glColor3f(1,0,0)
		glBegin(GL_QUADS)
		glVertex3f(self.beg[0],self.beg[1],0)
		glVertex3f(self.beg[0],self.end[1],0)
		glVertex3f(self.end[0],self.end[1],0)
		glVertex3f(self.end[0],self.beg[1],0)
		glEnd()

	def contains( self , p ) :
		xmin = min(self.beg[0],self.end[0])
		xmax = max(self.beg[0],self.end[0])
		ymin = min(self.beg[1],self.end[1])
		ymax = max(self.beg[1],self.end[1])

		return \
				p[0] > xmin and \
				p[0] < xmax and \
				p[1] > ymin and \
				p[1] < ymax

	def intersect( self , p1 , p2 ) :
		''' check line with rectangle intersection based
			on Cohen-Sutherland algorithm '''
		def compcode( p , xmin , xmax , ymin , ymax ) :
			code = INSIDE
			if p[0] < xmin : code |= LEFT
			elif p[0] > xmax : code |= RIGHT 
			if p[1] < ymin : code |= BOTTOM
			elif p[1] > ymax : code |= TOP
			return code

		xmin = min(self.beg[0],self.end[0])
		xmax = max(self.beg[0],self.end[0])
		ymin = min(self.beg[1],self.end[1])
		ymax = max(self.beg[1],self.end[1])

		c1 = compcode( p1 , xmin , xmax , ymin , ymax )
		c2 = compcode( p2 , xmin , xmax , ymin , ymax )

		if c1 | c2 == 0 : return True # both inside
		if c1 & c2 != 0 : return False # both on one side
		if c1 == 0 or c2 == 0 : return True # one outside and one inside
		# both outside

		xb = (p2[0] - p1[0]) * ( ymin - p1[1] ) / ( p2[1] - p1[1] ) + p1[0]
		if xb < xmax and xb > xmin : return True

		xe = (p2[0] - p1[0]) * ( ymax - p1[1] ) / ( p2[1] - p1[1] ) + p1[0]
		if xe < xmax and xe > xmin : return True

		yb = (p2[1] - p1[1]) * ( xmin - p1[0] ) / ( p2[0] - p1[0] ) + p1[1]
		if yb < ymax and yb > ymin : return True

		ye = (p2[1] - p1[1]) * ( xmax - p1[0] ) / ( p2[0] - p1[0] ) + p1[1]
		if ye < ymax and ye > ymin : return True

		return False

