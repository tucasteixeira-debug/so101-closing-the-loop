"""
Full 3D forward kinematics of the SO-101 (Lesson B, exercise 5).

Goal: write the gripper tip as a function of the 5 joint angles, using only
rotation matrices, and check it against MuJoCo.

Idea: each joint turns everything after it about its own axis.
For one joint: subtract the axis point c, rotate, add c back.
Packed into one 4x4 matrix T, the whole arm is:

    tip = T_pan @ T_lift @ T_elbow @ T_wrist_flex @ T_wrist_roll @ [p0, 1]
"""

import os

import mujoco
import numpy as np

# Official SO-101 model from TheRobotStudio, cloned into the home folder:
# git clone https://github.com/TheRobotStudio/SO-ARM100 ~/SO-ARM100
MODEL_PATH = os.path.expanduser("~/SO-ARM100/Simulation/SO101/scene.xml")
m = mujoco.MjModel.from_xml_path(MODEL_PATH)
d = mujoco.MjData(m)

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]

# Put the arm at zero and let MuJoCo compute positions, then read the constants:
# C  = a point on each joint's axis (5 x 3), p0 = where the tip is at zero.
d.qpos[:] = 0
mujoco.mj_forward(m, d)
C = np.array([d.joint(name).xanchor for name in JOINTS])
p0 = d.site("gripperframe").xpos.copy()      # copy, so it stays the zero-pose tip


# Rotation matrices about x, y and z.
# sign = -1 when the joint's axis points the "wrong" way (pan: -z, wrist_roll: -x).
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


# One joint as a 4x4: R in the top-left block, t = c - R c in the last column.
def make_T(R, c):
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = c - R @ c
    return T


# My forward kinematics: 5 angles in, tip position out.
def fk(angles):
    T_total = np.eye(4)
    for i in range(len(JOINTS)):
        if i == 0:                   # shoulder_pan, rotates about -z
            R = R_Z(angles[i], -1)
        elif i in [1, 2, 3]:         # lift, elbow, wrist_flex, rotate about +y
            R = R_Y(angles[i], 1)
        else:                        # wrist_roll, rotates about -x
            R = R_X(angles[i], -1)
        T_total = T_total @ make_T(R, C[i])    # multiply joint by joint, base first
    return (T_total @ np.append(p0, 1))[:3]    # add the 1, transform, drop the 1


# Comparing with MuJoCo: give it the same angles and read where it puts the tip.
def mujoco_tip(angles):
    d.qpos[:] = 0
    for name, a in zip(JOINTS, angles):      # associate each joint with its angle
        d.joint(name).qpos = a
    mujoco.mj_forward(m, d)                  # MuJoCo computes the positions (no physics)
    return d.site("gripperframe").xpos.copy()


def error_mm(angles):
    return np.linalg.norm(fk(angles) - mujoco_tip(angles)) * 1000


# ---- Checks ------------------------------------------------------------------------

print("Zero pose, my tip:", np.round(fk(np.zeros(5)), 4), " MuJoCo:", np.round(p0, 4))

angles = np.radians([30, 0, 0, 0, 0])
print("Pan at 30 deg, my tip:", np.round(fk(angles), 4), " MuJoCo:", np.round(mujoco_tip(angles), 4))

print("\nOne joint at a time (0.3 rad):")
for i, name in enumerate(JOINTS):
    angles = np.zeros(5)
    angles[i] = 0.3
    print(f"  {name:14s} error = {error_mm(angles):.1e} mm")

print("\n20 random poses inside the joint limits:")
rng = np.random.default_rng(42)
low = [m.joint(name).range[0] for name in JOINTS]
high = [m.joint(name).range[1] for name in JOINTS]
worst = max(error_mm(rng.uniform(low, high)) for _ in range(20))
print(f"  worst error = {worst:.1e} mm ->", "PASS" if worst < 0.1 else "FAIL")
