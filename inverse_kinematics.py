import numpy as np
from enum import Enum

#INVERSE KINEMATICS OF UR5e 
#RECIPICE BY https://tianyusong.com/wp-content/uploads/2017/12/ur5_inverse_kinematics.pdf
#UTILITY FUNCTIONS FROM MY OWN PREVIOUS CODE AT https://github.com/adamaske/biomedeng/blob/main/Robot_Arm_Project/kin_math.py
class DH_Param():
    def __init__(self, theta, alpha, r, d) -> None:
        self.m_theta = theta
        self.m_alpha = alpha
        self.m_r = r
        self.m_d = d
        
        return
    
def DH_Translation_Matrix(dh_param):
    mat = np.identity(4)
    theta  = np.deg2rad(dh_param.m_theta)
    alpha= np.deg2rad(dh_param.m_alpha)
    r = dh_param.m_r
    d = dh_param.m_d
    
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    
    ct = np.cos(theta)
    st = np.sin(theta)

    mat[0][0] = ct
    mat[0][1] = -st*ca
    mat[0][2] = st * sa
    mat[0][3] = r*ct
    
    mat[1][0] = st
    mat[1][1] = ct*ca
    mat[1][2] = -ct*sa
    mat[1][3] = r*st
    
    mat[2][0] = 0
    mat[2][1] = sa
    mat[2][2] = ca
    mat[2][3] = d
    
    mat[3][0] = 0
    mat[3][1] = 0
    mat[3][2] = 0
    mat[3][3] = 1
	
    return mat
    
class Axis(Enum):
    X = 0
    Y = 1
    Z = 2
    I = 3

def Rotation_Matrix(axis, theta):
    matrix = np.identity(4)
    theta_rad = np.deg2rad(theta)
    ct = np.cos(theta_rad)
    st = np.sin(theta_rad)
    
    if axis == Axis.X:
        matrix[1][1] = ct
        matrix[2][1] = st
        
        matrix[1][2] = -st
        matrix[2][2] = ct
        
    elif axis == Axis.Y:
        matrix[0][0] = ct
        matrix[0][2] = st
        
        matrix[2][0] = -st
        matrix[2][2] = ct
    elif axis == Axis.Z:
        matrix[0][0] = ct
        matrix[1][0] = st
        
        matrix[0][1] = -st
        matrix[1][1] = ct
    elif axis == Axis.I:
        return matrix
    
    return matrix 

def Translation_Matrix(vec):
    
    matrix = np.identity(4)
    matrix[0][3] = vec[0]
    matrix[1][3] = vec[1]
    matrix[2][3] = vec[2]
    
    return matrix

def Get_Translation(transformation):
    return np.array(((transformation[0][3], transformation[1][3], transformation[2][3])))

#Original thetas
t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0.1
t6 = 123      

# a = r in my system
link1 = DH_Param(t1, np.rad2deg(np.pi/2), 0, 0.089159)
link2 = DH_Param(t2, 0, -0.425, 0)
link3 = DH_Param(t3, 0, -0.39225, 0)
link4 = DH_Param(t4, np.rad2deg(np.pi/2), 0, 0.10915)
link5 = DH_Param(t5, np.rad2deg(-np.pi/2), 0, 0.09465)
link6 = DH_Param(t6, 0, 0, 0.0823)

T01 = DH_Translation_Matrix(link1) #Translation matrices
T12 = DH_Translation_Matrix(link2)
T23 = DH_Translation_Matrix(link3)
T34 = DH_Translation_Matrix(link4)
T45 = DH_Translation_Matrix(link5)
T56 = DH_Translation_Matrix(link6)

ts = [T12, T23, T34, T45, T56]
T06 = np.array(T01)
for t in ts:
    T06 = np.matmul(T06, t)

print("T 0_6 : ")
print(T06)


P05 = np.matmul(T06, Translation_Matrix([0, 0, -link6.m_d]))
print("P 0_5 : ")
print(P05)

p05 = Get_Translation(P05)
theta1 = np.arctan2(p05[1], p05[0]) + np.arccos(link4.m_d / (np.sqrt(np.square(p05[0]) + np.square(p05[1])))) + (np.pi /2)

p06 = Get_Translation(T06)
p16_z =  p06[0]*np.sin(theta1) - p06[1]*np.cos(theta1)
theta5 = np.arccos(np.clip((p16_z - link4.m_d) / link6.m_d, a_min=-1, a_max=1))

T61 = np.linalg.inv(np.matmul(np.linalg.inv(T01), T06))
z_y = T61[1][2]
z_x = T61[0][2]
if theta5 == 0 or (z_y == 0 and z_x == 0):
    print("theta6 not defined!")
    theta6 = 0
else:
    theta6 = np.arctan2(-z_y/np.sin(theta5), z_x/np.sin(theta5))

T16 = np.matmul(np.matmul(np.matmul(np.matmul(T12, T23), T34),  T45), T56)
T14 = np.matmul(T16, np.linalg.inv(np.matmul(T45, T56)))
P13 = np.matmul(T14, Translation_Matrix([0, -link4.m_d, 0, 1]))
p13 = Get_Translation(P13)
theta3 = np.arccos(np.clip((np.square(np.linalg.norm(p13)) - np.square(link2.m_r) - np.square(link3.m_r))/ (2*link2.m_r*link3.m_r), a_min=-1, a_max=1))

theta2 =  -np.arctan2(p13[1], -p13[0]) + np.arcsin((link3.m_r*np.sin(theta3)) / np.linalg.norm(p13))

T34 = np.matmul(np.linalg.inv(np.matmul(T12, T23)), T14)

theta4 = np.arctan2(T34[0][1], T34[0][0])

print("theta 1 : ", np.round(np.rad2deg(theta1), 3)) #-7.1 off
print("theta 2 : ", np.round(np.rad2deg(theta2), 3)) # 90 + 0.5xt6
print("theta 3 : ", np.round(np.rad2deg(theta3), 3)) # 90 + 0.5xt6
print("theta 4 : ", np.round(np.rad2deg(theta4), 3)) # 90 + 0.5xt6
print("theta 5 : ", np.round(np.rad2deg(theta5), 3)) # 88.44 off 
print("theta 6 : ", np.round(np.rad2deg(theta6), 3)) # 90 + 0.5xt6
#calculate errors
t1_error = t1 - np.round(np.rad2deg(theta1), 3)
t2_error = t2 - np.round(np.rad2deg(theta2), 3)
t3_error = t3 - np.round(np.rad2deg(theta3), 3)
t4_error = t4 - np.round(np.rad2deg(theta4), 3)
t5_error = t5 - np.round(np.rad2deg(theta5), 3)
t6_error = t6 - np.round(np.rad2deg(theta6), 3)

print("t1_error : ", t1_error)
print("t2_error : ", t2_error)
print("t3_error : ", t3_error)
print("t4_error : ", t4_error)
print("t5_error : ", t5_error)
print("t6_error : ", t6_error)


    