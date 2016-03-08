import numpy as np
import sympy as sp
from IPython.display import display, Math
# To improve image quality
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png', 'pdf')
# To control stdout
#import sys
#from latex import build_pdf
import time
import subprocess
import os
import tempfile
import shutil
import cython


@cython.boundscheck(False)
@cython.wraparound(False)
def coef(n,J):
    global l
    p = 1
    
    for k in range(l):
        p *= np.math.factorial(J[k])
    
    return np.math.factorial(n)/p    
    

@cython.boundscheck(False)
@cython.wraparound(False)    
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
        
        
@cython.boundscheck(False)
@cython.wraparound(False)        
def findJ(depth=0):
    global J,A,n,l    
    
    if depth>=l:
        if validate(J,n):        
            #print(J)
            A = np.vstack((A,J))            
    else:
        for k in range(n+3):
            J[depth] = k
            findJ(depth+1)
    

@cython.boundscheck(False)
@cython.wraparound(False)    
def printEqLatex(A,breakline=4):
    global l,M,n  
    s = ""
    count = 0
    
    for J in A:
        c = coef(n+2,J)
        if c != 0:
            s += "  +  " + str(int(c))
            for k in range(l):
                m = k-M
                if J[k] != 0:
                    s += "f_{" + str(m) + "}"
                    if J[k] != 1:
                        s += "^" +str(int(J[k]))
            count += 1        
        if count%breakline == 0:
            s += "$\n$"

    s += " = 0"        
    return s
    

@cython.boundscheck(False)
@cython.wraparound(False)    
def printEqMath(A,f):
    global l,M,n
    expr = 0    
    
    for J in A:
        c = coef(n+2,J) 
        tmp = 1          
        for k in range(l):
            tmp *= f[k]**int(J[k])
        expr += int(c)*tmp
        
    return expr    
      
    
@cython.boundscheck(False)
@cython.wraparound(False)
def SimplifyEq(eq,f):
    global M,l
    # F[k]=abs(f[k])
    #F = sp.symbols('F0:25',real=True)
    
    #Change f_{-k} = conj(f_{k})
    for k in range(M):
        eq = eq.subs(f[k],np.conjugate(f[l-1-k]))
    #Shift the index from (0,l) to (-M,M)
    for k in range(M,l):
        eq = eq.subs(f[k],f[k-M])   
    #Substitute f*conj(f)=|f|^2=F^2
    #for k in range(M+1):
        #eq = eq.subs(f[k]*np.conj(f[k]),F[k]**2)
    
    #eq = sp.simplify(eq.expand(complex=True))    
    #eq = sp.powsimp(eq)
    #eq = sp.factor(eq)    
    return eq


@cython.boundscheck(False)
@cython.wraparound(False)
def displayMath(LatexString,filename):   
    global M,n         
    plt.text(0.01, 0.4,'$%s$'% LatexString,{'color': 'b', 'fontsize': 18})
    plt.title(filename)
    #plt.plot(A)      
    plt.savefig(filename+".png")
    #plt.show()


#def saveSolution(filename,tex):
#    pdf = build_pdf(tex)
#    pdf.save_to(filename+".pdf")
    

@cython.boundscheck(False)
@cython.wraparound(False)    
def generate_pdf(filename,tex):    
    current = os.getcwd()
    temp = tempfile.mkdtemp()
    os.chdir(temp)
    
    texfile = filename+".tex"
    tf = open(texfile,'w')
    tf.write(tex)
    tf.close()
    shutil.copy(texfile,current)
    
    proc=subprocess.Popen(['pdflatex',texfile])
    subprocess.Popen(['pdflatex',tex])
    proc.communicate()
    
    #os.rename('cover.pdf',filename)
    shutil.copy(filename+".pdf",current)
    #shutil.rmtree(temp)  
    
    
def generate_report(filename,OriEq,SimEq,SolList,Time):
    global M,n
    text = "M = "+str(M)+", n = "+str(n)+":"
    tex = (r"\documentclass{article}"
                 r"\usepackage{breqn}"
                 r"\begin{document}" + \
                 text + \
                 r"\newline\newline Original equation:"
                 r"\begin{dmath}" + \
                 sp.latex(OriEq.replace('$','')) + \
                 r"\end{dmath}"
                 r"Equivalent equation, where $f_{-j}=\overline{f_j}$:"
                 r"\begin{dmath}" + \
                 sp.latex(SimEq) + r" = 0" + \
                 r"\end{dmath}"
                 r"All possible solutions:")
    for sol in SolList:                
        tex += (r"\begin{dmath}" + \
                 sp.latex(sol) + \
                 r"\end{dmath}")
    tex += (Time + r"\end{document}")
    generate_pdf(filename,tex)
    
################# MAIN PROGRAM ####################

#sp.init_session(quiet=True)
sp.init_printing()

# Index of Fourier coef of f
M = input("Enter an integer for M: ")
M = int(M)
# l=len(J) with index from (-M,M)
l = M*2+1
# Power
n = input("Enter an integer for n: ")
n = int(n)

print("M = "+str(M)+", n = "+str(n)+":")
# Combination in (f)^n
J = np.zeros((l,),dtype=np.int)
# A=a list of J
A = np.empty((0,l),dtype=np.int)
# Change the number of f[k] here, e.g 25 means max(M)=12 and l=25
f = sp.symbols('f0:25',complex=True)

startTime = time.time()

filename = "conjecture M="+str(M)+" n="+str(n)
try:    
    A = np.load(filename + '.npy')
except:    
    findJ()
    np.save(filename,A)
s = printEqLatex(A)  

print("\nOriginal equation:")
#displayMath(s,filename)
display(Math(s.replace('$\n$','')))
print("\nTime elapsed:",time.time()-startTime,"seconds")

eq = printEqMath(A,f)
eq = SimplifyEq(eq,f)
print("\nEquivalent left-hand-side, where f_{-j}=conj(f_j):")
display(eq)
print("\nTime elapsed:",time.time()-startTime,"seconds")

print("\nAll possible solutions:")
SolList = sp.solve(eq,f[1:M+1],manual=1,simplify=0,check=0,numerical=0,dict=1)
for sol in SolList:
    display(sol)
#sp.preview(SolList, output='png')

Time = "\nTime elapsed: " + str(time.time()-startTime) + " seconds"
print(Time)
print("\nGenerating report.")
generate_report(filename,s,eq,SolList,Time)
