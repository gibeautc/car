#!/usr/bin/env python

from PIL import Image


class Pos:
	#pos object
	def __init__(self,x,y):
		self.x=x
		self.y=y
class Block:
	#block object, can have 
	blockSize=12
	def __init__(self):
		self.value=128
		#value will be the probabilty of block being occupied
		#middle of the road will be unknow, then up for better change, down for lower
		self.loc=128
		#loc is chance that block is our current location
		# neg is unknown, 0 is clear, >0 chance of being blocked


class World:
	def __init__(self):
		self.grid=[]
		self.xlen=300
		self.ylen=300
		for x in range(self.xlen):
			row=[]
			for y in range(self.ylen):
				row.append(Block())
			self.grid.append(row)
	def PrintWorld(self):
		#want to have 500x500 image
		imgSize=500
		img=Image.new('RGB',(self.xlen,self.ylen),"black")
		pix=img.load()
		
		for x in range(self.xlen):
			for y in range(self.ylen):
				pix[x,y]=(self.grid[x][y].value,self.grid[x][y].value,0)
		img.save('img.pgm')
		

def main():
	world=World()
	world.PrintWorld()
					

if __name__ =="__main__":
	main()
			
