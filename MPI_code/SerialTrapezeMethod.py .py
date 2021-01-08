import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import time

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()



def compute_integrale_trapeze(x, y, nbi):

    integrale = 0.
    for i in range(nbi):
        trap = (x[i+1]-x[i])/2 * (y[i]+y[i+1])
        integrale = integrale + trap
    return integrale

def plot_integrale(x, y, nbi):
    for i in range(nbi):
        # dessin du rectangle
        x_trap = [x[i], x[i], x[i+1], x[i+1], x[i]] # abscisses des sommets
        y_trap = [0   , y[i], y[i+1],      0,        0   ] # ordonnees des sommets
        plt.plot(x_trap, y_trap,"r")
    
    return 0

t0 = time.process_time()
Xmin = 0
Xmax = 3*np.pi/2
nbx = 20  # max nbr of iterations
dx = (Xmax-Xmin)/(nbx-1) # space step
nbi = int((nbx-1)/size) 

if size == rank+1:
	nbi += (nbx-1)%size

if rank== (size-1):
   xmax = 3*np.pi/2
   xmin = Xmax-nbi*dx
else:
   xmin =Xmin+rank*nbi*dx
   xmax =Xmin+(rank+1)*nbi*dx 

nn= nbi+1
x = np.linspace(xmin, xmax, nn)
y = np.cos(x)

integrale = compute_integrale_trapeze(x, y, nbi)
integraletotal=COMM.reduce(integrale,op=MPI.SUM, root=0)
t1 = time.process_time()
if rank==0:
	print('\n')
	print("Integrale =",integraletotal)
	print("Time spent is",t1 - t0)
plot_integrale(x, y, nbi)
plt.plot(x,y,'bo-')   
plt.show()