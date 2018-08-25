# Generic servo loop analysis functions
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
