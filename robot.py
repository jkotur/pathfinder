import sys

import math as m
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

class Robot( Drawable ) :
	def __init__( self , beg , end ) :
		self.l1 = 1
		self.l2 = 1

		self.beg = np.array( beg )
		self.end = np.array( end )

		self.start_end = None
		self.finish_end = None

		self.mid , self.end = self.inverse_pos( self.beg , self.end , self.l1 , self.l2 )

	def get_beg( self ) :
		return self.beg

	def get_end( self ) :
		return self.end

	def get_start( self ) :
		return self.start_end

	def get_finish( self ) :
		return self.finish_end

	def set_beg( self, beg ) :
		self.beg = np.array( beg )
		self.mid , self.end = self.inverse_pos( self.beg , self.end , self.l1 , self.l2 )

	def set_end( self, end ) :
		self.end = np.array( end )
		self.mid , self.end = self.inverse_pos( self.beg , self.end , self.l1 , self.l2 )

	def set_start( self , end ) :
		self.start_end = np.array(end)
		self.start_mid , self.start_end = self.inverse_pos( self.beg , self.start_end , self.l1 , self.l2 )

	def set_finish( self , end ) :
		self.finish_end = np.array(end)
		self.finish_mid , self.finish_end = self.inverse_pos( self.beg , self.finish_end , self.l1 , self.l2 )

	def set_params( self , l1 , l2 ) :
		self.l1 = l1
		self.l2 = l2
		self.mid , self.end = self.inverse_pos( self.beg , self.end , self.l1 , self.l2 )
		if self.start_end != None :
			self.start_mid , self.start_end = self.inverse_pos( self.beg , self.start_end , self.l1 , self.l2 )
		if self.finish_end != None :
			self.finish_mid , self.finish_end = self.inverse_pos( self.beg , self.finish_end , self.l1 , self.l2 )

	def gfx_init( self ) :
		pass 

	def draw( self ) :
		glColor3f(0,0,0)
		self.draw_robot( self.beg , self.mid , self.end )

		if self.start_end != None :
			glColor3f(0,1,0)
			self.draw_robot( self.beg , self.start_mid , self.start_end )
		if self.finish_end != None :
			glColor3f(0,0,1)
			self.draw_robot( self.beg , self.finish_mid , self.finish_end )

	def draw_robot( self , beg , mid , end ) :
		glBegin(GL_LINE_STRIP)
		glVertex3f(beg[0],beg[1],0)
		glVertex3f(mid[0],mid[1],0)
		glVertex3f(end[0],end[1],0)
		glEnd()

	def set_state( self , a1 , a2 ) :
		self.mid , self.end = self.forward( a1 , a2 )

	def forward( self , a1 , a2 ) :
		return self._forward( self.beg , a1 , a2 , self.l1 , self.l2 )

	def _forward( self , beg , a1 , a2 , l1 , l2 ) :
		x1 = l1 * m.cos(a1)
		y1 = l1 * m.sin(a1)
		x2 = l2 * m.cos(a2)
		y2 = l2 * m.sin(a2)
		mid = beg + np.array((x1,y1))
		end = mid + np.array((x2,y2))
		return mid , end

	def inverse_pos( self , beg , end , l1 , l2 ) :
		a1 , a2 = self._inverse( beg , end , l1 , l2 )
		return self._forward( beg , a1 , a2 , l1 , l2 )

	def _inverse( self , *args ) :
		try :
			return self.inverse_throw( *args )
		except ValueError as e :
			return 0.0 , 0.0

	def inverse( self , end ) :
		return self._inverse( self.beg , end , self.l1 , self.l2 )

	def inverse_throw( self , beg , end , l1 , l2 ) :
		p = end - beg
		l = np.linalg.norm( p )

		c2 = (l*l + l2*l2 - l1*l1)/(2.0*l*l2)
		c1 = (l-l2*c2)/l1

		a22 = m.acos( c2 )
		a12 = m.acos( c1 )

		a11 = m.atan2( p[1] , p[0] )
		a21 = a22 + a11

		a1 = a11+a12
		a2 = a11-a22

		return a1 , a2

