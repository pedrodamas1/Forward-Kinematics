# links make chains
# rings make tentacles

import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Link:

	def __init__(self, length):

		self.L = length
		self.pos = np.zeros((3,2)) # x1 x2 # y1 y2 # z1 z2
		self.pos[0][1] = length
		self.posRot = self.posTrans = self.pos # relevant variables

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
		return None

	def translate(self, d):
		#self.posTrans = self.posRot + 
		dx,dy,dz = d

		T = np.array([	[1, 0, 0, dx],
						[0, 1, 0, dy],
						[0, 0, 1, dz],
						[0, 0, 0, 1]])

		posRotTemp = np.append(self.posRot, np.array([[1,1]]), axis=0 )
		posTransTemp = np.matmul( T, posRotTemp )
		self.posTrans = posTransTemp[0:3][:]

		return None


class Chain:

	# use inheritance?
	def __init__(self, number, size):

		self.number = number # number of links
		self.size = size # size of each link
		self.links = []
		self.angles = np.zeros((3,number))
		self.posPlot = np.zeros((3,number))

		# create the link objects
		for i in range(number):
			self.links.append( Link(size) )


	def assemble(self):
		'''
		Now, rotate, translate and update posPlot
		'''
		for i in range(self.number):
			# collect angles and rotate
			alpha, beta, gama = self.angles
			self.links[i].rotate(alpha[i], beta[i], gama[i])

			if i>0:
				end_pos = self.links[i-1].posTrans[:,1]
				self.links[i].translate(end_pos)

			x,y,z = self.links[i].posTrans[:,1]
			self.posPlot[0,i] = x
			self.posPlot[1,i] = y
			self.posPlot[2,i] = z
		



N = 3
thisChain = Chain(N, 1)
thisChain.angles = np.random.rand(3,N)*-3
thisChain.assemble()

x,y,z = thisChain.posPlot




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


