import random
import numpy as np
import timeit
from mpi4py import MPI

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size= COMM.Get_size()

def f(x):
    return np.sin(x)
    
a=0
b=np.pi # b>a
inter=100
x=np.linspace(a,b,inter)
y=f(x)
fmin=min(y)
fmax=max(y)
Area_rectangle=abs(b-a)*abs(fmax-fmin)
nbi=int((inter)/(size))
if size==rank+1:
    nbi=nbi+(inter)%size    

random.seed(45)
def Integration_de_MonteCarlo():
    random.seed(45)
    pr=0
    for i in range(nbi):
        # 0<= random.random() <=1
        x_random=a+(b-a)*random.random()
        y_random=fmin+(fmax-fmin)*random.random()
        if y_random<=f(x_random):
            pr+=1
    return pr

start = timeit.default_timer()
integrale=Integration_de_MonteCarlo()
totale_integrale=COMM.reduce(integrale,op=MPI.SUM,root=0)
end = timeit.default_timer()

if rank==0:
	integral=(totale_integrale/inter)*Area_rectangle
	print("intargale=",integrale)
	print("time",end-start) 