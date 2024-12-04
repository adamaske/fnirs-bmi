import numpy as np
t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0
t6 = 0              
#                           a           alpha       d           theta
dh_params = np.array(((        0,   np.pi / 2,    0.089159,      t1),
                      (   -0.425,           0,           0,      t2),
                      (-0.039225,           0,           0,      t3),
                      (        0,   np.pi / 2,     0.10915,      t4),
                      (        0,    -np.pi/2,     0.09465,      t5),
                      (        0,            0,     0.0823,      t6),))
a1, a2, a3, a4, a5, a6 = 0, -0.425, -0.039225, 0, 0, 0
al1, al2, al3, al5, al5, al6 = np.pi / 2, 0, 0, np.pi/2, -np.pi/2, 0
d1, d2, d3, d4, d5, d6 = 0.089159, 0, 0, 0.10915, 0.09465, 0.0823

def ik(position, orientation):
    desired = np.array(position)

    
    thetas = []
    return thetas
    
    