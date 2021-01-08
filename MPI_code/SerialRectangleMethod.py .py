
import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import time

COMM= MPI.COMM_WORLD
rank= COMM.Get_rank()
size= COMM.Get_size()

def itegrale_rectangle(x, y, nbi):
    
    integrale =0.
    for i in range(nbi):
        integrale = integrale + y[i]*(x[i+1]-x[i])
        
    return integrale

def plot_integrale(x, y, nbi):
  
    for i in range(nbi):
          # dessin du rectangle
        x_rect = [x[i], x[i], x[i+1], x[i+1], x[i]] # abscisses des sommets
        y_rect = [0   , y[i], y[i]  , 0     , 0   ] # ordonnees des sommets
        plt.plot(x_rect, y_rect,"r")
        
startime = time.process_time()
Xmin = -3*np.pi/2
Xmax = 3*np.pi/2
nx = 40
dx = (Xmax-Xmin)/(nx-1)
nbi = int((nx-1)/size) 
if size==(rank+1):
    nbi+=(nx-1)%size
    xmax = 3*np.pi/2 
    xmin = Xmax-nbi*dx
else:
   xmin =Xmin+rank*nbi*dx
   xmax =Xmin+(rank+1)*nbi*dx
nbxloc = nbi+1
x = np.linspace(xmin, xmax, nbxloc)
y = np.cos(x)
integrale = itegrale_rectangle(x, y, nbi)
#integrale_sum=COMM.reduce(integrale,op=MPI.SUM, root=0)
if rank==0:
    integrale_sum=integrale
    for i in range(1,size):
        pc=COMM.recv(source=i)
        print("processeur",rank,"<---",i)
        integrale_sum+=integrale
else:
    print("processeur",rank,"--->",0)
    COMM.send(integrale,dest=0)
endtime= time.process_time()
if rank==0:
	print('\n')
	print("Integrale =", integrale_sum)
	print("Time spent is",endtime-startime)
plot_integrale(x, y, nbi)
plt.plot(x,y)
plt.plot(x,y,'bo-')   
plt.show()