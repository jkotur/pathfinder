
import sys
import time

import numpy as np
import numpy.linalg as la
import transformations as tr

from OpenGL.GL import *
from OpenGL.GLU import *

import math as m

if sys.platform.startswith('win'):
    timer = time.clock
else:
    timer = time.time

from block import Block

class Scene :
	def __init__( self ) :
		self.last_time = timer()

		self.blocks = []
		self.new_block = None

	def gfx_init( self ) :
		glClearColor(1,1,1,1)
		self._update_proj()

	def draw( self ) :
		self._update_proj()

		self.time = timer()

		dt = self.time - self.last_time

		self._step( dt )

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self._draw_scene()

		self.last_time = self.time

	def _step( self , dt ) :
		pass

	def _draw_scene( self ) :
		glClear(GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT);

		for b in self.blocks :
			b.draw()

	def _update_proj( self ) :
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho( 0 , self.width , self.height , 0 , -10 , 10 )
		glMatrixMode(GL_MODELVIEW)

	def set_ratio( self , ratio ) :
		self.ratio = ratio
		self._update_proj()

	def set_screen_size( self , w , h ) :
		self.width  = w 
		self.height = h
		self.set_ratio( float(w)/float(h) )

	def mouse_move( self , df , p ) :
		if self.new_block != None :
			self.new_block.set_end( p )

	def mouse_but_pressed( self , but , p ) :
		if but == 3 :
			self.new_block = Block( p )
			self.blocks.append( self.new_block )

	def mouse_but_released( self , but , p ) :
		if but == 3 :
			self.new_block = None

	def key_pressed( self , p ) :
		pass

