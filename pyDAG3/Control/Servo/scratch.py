# Control scratch.  This only works with scilab 5 not 6
from pyDAG3.Control.Servo.servo_loop import *


"""Edit to whichever ../scilab2py/__init__.py is being called and flagged for missing dll
 # lib1 = ctypes.CDLL(os.path.join(basepath, 'core', 'libmmd.dll'))
    # lib2 = ctypes.CDLL(os.path.join(basepath, 'core', 'libifcoremd.dll'))
    #
    # def handler(sig, hook=thread.interrupt_main):
    #     hook()
    #     return 1
    #
    # routine = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)(handler)
    # ctypes.windll.kernel32.SetConsoleCtrlHandler(routine, 1)
    try:
        lib1 = ctypes.CDLL(os.path.join(basepath, 'core', 'libmmd.dll'))
        lib2 = ctypes.CDLL(os.path.join(basepath, 'core', 'libifcoremd.dll'))

        def handler(sig, hook=thread.interrupt_main):
            hook()
            return 1
        routine = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)(handler)
        ctypes.windll.kernel32.SetConsoleCtrlHandler(routine, 1)
"""


from scilab2py import Scilab2Py
sci = Scilab2Py()

# ZDT1 multi-objective function
def_zdt1 = "function f=zdt1(x)\n\
f1 = x(1);\n\
g = 1 + 9 * sum(x(2:$)) / (length(x)-1);\n\
h = 1 - sqrt(f1 ./ g);\n\
f = [f1, g.*h];\n\
endfunction"

import math


def zdt1(x):
    f1 = np.array(x[0])
    g = np.array(1 + 9 * sum(x[1:]))
    h = 1 - math.sqrt(f1 / g)
    return f1, g*h


sci.eval(def_zdt1)
# sci.zdt1 = zdt1

print('python direct =', sci.zdt1([4, 1]))
sci.eval("zdt1([4, 1])")

sci.eval("pyAddToPath('./')")
sci.eval("pyImport pyDAG3.Control.Servo.servo_loop;")



"""
# Min boundary function
def_min_bd_zdt1 = "function Res=min_bd_zdt1(n)\n\
Res = zeros(n,1);\n\
endfunction"
sci.eval(def_min_bd_zdt1)


# Max boundary function
def_max_bd_zdt1 = "function Res=max_bd_zdt1(n)\n\
Res = ones(n,1)\n\
endfunction"
sci.eval(def_max_bd_zdt1)


# Set NSGA-II parameters
def_par = "// Problem dimension\n\
dim = 2;\n\
# Example of use of the genetic algorithm\n\
funcname = 'zdt1';\n\
PopSize = 500;\n\
Proba_cross = 0.7;\n\
Proba_mut = 0.1;\n\
NbGen = 10;\n\
NbCouples = 110;\n\
Log = %T;\n\
pressure = 0.1;"
sci.eval(def_par)


# Parameters to adapt to the shape of the optimization problem
sci.eval("ga_params = init_param();")
sci.eval("ga_params = add_param(ga_params, 'minbound', min_bd_zdt1(dim));")
sci.eval("ga_params = add_param(ga_params, 'maxbound', max_bd_zdt1(dim));")
sci.eval("ga_params = add_param(ga_params, 'dimension', dim);")
sci.eval("ga_params = add_param(ga_params, 'beta', 0);")
sci.eval("ga_params = add_param(ga_params, 'delta', 0);")
# Parameters to fine tune the Genetic algorithm.
# All these parameters are optional for continuous optimization.
# If you need to adapt the GA to a special problem.
sci.eval("ga_params = add_param(ga_params, 'init_func', init_ga_default);")
sci.eval("ga_params = add_param(ga_params, 'crossover_func', crossover_ga_default);")
sci.eval("ga_params = add_param(ga_params, 'mutation_func', mutation_ga_default);")
sci.eval("ga_params = add_param(ga_params, 'codage_func', coding_ga_identity);")
sci.eval("ga_params = add_param(ga_params,'nb_couples',NbCouples);")
sci.eval("ga_params = add_param(ga_params,'pressure',pressure);")
# Define s function shortcut
sci.eval("deff('y=fobjs(x)','y = zdt1(x);');")


cmd_nsga2 = "[pop_opt, fobj_pop_opt, pop_init, fobj_pop_init] = \
             optim_nsga2(fobjs, PopSize, NbGen, Proba_mut, Proba_cross, Log, ga_params);"
sci.eval(cmd_nsga2)

# Compute Pareto front and filter
sci.eval("[f_pareto,pop_pareto] = pareto_filter(fobj_pop_opt,pop_opt);")
# Optimal front function definition
sci.eval("f1_opt = linspace(0,1);")
sci.eval("f2_opt = 1 - sqrt(f1_opt);")
# Plot solution: Pareto front
sci.eval("scf(1);")
# Plotting final population
sci.eval("plot(fobj_pop_opt(:,1),fobj_pop_opt(:,2),'g.');")
# Plotting Pareto population
sci.eval("plot(f_pareto(:,1),f_pareto(:,2),'k.');")
sci.eval("plot(f1_opt, f2_opt, 'k-');")
sci.eval('title("Pareto front","fontsize",3);')
sci.eval('xlabel("$f_1$","fontsize",4);')
sci.eval('ylabel("$f_2$","fontsize",4);')
sci.eval("legend(['Final pop.','Pareto pop.','Pareto front.']);")
# Transform list to vector for plotting Pareto set
sci.eval("npop = length(pop_opt);")
sci.eval("pop_opt = matrix(list2vec(pop_opt),dim,npop)';")
sci.eval("nfpop = length(pop_pareto);")
sci.eval("pop_pareto = matrix(list2vec(pop_pareto),dim,nfpop)';")
# Plot the Pareto set
sci.eval("scf(2);")
# Plotting final population
sci.eval("plot(pop_opt(:,1),pop_opt(:,2),'g.');")
# Plotting Pareto population
sci.eval("plot(pop_pareto(:,1),pop_pareto(:,2),'k.');")
sci.eval('title("Pareto Set","fontsize",3);')
sci.eval('xlabel("$x_1$","fontsize",4);')
sci.eval('ylabel("$x_2$","fontsize",4);')
sci.eval("legend(['Final pop.','Pareto pop.']);")
"""

"""
TAU = 0.1
GAIN = 10
[gm, pm, wp, wg], SYSC_OL, SYSC_CL = servo_loop(GAIN, TAU)
print('gm=', gm, 'wg=', wg, 'pm=', pm, 'wp=', wp)



plotting = False
if plotting:
    import matplotlib.pyplot as plt
    y, t = mat.step(SYSC_CL)
    plt.figure(1)
    plt.plot(t, y)
    plt.grid()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.show()
    plt.figure(2)
    mat.bode(SYSC_OL, dB=True)

"""
