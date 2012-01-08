
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

from robot import Robot
from block import Block
from finder import PathFinder

class Scene :
	def __init__( self ) :
		self.last_time = timer()

		self.robot = Robot( (400,400) , (300,300) )
		self.move_robot = False

		self.blocks = []
		self.new_block = None

		self.finder = PathFinder( self.robot , self.blocks )

		self.anim = False

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
		if self.anim :
			self.finder.step( dt )

	def _draw_scene( self ) :
		glClear(GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT);

		for b in self.blocks :
			b.draw()

		self.robot.draw()

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
		if self.move_robot :
			self.robot.set_end( p )
		if self.new_block != None :
			self.new_block.set_end( p )

	def mouse_but_pressed( self , but , p ) :
		if but == 1 :
			self.robot.set_end( p )
			self.move_robot = True
		elif but == 3 :
			self.new_block = Block( p )
			self.blocks.append( self.new_block )

	def mouse_but_released( self , but , p ) :
		if but == 1 :
			self.move_robot = False
		elif but == 3 :
			self.new_block = None

	def key_pressed( self , key ) :
		pass

	def set_start_point( self ) :
		self.robot.set_start( self.robot.get_end() )

	def set_finish_point( self ) :
		self.robot.set_finish( self.robot.get_end() )

	def set_robot_params( self , l1 , l2 ) :
		self.robot.set_params( l1 , l2 )

	def anim_toggle( self ) :
		self.anim = not self.anim

	def anim_reset( self ) :
		self.finder.reset()

