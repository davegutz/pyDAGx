# Control scratch
import control as ctrl
import control.matlab as mat
import numpy as np
import matplotlib.pyplot as plt

#      +
# ------>O------C------G------->y
#      - ^                 |
#        |                 |
#        |-------------H---|


G = ctrl.tf(np.array([1]), np.array([1, 0]))
H = ctrl.tf(np.array([1]), np.array([0.01, 1]))
gain = 10
C = ctrl.tf(np.array([0.1, 1]), np.array([0.008, 1]))*gain
fbsum = mat.ss([], [], [], [1, -1])
sys_ol = mat.append(mat.tf2ss(C), mat.tf2ss(G), mat.tf2ss(H))
sys_cl = mat.append(mat.tf2ss(C), mat.tf2ss(G), mat.tf2ss(H), fbsum)
Q_OL = np.array([[2, 1], [3, 2]])
Q_CL = np.array([[1, 4], [2, 1], [3, 2], [5, 3]])
SYSC_OL = mat.connect(sys_ol, Q_OL, [1], [3])
SYSC_CL = mat.connect(sys_cl, Q_CL, [4], [2])
gm, pm, wg, wp = mat.margin(SYSC_OL)
print('gm=', gm, 'wg=', wg, 'pm=', pm, 'wp=', wp)

plotting = False
if plotting:
    y, t = mat.step(SYSC_CL)
    plt.figure(1)
    plt.plot(t, y)
    plt.grid()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.show()

    plt.figure(2)
    mat.bode(SYSC_OL, dB=True)
