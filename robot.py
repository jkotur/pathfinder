import sys

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

class Robot( Drawable ) :
	def __init__( self , pos , a1 , a2 ) :
		self.pos = pos
		self.a1 = a1
		self.a2 = a2

	def step( self ) :
		pass

	def gfx_init( self ) :
		pass 

	def draw( self ) :
		pass

	def resolve( self , pos ) :
		pass

