# /etc/skel/.bashrc
#
# This file is sourced by all *interactive* bash shells on startup,
# including some apparently interactive shells such as scp and rcp
# that can't tolerate any output.  So make sure this doesn't display
# anything or bad things will happen !


# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]] ; then
	# Shell is non-interactive.  Be done now!
	return
fi


export LD_LIBRARY_PATH=/usr/lib64:$HOME/.virtualenvs/testp3/lib/python3.4:$LD_LIBRARY_PATH 
export PATH=/usr/bin:$HOME/.virtualenvs/testp3/bin:$HOME/.virtualenvs/testp3/include:$PATH


# Put your fun stuff here.
source /usr/bin/virtualenvwrapper.sh


export LAPACK=/usr/lib/libreflapack.so
export BLAS=/usr/lib/libopenblas_openmp.so

