
import random 
import timeit
from mpi4py import MPI

COMM = MPI.COMM_WORLD
rank= COMM.Get_rank()
size= COMM.Get_size()

inter= 100000
nbi=int((inter)/(size))
if size==rank+1:
    nbi=nbi+(inter)%size
random.seed(42)  

def génération_des_points():
    random.seed(42)  
    pc= 0
    for i in range(nbi): 
        rand_x= random.uniform(-1, 1) 
        rand_y= random.uniform(-1, 1) 
        odist = rand_x**2 + rand_y**2  
        if odist<= 1: 
           pc+= 1
    return pc

start = timeit.default_timer()
pc=génération_des_points()
#total_cp=COMM.reduce(pc,op=MPI.SUM, root=0)
if rank==0:
    total_cp=pc
    for i in range(1,size):
        pc=COMM.recv(source=i)
        print("processeur",rank,"<---",i)
        total_cp+=pc
else:
    print("processeur",rank,"--->",0)
    COMM.send(pc,dest=0)
end = timeit.default_timer()
if rank==0:
	pi = 4* total_cp/ inter
	print("Pi~=", pi,"\n", "le temp de l'exicution",end-start) 
