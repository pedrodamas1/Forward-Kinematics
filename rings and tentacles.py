# links make chains
# rings make tentacles

import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


###########################################################################################################

class Ring:

	def __init__(self, length, radius, points):

		self.length = length
		self.radius = radius
		self.points = points

		angles = np.linspace(0,2*np.pi,points)
		self.x = np.ones(points)*length
		self.y = radius*np.cos(angles)
		self.z = radius*np.sin(angles)

		self.pos = np.array([self.x, self.y, self.z])
		self.posRot = self.posTrans = self.pos # relevant variables

		self.avgPoint = np.average(self.posTrans, axis=1)


	def rotate(self, alpha, beta, gama):

		Rz = np.array([	[np.cos(alpha),	-np.sin(alpha),	0],
						[np.sin(alpha), np.cos(alpha),	0],
						[0, 			0, 				1]])

		Ry = np.array([	[np.cos(beta),	0,	np.sin(beta)],
						[0,				1,	0],
						[-np.sin(beta),	0,	np.cos(beta)]])

		Rx = np.array([	[1,	0, 				0],
						[0,	np.cos(gama),	-np.sin(gama)],
						[0,	np.sin(gama),	np.cos(gama)]])

		self.posRot = np.matmul( np.matmul( np.matmul( Rz, Ry), Rx), self.pos)
		self.posTrans = self.posRot
		self.avgPoint = np.average(self.posTrans, axis=1)
		return None

	def translate(self, d):
		dx,dy,dz = d

		T = np.array([	[1, 0, 0, dx],
						[0, 1, 0, dy],
						[0, 0, 1, dz],
						[0, 0, 0, 1]])

		posRotTemp = np.append(self.posRot, np.ones((1,self.points)), axis=0 )
		posTransTemp = np.matmul( T, posRotTemp )
		self.posTrans = posTransTemp[0:3][:]
		self.avgPoint = np.average(self.posTrans, axis=1)
		return None


###########################################################################################################

class Tentacle:

	def __init__(self, number, length, radius, points):

		self.number = number # number of rings
		self.length = length # length of each ring
		self.radius = radius # radius of the rings
		self.points = points # number of points for each ring

		self.rings = []
		self.angles = np.zeros((3,number))

		# create the rings objects
		for _ in range(number):
			self.rings.append( Ring(length, radius, points) )


	def assemble(self):
		#Now, rotate, translate and update posPlot
		for i in range(self.number):
			# collect angles and rotate
			alpha, beta, gama = self.angles
			self.rings[i].rotate(alpha[i], beta[i], gama[i])

			if i>0:
				end_pos = self.rings[i-1].avgPoint
				self.rings[i].translate(end_pos)




tentacleDemo = True
if tentacleDemo:
	
	# This import registers the 3D projection, but is otherwise unused.
	from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
	import matplotlib.pyplot as plt
	import random

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_aspect('equal')

	N = 5

	myTentacle = Tentacle(N,1,.3,10)
	#myTentacle.angles = np.array([
	#	np.linspace(0,0.2,N),
	#	np.zeros(N),
	#	np.zeros(N)])
	myTentacle.angles = np.array([
		np.random.rand(N),
		np.zeros(N),
		np.zeros(N)])
	myTentacle.assemble()

	XX, YY, ZZ =  [], [], []

	for i in range(N):
		thisRing = myTentacle.rings[i]
		x,y,z = thisRing.posTrans
		XX.append( x.tolist() )
		YY.append( y.tolist() )
		ZZ.append( z.tolist() )

		ax.scatter(x, y, z, label=str(i))
	
	XX = np.asarray(XX)
	YY = np.asarray(YY)
	ZZ = np.asarray(ZZ)

	ax.plot_surface(XX,YY,ZZ)
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	ax.set_xlim(-3,5)
	ax.set_ylim(-3,5)
	ax.set_zlim(-3,5)

	ax.legend()
	plt.show()


'''


def update_plot():
	thisChain.angles = np.random.rand(3,N)*-3
	thisChain.assemble()
	x,y,z = thisChain.posPlot
	ax.clear()
	ax.plot(x,y,z, 'bo-')
	canvas.draw()
	root.after(2000, update_plot)
	return None



import tkinter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

ax = fig.add_subplot(111, projection="3d")
ax.plot(x,y,z, 'bo-')
ax.plot(2*x+1,y,z, 'bo-')

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


ax.set_xlim(-3, 5)
ax.set_ylim(-3, 5)
ax.set_zlim(-3, 5)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

root.after(2000, update_plot)
root.mainloop()


'''




ringDemo = False
if ringDemo:

	thisRing = Ring(1,1,12)
	x1,y1,z1 = thisRing.posTrans
	thisRing.rotate(0.5,0,0)
	x2,y2,z2 = thisRing.posTrans
	thisRing.translate([1,0,0])
	x3,y3,z3 = thisRing.posTrans
	x4,y4,z4 = thisRing.avgPoint

	# This import registers the 3D projection, but is otherwise unused.
	from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_aspect('equal')

	ax.scatter(x1, y1, z1, label='original')
	ax.scatter(x2, y2, z2, label='rot')
	ax.scatter(x3, y3, z3, label='trans')
	ax.scatter(x4, y4, z4, label='avg')

	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	ax.set_xlim(-3,3)
	ax.set_ylim(-3,3)
	ax.set_zlim(-3,3)

	ax.legend()
	plt.show()
