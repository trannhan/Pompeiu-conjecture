import numpy as np
import time


def validate(J,n):
    global l,M
    
    if sum(J)!=n+2:
        return False
        
    summJ = 0
    for k in range(l):        
        summJ += (k - M)*J[k]
        
    if summJ!=-n:
        return False
        
    return True 
    
    
M = 4
l = M*2+1
n = 2
J = np.zeros((l,),dtype=np.int)
A = np.empty((0,l),dtype=np.int)

start_time = time.time()
cont = True
while cont:
    if validate(J,n):        
        #print(J)
        A = np.vstack((A,J)) 
    J[0] += 1
    for k in range(l):
        if J[k]>=n+3:
            if k==l-1:
                cont = False
                break
            J[k] = 0
            J[k+1] += 1
        else:
            break
print("Elapsed time: ", time.time()-start_time)