"""
C3: first grasp on the real follower.

All six joints move together to one pose, the gripper opens, I hand it an
object, it closes, and the arm goes back to rest still holding it.
Every tick I log what I commanded and what the encoders read, so at the end
I get the gap per joint (during the move and while holding).

Before running, I wrote down which joint I expected to lag the most and
which ones would sag while holding (the ones carrying the arm's weight).

Careful: at rest, lift, elbow and wrist_flex sit at the end of their range.
Moving away from the stop is + for lift and wrist_flex, but - for the elbow.
"""
import time

import matplotlib.pyplot as plt
import numpy as np

from lerobot.robots.so_follower.so_follower import SOFollower
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig

# Same joint order everywhere: column j of every array is NAMES[j].
NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]

# How far each joint goes from rest (degrees; the gripper is in %).
#                  pan  lift  elbow  wflex  roll  grip
DELTA = np.array([30, 70, 10, 40, 0, 40])   # grasp pose, gripper open
Beta = np.array([30, 70, 10, 40, 0, 0])     # same pose, gripper closed

DURATION = 4                # s per move
HOLD = 5                    # s to hand it the object
CONTROL_HZ = 50
PERIOD = 1 / CONTROL_HZ     # 0.02 s per tick

config = SOFollowerRobotConfig(
    port="/dev/so101_follower",
    id="follower_01",
    max_relative_target=5.0,    # LeRobot never lets one command jump more than 5 deg
)
robot = SOFollower(config)

# One row of 6 numbers per tick -> arrays of shape (ticks, 6) at the end.
t_log, cmd_log, meas_log = [], [], []
t_start_script = None


def read_pose():
    # the robot gives a dictionary; I want an array in my NAMES order
    obs = robot.get_observation()
    return np.array([obs[f"{n}.pos"] for n in NAMES])


def tick(target):
    # one 0.02 s beat: send, read, write down, wait for the rest of the beat
    t_tick = time.perf_counter()

    action = {f"{n}.pos": float(v) for n, v in zip(NAMES, target)}   # array back to dictionary
    robot.send_action(action)

    measured = read_pose()
    t_log.append(time.perf_counter() - t_start_script)
    cmd_log.append(target.copy())
    meas_log.append(measured)

    time.sleep(max(0.0, PERIOD - (time.perf_counter() - t_tick)))


def move_to(start, goal, duration):
    # same alpha for all joints, so they all start and arrive together
    n = int(duration * CONTROL_HZ)
    for k in range(1, n + 1):
        alpha = k / n
        tick((1 - alpha) * start + alpha * goal)
    return goal     # the next move starts from here (otherwise the gripper re-opened on the way back)


def hold(target, seconds):
    for _ in range(int(seconds * CONTROL_HZ)):
        tick(target)


robot.connect(calibrate=False)
try:
    start = read_pose()
    goal = start + DELTA
    closed = start + Beta
    np.set_printoptions(precision=2, suppress=True)
    print("start: ", start)
    print("goal:  ", goal)
    print("closed:", closed)

    t_start_script = time.perf_counter()
    current = start

    current = move_to(current, goal, DURATION)      # up, gripper opens
    print(f"Place the object in the gripper now ({HOLD:.0f} s)...")
    hold(current, HOLD)
    print("Closing.")
    current = move_to(current, closed, 2)           # gripper closes
    hold(current, 2)
    current = move_to(current, start, DURATION)     # back to rest, still holding
    hold(current, 1.0)
finally:
    robot.disconnect()

# ---- numbers ----
t_a = np.array(t_log)
cmd_a = np.array(cmd_log)       # row = tick, column = joint
meas_a = np.array(meas_log)
gap = meas_a - cmd_a

move_up = t_a <= DURATION
hold_early = (t_a > DURATION) & (t_a <= DURATION + 1.0)
hold_late = (t_a > DURATION + HOLD - 5.0) & (t_a <= DURATION + HOLD)

# axis=0 goes down the time axis -> one number per joint
max_gap_move = np.abs(gap[move_up]).max(axis=0)
offset_early = gap[hold_early].mean(axis=0)
offset_late = gap[hold_late].mean(axis=0)

print(f"\nticks recorded: {len(t_a)}   (expected {int((2 * DURATION + HOLD + 2 + 2 + 1.0) * CONTROL_HZ)})")
print(f"{'joint':<15}{'max gap move':>14}{'hold 1st s':>12}{'hold last 5s':>14}   [deg]")
for j, n in enumerate(NAMES):
    print(f"{n:<15}{max_gap_move[j]:>14.3f}{offset_early[j]:>+12.3f}{offset_late[j]:>+14.3f}")
print(f"one encoder count = {360 / 4096:.3f} deg  (gripper column is in %, not deg)")

# ---- plot: one graph per joint ----
fig, axes = plt.subplots(6, 1, sharex=True, figsize=(8, 11))
for j, n in enumerate(NAMES):
    axes[j].plot(t_a, cmd_a[:, j], "--", label="commanded")
    axes[j].plot(t_a, meas_a[:, j], label="measured")
    axes[j].set_ylabel(n, fontsize=8)
    axes[j].grid(True)
axes[0].legend(fontsize=8)
axes[0].set_title(f"Real arm: all joints, {DURATION} s moves, hold {HOLD} s")
axes[-1].set_xlabel("time [s]")
plt.tight_layout()
plt.savefig("c3_pose_move.png", dpi=120)
plt.show()
