import sys

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

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

