import sys

import math as m
import numpy as np

from block import Block
from robot import Robot

class PathFinder :
	def __init__( self , robot , blocks ) :
		self.robot = robot
		self.blocks = blocks

		self.dim = 128

		self.state_map = np.ones((self.dim,self.dim),np.bool)
		self.dists_map = np.zeros((self.dim,self.dim),np.int)

		self.path = []

		self.t = 0

		np.set_printoptions( threshold=200000 ,linewidth = 160 )

	def step( self , dt ) :
		i = int(self.t * len(self.path) / 10.0)

		def dtr( a ) : return a * 2.0 * m.pi / self.dim

		if i < len(self.path) :
			a1 , a2 = map( dtr , self.path[i] ) 

			self.robot.set_state( *map( dtr , self.path[i] ) )

		self.t += dt

	def reset( self ) :
		self.gen_state_map()
		self.find_path()
		self.t = 0.0

	def gen_state_map( self ) :

		def dtr( a ) : return a * 2.0 * m.pi / self.dim

		for a1 in range(0,self.dim) :
			for a2 in range(0,self.dim) :
				beg = self.robot.get_beg()
				mid , end = self.robot.forward( dtr(a1) , dtr(a2) )
				self.state_map[a1,a2] = True
				for b in self.blocks :
#                    if b.contains( beg ) or b.contains( end ) :
					if b.intersect( beg , mid ) or b.intersect( mid , end ) :
						self.state_map[a1,a2] = False
						break


#        print self.state_map

	def find_path( self ) :
		def rtd( a ) :
			a = a if a >= 0.0 else a + 2.0 * m.pi
			return int( a * self.dim / 2.0 / m.pi)

		self.dists_map.fill(0)

		beg = tuple(map( rtd, self.robot.inverse( self.robot.get_start ())))
		end = tuple(map( rtd, self.robot.inverse( self.robot.get_finish())))

#        print self.robot.inverse( self.robot.get_start ())[0] * 180.0 / m.pi , self.robot.inverse( self.robot.get_finish())[0] * 180.0 / m.pi 
#        print beg , end

		self.dists_map[ beg ] = 1

		nebs = [ beg ]

		def tostack( a1 , a2 , l ) :
			if a1 < 0 : a1 += self.dim
			if a2 < 0 : a2 += self.dim
			if a1 >= self.dim : a1 -= self.dim
			if a2 >= self.dim : a2 -= self.dim 

			if self.state_map[a1,a2] == False : return
			if self.dists_map[a1,a2] == 0 or self.dists_map[a1,a2] > l+1 :
				self.dists_map[a1,a2] = l+1
				nebs.append( (a1,a2) )

		res = False
		while len(nebs) > 0 :
			a1 , a2 = nebs.pop(0)

			if (a1,a2) == end :
				res = True
				break

			tostack( a1+1 , a2   , self.dists_map[a1,a2] )
			tostack( a1   , a2+1 , self.dists_map[a1,a2] )
			tostack( a1-1 , a2   , self.dists_map[a1,a2] )
			tostack( a1   , a2-1 , self.dists_map[a1,a2] )

#        print self.dists_map

		if not res :
			print "Path not found:("
			return

		path = [ end ]

		def topath( a1 , a2 , l ) :
			if a1 < 0 : a1 += self.dim
			if a2 < 0 : a2 += self.dim
			if a1 >= self.dim : a1 -= self.dim
			if a2 >= self.dim : a2 -= self.dim 

			if self.dists_map[ a1 , a2   ] == l-1 :
				path.insert( 0 , ( a1 , a2   ) )
				return True
			return False

		while path[0] != beg :
			a1 , a2 = path[0]
			l = self.dists_map[ a1 , a2 ]
			if topath( a1+1 , a2   , l ) : continue
			if topath( a1   , a2+1 , l ) : continue
			if topath( a1-1 , a2   , l ) : continue
			if topath( a1   , a2-1 , l ) : continue

		self.path = path

#        print path

