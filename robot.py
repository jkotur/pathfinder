import sys

import math as m
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

class Robot( Drawable ) :
	def __init__( self , beg , end ) :
		self.l1 = 200
		self.l2 = 100

		self.beg = np.array( beg )
		self.end = np.array( end )

		self.mid = self.resolve()

	def set_beg( self, beg ) :
		self.beg = np.array( beg )
		self.mid = self.resolve()

	def set_end( self, end ) :
		self.end = np.array( end )
		self.mid = self.resolve()

	def step( self ) :
		pass

	def gfx_init( self ) :
		pass 

	def draw( self ) :
		mid = self.resolve()

		glColor3f(0,0,0)
		glBegin(GL_LINE_STRIP)
		glVertex3f(self.beg[0],self.beg[1],0)
		glVertex3f(self.mid[0],self.mid[1],0)
		glVertex3f(self.end[0],self.end[1],0)
		glEnd()

	def resolve( self ) :
		try :
			p = self.end - self.beg
			l = np.linalg.norm( p )
			l1 = self.l1
			l2 = self.l2

			c2 = (l*l + l2*l2 - l1*l1)/(2.0*l*l2)
			c1 = (l-l2*c2)/l1

			a22 = m.acos( c2 )
			a12 = m.acos( c1 )

			a11 = m.atan2( p[1] , p[0] )
			a21 = a22 - a11

			x1 = l1 * m.cos( a11 + a12 )
			y1 = l1 * m.sin( a11 + a12 )
		except ValueError as e :
			print e
			x1 = 0
			y1 = 0

		return self.beg + np.array((x1,y1))

