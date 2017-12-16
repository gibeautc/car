#!/usr/bin/env python
import random
import sys
from PIL import Image
random.seed()


worldSize=20

step=False
smart=False
safe=False
adventure=100

def mapVal(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



class Pos:
	def __init__(self,x,y):
		self.x=x
		self.y=y
class Block:
	bmin=500000
	bmax=0
	def __init__(self,x):
		self.val=-1.0
		self.obj=x
		self.visited=0

class World:
	def __init__(self):
		self.grid=[]
		self.pos=Pos(0,0)
		self.StartPos=Pos(0,0)
		self.cnt=0
		self.alive=True
	def pos(self,p):
		return self.grid[p.x][p.y]
	def print_state(self):
		for x in range(worldSize):
			for y in range(worldSize):
				print(str(self.grid[x][y].obj)+" "),
			print("\t"),
			for y in range(worldSize):
				print(str("{:1.2f}".format(self.grid[x][y].val))+" "),
			print("")
		print("Starting Pos: "+str(self.StartPos.x)+","+str(self.StartPos.y))	
		print("Current  Pos: "+str(self.pos.x)+","+str(self.pos.y))
		print("Current Cnt: "+str(self.cnt))
	def move(self,x,y):
		self.pos.x=x
		self.pos.y=y	
		self.cnt+=1
		self.grid[x][y].visited+=1
		if self.grid[x][y].visited<Block.bmin:
			Block.bmin=self.grid[x][y].visited
		if self.grid[x][y].visited>Block.bmax:
			Block.bmax=self.grid[x][y].visited



def chance(opt,chan):
	#given in two lists
	#[1,2,3] and [50,25,25]
	#if the chances dont add up to 100 then the remander of the time None is an option
	master=[]
	for i in chan:
		if i!=int(i):
			for n in range(len(chan)):
				chan[n]=chan[n]*100
	rem=100-sum(chan)
	for n in range(len(opt)):
		for x in range(chan[n]):
			master.append(opt[n])
	for x in range(rem):
		master.append(None)
	random.shuffle(master)
	return master[0]	
	
def load_map():
	try:
		f=open("aimap",'r')
	except:
		print("No map file... attemping to make one")
		make_map()
		f=open("aimap",'r')
	data=f.read()
	data=data.split("\n")
	world=World()
	rowc=0
	have_start=False
	for line in data:
		row=[]
		el=line.split(",")
		col=0
		for e in el:
			if not have_start:
				if e=='0':
					have_start=True
					world.StartPos.x=rowc
					world.StartPos.y=col
			col+=1
			try:
				row.append(Block(int(e)))
				
			except:
				pass	
		world.grid.append(row)
		rowc+=1
		worldSize=len(world.grid)
	print("Map loaded")
	return world

		
def make_map():
	mmap=World()
	goal=random.randint(0,worldSize*worldSize)
	cnt=0
	for x in range(worldSize):
		row=[]
		for y in range(worldSize):

			i=random.randint(0,10)
			if i<7:
				v=0
			elif i<9:
				v=1	#block
			else:
				v=2	#death
			if cnt==goal:
				v=3	#goal
			row.append(v)
			cnt+=1
		mmap.grid.append(row)
	f=open("aimap","w")
	for x in range(worldSize):
		for y in range(worldSize):
			f.write(str(mmap.grid[x][y]))
			if y<worldSize-1:
				f.write(",")
		f.write("\n")	
	f.close()
	#return mmap,space




			
def look(world):
	#look around
	#right now just 4 pos directions, up,down,left,right
	#up x-1
	#down x+1
	#left y-1
	#right y+1
	#-1 means that is off the world
	#0,1,2,3 match the int in the world def
	obj=[-1,-1,-1,-1]
	val=[-1,-1,-1,-1]
	#print("I am at: "+str(pos.x)+","+str(pos.y))
	#print("Looking")
	if world.pos.y==worldSize-1:
		upy=0
	else:
		upy=world.pos.y+1
	if world.pos.y==0:
		downy=worldSize-1
	else:
		downy=world.pos.y-1
	if world.pos.x==worldSize-1:
		upx=0
	else:
		upx=world.pos.x+1
	if world.pos.x==0:
		downx=worldSize-1
	else:
		downx=world.pos.x-1	
	obj[0]=world.grid[downx][world.pos.y].obj
	obj[1]=world.grid[upx][world.pos.y].obj
	obj[2]=world.grid[world.pos.x][downy].obj
	obj[3]=world.grid[world.pos.x][upy].obj
	
	val[0]=world.grid[downx][world.pos.y].val
	val[1]=world.grid[upx][world.pos.y].val
	val[2]=world.grid[world.pos.x][downy].val
	val[3]=world.grid[world.pos.x][upy].val
	myval=0.0
	for v in val:
		if v>myval:
			myval=v
	world.grid[world.pos.x][world.pos.y].val=myval*0.95
	return obj,val
def move(world,d):
	#up,down,left,right   0,1,2,3
	#right now it is deterministic, always goes where you want
	#r=random.randint(0,700)
	#err=0
	#act_d=d
	#if r==1:
#		err=1
#	if r==2:
#		err=2
	
	correct=98
	side=(100-correct)
	
	if d==0:
		act_d=chance([0,2,3],[correct,side,side])
	if d==1:
		act_d=chance([1,2,3],[correct,side,side])
	if d==2:
		act_d=chance([2,0,1],[correct,side,side])
	if d==3:
		act_d=chance([3,0,1],[correct,side,side])
	
	#if d==0:
		#if err==1:
			#act_d=2
		#if err==2:
			#act_d=3
	
	#if d==1:
		#if err==1:
			#act_d=2
		#if err==2:
			#act_d=3
			
	#if d==2:
		#if err==1:
			#act_d=1
		#if err==2:
			#act_d=0
			
	#if d==3:
		#if err==1:
			#act_d=1
		#if err==2:
			#act_d=0
			
		

		
	x=0
	y=0
	#perposed direction- mainly to check if we see the goal
	if d==0:
		x=-1
	elif d==1:
		x=1
	elif d==2:
		y=-1
	elif d==3:
		y=1
	else:
		print("move error")
	
	newx=world.pos.x+x
	newy=world.pos.y+y
	if newx<0:
		newx=newx+worldSize
	if newy<0:
		newy=newy+worldSize
	if newx>worldSize-1:
		newx=newx-worldSize
	if newy>worldSize-1:
		newy=newy-worldSize
		
	if world.grid[newx][newy].obj==3:
		#found goal
		world.grid[newx][newy].val=1.0
	
	#actual direction
	if act_d==0:
		x=-1
	elif act_d==1:
		x=1
	elif act_d==2:
		y=-1
	elif act_d==3:
		y=1
	else:
		print("move error")
	
	newx=world.pos.x+x
	newy=world.pos.y+y
	
	
	
	
		
	if newx<0:
		newx=newx+worldSize
	if newy<0:
		newy=newy+worldSize
	if newx>worldSize-1:
		newx=newx-worldSize
	if newy>worldSize-1:
		newy=newy-worldSize
		
	#print("Move from:"+str(world.pos.x)+","+str(world.pos.y))
	#print("To: "+str(newx)+","+str(newy))
	if world.grid[newx][newy].obj==1:
		#print("Cant Go there, Blocked")
		#if world.grid[newx][newy].val<0:
		#	world.grid[world.pos.x][world.pos.y].val=0.0
		world.cnt+=1
		return
	if world.grid[newx][newy].obj==2:
		#print("You Died")
		if safe:
			world.grid[world.pos.x][world.pos.y].val=world.grid[world.pos.x][world.pos.y].val *0.2
		world.cnt=55555
		world.alive=False
		return
	if world.grid[newx][newy].val<0:
		world.grid[newx][newy].val=0.0		
	
	world.move(newx,newy)
	
def decide(l1,l2):
	
	
	#right now just makes a random desicion on which direction to go
	#print("list1: " +str(l1))
	#print("list2: " +str(l2))
	m=max(l2)
	#print("Max: "+str(m))
	if m<=0 or not smart:
		random.shuffle(l1)
		return l1[0]
	
	i=l2.index(m)
	if adventure>0:
		other=(100-adventure)/len(l1)
		other=int(other)
		chan=[]
		for x in range(len(l1)):
			if x==i:
				chan.append(adventure)
			else:
				chan.append(other)
		return chance(l1,chan)
				
		
	
	#return l1[i]

def start(world):
	#print("\n\n")
	world.pos.x=world.StartPos.x
	world.pos.y=world.StartPos.y
	world.cnt=0
	found_goal=False
	world.alive=True
	while not found_goal:
		if not world.alive:
			return world.cnt
		if world.cnt>50000:
			print("Giving up")
			return 50000
		if step:
			world.print_state()
			n=raw_input("Next")
		look_res,val_res=look(world)
		#print("I looked around and see: "+str(look_res))
		l1=[]
		l2=[]
		for x in range(4):
			if look_res[x]==3:
				#Found the goal
				#world.grid[world.pos.x][world.pos.y].val=1.0
				move(world,x)
				found_goal=True
				return (world.cnt)
			if look_res[x]==0:
				#can go this way, add to list of possible movements
				l1.append(x)
				l2.append(val_res[x])
		if len(l1)==0:
			print("no place to move")
			return
		d=decide(l1,l2)
		move(world,d)

def makeImage(world):
	#want to have 500x500 image
		img=Image.new('RGB',(worldSize,worldSize),"black")
		pix=img.load()
		
		for x in range(worldSize):
			for y in range(worldSize):
				#pix[x,y]=(self.grid[x][y].value,self.grid[x][y].value,0)
				o=world.grid[x][y].obj
				if o==0:
					v=world.grid[x][y].val
					m=int(mapVal(v,Block.bmin,Block.bmax,0,255))
					pix[x,y]=(0,0,m)
				if o==1:
					pix[x,y]=(0,255,0)
				if o==2:
					pix[x,y]=(255,0,0)
		img.save('img.pgm')


def main():
	global safe
	global smart
	#start up
	res=[]
	num=50
	if len(sys.argv)>1:
		for a in sys.argv:
			if 'n' in a:
				print("making new map")
				make_map()
			if 'c' in a:
				try:
					num=int(sys.argv[sys.argv.index(a)+1])
					print("new count: "+str(num))
				except:
					print("Not a number")
			if 'safe' in a:
				safe=True	
			if 'smart' in a:
				smart=True
			if 'ad' in a:
				try:
					adventure=int(sys.argv[sys.argv.index(a)+1])
					print("Adventure Level: "+str(num))
				except:
					print("Not a number")
	Map=load_map()
	Map.print_state
	low=50000
	for x in range(num):
		print("."),
		r=start(Map)
		res.append(r)
		#if r<low:
		#	low=r
		#if r>low:
		#	print("Current Low: "+str(low))
			#Map.print_state()
			#n=raw_input("Next")
	print("")
	Map.print_state()
	total=0
	cnt=0
	most=0
	least=50001
	for n in res:
		if n<0:
			continue
		if n<50000:
			try:
				total+=n
				cnt+=1
				if n>most:
					most=n
				if n<least:
					least=n
			except:
				pass
	availCell=0
	seenCell=0
	evalCell=0	
	for x in range(worldSize):
		for y in range(worldSize):
			if Map.grid[x][y].obj==0:
				availCell+=1
				if Map.grid[x][y].val>=0:
					seenCell+=1
				if Map.grid[x][y].val>0:
					evalCell+=1
	print("Adventure: "+str(adventure))
	print("Smart: "+str(smart))
	print("Safe: "+str(safe))
	print("Average for successfull maps:"+str(total/cnt))
	print("Percent Successful: "+str(float(cnt)/float(num)))
	print("Percent Cells seen: "+str(float(seenCell)/float(availCell)))
	print("Percent Cells evaluated: "+str(float(evalCell)/float(availCell)))
	print("Max: "+str(most))
	print("Min: "+str(least))
	makeImage(Map)
	#print(res)

if __name__=="__main__":
		main()
