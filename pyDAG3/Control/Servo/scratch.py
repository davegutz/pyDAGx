# Control scratch
import control as ctrl
import control.matlab as mat
import numpy as np


def servo_loop(gain, tau):
    #      +
    # r----->O------C------G------->y
    #      - ^                 |
    #        |                 |
    #        |-------------H---|
    g = ctrl.series(ctrl.tf(np.array([1]), np.array([1, 0])),    # Integrator
                    ctrl.tf(np.array([1]), np.array([0.1, 1])))  # Actuator lag
    h = ctrl.tf(np.array([1]), np.array([0.01, 1]))              # Sensor lag
    c = ctrl.tf(np.array([tau, 1]), np.array([0.008, 1]))*gain   # Control law
    fbsum = mat.ss([], [], [], [1, -1])
    sys_ol = mat.append(mat.tf2ss(c), mat.tf2ss(g), mat.tf2ss(h))
    sys_cl = mat.append(mat.tf2ss(c), mat.tf2ss(g), mat.tf2ss(h), fbsum)
    q_ol = np.array([[2, 1], [3, 2]])
    q_cl = np.array([[1, 4], [2, 1], [3, 2], [5, 3]])
    sys_ol = mat.connect(sys_ol, q_ol, [1], [3])
    sys_cl = mat.connect(sys_cl, q_cl, [4], [2])
    return mat.margin(sys_ol), sys_ol, sys_cl


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
y = [1, 2]
print('y=', y)
x = sci.zeros(3, 3)
print(x, x.dtype)


"""
sci.push('y', y)

sci.pull('y')
#  array([[ 1.,  2.]])
sci.push(['x', 'y'], ['spam', [1., 2., 3., 4.]])
sci.pull(['x', 'y'])  # doctest: +SKIP
#  [u'spam', array([[ 1.,  2.,  3.,  4.]])]

from scilab2py import scilab


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
