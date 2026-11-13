import numpy as np

L1, L2 = 0.11, 0.12
theta1, theta2 = np.radians([30, 40])

def tip(theta1, theta2):
    x = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    y = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    return np.array([x, y])

ponta = tip(theta1, theta2)

J = np.array([[ L1*np.cos(theta1) + L2*np.cos(theta1+theta2),  L2*np.cos(theta1+theta2)],
              [-L1*np.sin(theta1) - L2*np.sin(theta1+theta2), -L2*np.sin(theta1+theta2)]])

error = np.radians([0.088, 0.088])                        # one encoder step on each joint

predicted = ponta + J @ error                             # Jacobian's guess
true      = tip(theta1 + error[0], theta2 + error[1])     # real FK at the nudged pose

print("predicted:", predicted)
print("true:     ", true)
print("difference (mm):", (predicted - true) * 1000)