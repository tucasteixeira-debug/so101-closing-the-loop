"""
Full 3D forward kinematics of the SO-101, now with orientation (Lesson B, exercise 6).

Builds on ex5 (position, validated to 1.3e-12 mm on 20 poses).
New goal: fk also returns the gripper's orientation, a 3x3 matrix whose
columns are the gripper's own x, y, z arrows written in world coordinates.

    R(theta) = T_total[:3, :3] @ R0      (R0 = gripper orientation at the zero pose)
"""

import os

import mujoco
import numpy as np

MODEL_PATH = os.path.expanduser("~/SO-ARM100/Simulation/SO101/scene.xml")
m = mujoco.MjModel.from_xml_path(MODEL_PATH)
d = mujoco.MjData(m)

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]

# Constants read once at the zero pose (same as ex5).
d.qpos[:] = 0
mujoco.mj_forward(m, d)
C = np.array([d.joint(name).xanchor for name in JOINTS])
p0 = d.site("gripperframe").xpos.copy()

# R0, the gripper's orientation at the zero pose.
# MuJoCo gives xmat as 9 numbers in a row (shape (9,)), laid out row by row,
# so fold it back into 3 rows. np.array(...) builds a new array, so this is a copy.
r = d.site("gripperframe").xmat

R0 = np.array([r[0:3],
               r[3:6],
               r[6:9]])


# ---- Unchanged from ex5 --------------------------------------------------------

def R_X(angle, sign):
    a = sign * angle
    return np.array([[1, 0, 0],
                     [0, np.cos(a), -np.sin(a)],
                     [0, np.sin(a),  np.cos(a)]])

def R_Y(angle, sign):
    a = sign * angle
    return np.array([[ np.cos(a), 0, np.sin(a)],
                     [0, 1, 0],
                     [-np.sin(a), 0, np.cos(a)]])

def R_Z(angle, sign):
    a = sign * angle
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a),  np.cos(a), 0],
                     [0, 0, 1]])

def make_T(R, c):
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = c - R @ c
    return T


# ---- Forward kinematics: 5 angles in, (tip position, orientation) out -----------

def fk(angles):
    T_total = np.eye(4)
    for i in range(len(JOINTS)):
        if i == 0:                   # shoulder_pan, rotates about -z
            R = R_Z(angles[i], -1)
        elif i in [1, 2, 3]:         # lift, elbow, wrist_flex, rotate about +y
            R = R_Y(angles[i], 1)
        else:                        # wrist_roll, rotates about -x
            R = R_X(angles[i], -1)
        T_total = T_total @ make_T(R, C[i])
    p = (T_total @ np.append(p0, 1))[:3]

    # Orientation: turn the three zero-pose arrows (columns of R0) with the joints.
    # Only the rotation block matters; the t column (shifts) never touches directions.
    R_grip = T_total[:3, :3] @ R0

    return p, R_grip


# ---- What MuJoCo says, for comparison -------------------------------------------

def mujoco_pose(angles):
    d.qpos[:] = 0
    for name, a in zip(JOINTS, angles):
        d.joint(name).qpos = a
    mujoco.mj_forward(m, d)
    p = d.site("gripperframe").xpos.copy()

    # MuJoCo's orientation as a 3x3. reshape returns a view, so copy.
    R_mj = d.site("gripperframe").xmat.reshape(3, 3).copy()

    return p, R_mj


# ---- R0 is (almost) a pure twist about x ---------------------------------------
# Idea: at zero the gripper points along world x, so x stays (1, 0, 0) and only
# y and z are tipped by an angle alpha in the y-z plane. Read alpha out of R0
# and rebuild R0 with R_X to test that.
# Standard R_x(alpha): column 1 = (0, cos a, sin a) -> R0[1,1] = cos a, R0[2,1] = sin a

alpha = np.arctan2(R0[2, 1], R0[1, 1])        # arctan2 keeps the sign
R0_rebuilt = R_X(alpha, 1)

np.set_printoptions(precision=4, suppress=True)
print("R0 =\n", R0)
print("x arrow at zero:", R0[:, 0])
print(f"twist at zero: {np.degrees(alpha):.2f} deg")
print("max |R_X(alpha) - R0|:", np.abs(R0_rebuilt - R0).max())   # ~1e-16 -> pure twist


# ---- Checks ------------------------------------------------------------------

# Predictions in the notebook first:
#   pan 30:        column 0 = ?
#   wrist_roll 90: which column stays, what happens to the other two (and their signs)?

for label, deg in [("pan 30", [30, 0, 0, 0, 0]),
                   ("wrist_roll 90", [0, 0, 0, 0, 90])]:
    angles = np.radians(deg)
    _, R_mine = fk(angles)
    _, R_mj = mujoco_pose(angles)
    print(f"\n{label}\nmine:\n{R_mine}\nMuJoCo:\n{R_mj}")
    print("still a rotation?  RtR = I:", np.allclose(R_mine.T @ R_mine, np.eye(3)),
          "  det =", round(np.linalg.det(R_mine), 6))

