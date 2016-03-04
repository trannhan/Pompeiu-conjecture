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


def coef(n,J):
    global l
    p = np.zeros((l,),dtype=np.int)
    
    for k in range(l):
        p[k] = np.math.factorial(J[k])        

    return np.math.factorial(n)/np.prod(p)


def validate(J,n):
    global l,M
    
    if sum(J)!=n+2:
        return False
        
    summJ = np.zeros((l,),dtype=np.int)
    for k in range(l):        
        summJ[k] = (k - M)*J[k]
        
    if sum(summJ)!=-n:
        return False
        
    return True        
        
                
def findJ(n,depth=0):
    global J,A,l    
    
    if depth>=l:
        if validate(J,n):        
            #print(J)
            A = np.vstack((A,J))            
    else:
        for k in range(n+3):
            J[depth] = k
            findJ(n,depth+1)
    
    
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
      
    
def SimplifyEq(eq,f):
    global M,l
    
    #Change f_{-k} = conj(f_{k})
    for k in range(M):
        eq = eq.subs(f[k],np.conjugate(f[l-1-k]))
    #Shift the index from (0,l) to (-M,M)
    for k in range(M,l):
        eq = eq.subs(f[k],f[k-M])   
    
    #eq = sp.simplify(eq.expand(complex=True))    
    #eq = sp.powsimp(eq)
    #eq = sp.factor(eq)    
    return eq


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

print("\nM = "+str(M)+", n = "+str(n)+":")
# Combination in (f)^n
J = np.zeros((l,),dtype=np.int)
# Change the number of f[k] here, e.g 21 means max(M)=10 and l=21
f = sp.symbols('f0:21',complex=True)

startTime = time.time()

s = ["" for x in range(n)]
eq = [0 for x in range(n)]
for N in range(n):
    filename = "conjecture M="+str(M)+" n="+str(N+1)
    # A = list of J
    A = np.empty((0,l),dtype=np.int)
    try:    
        A = np.load(filename + '.npy')
    except:    
        findJ(N+1)
        np.save(filename,A)
    s[N] = printEqLatex(A)
    eq[N] = printEqMath(A,f)
    eq[N] = SimplifyEq(eq[N],f)

print("\nOriginal equation:")
for N in range(n):
    display(Math(s[N].replace('$\n$','')))
print("\nTime elapsed:",time.time()-startTime,"seconds")

print("\nEquivalent left-hand-side, where f_{-j}=conj(f_j):")
for N in range(n):
    display(eq[N])
print("\nTime elapsed:",time.time()-startTime,"seconds")

print("\nAll possible solutions:")
SolList = sp.solve(eq,f[1:M+1],manual=1,simplify=0,check=0,numerical=0,dict=1)
#F = sp.Matrix(eq)
#RHS = sp.zeros(n,1)
#SolList = F.solve(RHS)
for sol in SolList:
    display(sol)

Time = "\nTime elapsed: " + str(time.time()-startTime) + " seconds"
print(Time)
print("\nGenerating report.")
#generate_report(filename,s,eq,SolList,Time)

