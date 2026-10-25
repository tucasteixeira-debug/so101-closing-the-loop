# Progress Log

A dated record of my project, newest first. Each entry covers one session or a span of sessions and lists, in plain terms:

- **Achieved**: concrete, verifiable outcomes, quantified where possible.
- **Formation**: the questions I worked through, across the full stack the project rests on. That includes computing and operating systems, communication, electronics, mechanics, kinematics, control, measurement and statistics, perception, and machine learning.
- **Not achieved / open**: what didn't work, what is blocked, and what remains.

I started from zero in most of these areas. The Formation lists record what I studied; they are not a claim of mastery. I draft entries from my private working notes with an AI-assisted workflow and review each one by hand before committing it.

## How I learn: method and references

To develop academic-level thinking for this robot, I consult university robotics courses and use them as references for my exercises and study: Georgia Tech ECE 4560 (Maegan Tucker, a course built on the SO-101), MIT 6.4210 *Robotic Manipulation* (Russ Tedrake) and *Modern Robotics* (Kevin Lynch & Frank Park). I don't use them to copy a course. They give me guidance and set the level, so that I build an academic formation and can then solve problems and make a contribution on my own.

In practice I work every step by hand first: derivations and sketches in my notebook, closed-book recall of the previous lesson, and an explanation of each step in my own words. Only then do I code it and check it against the simulator or the real arm, with real numbers. An AI tutor asks me questions, makes me explain my reasoning and checks my numbers. Each entry lists the sources it used under **Method and references**, and my published exercises are in [`sim/exercises/`](sim/exercises/).

## Entries

> **2026-10-25:** project reframed from *error anatomy* to *closing the loop*: same measurements, now followed by a vision-based correction with before/after numbers. Earlier entries keep their original wording.

| Dates | Entry |
|---|---|
| [2026-10-20 to 2026-10-24](#2026-10-20-to-2026-10-24--full-3d-forward-kinematics-of-the-so-101-validated-against-mujoco) | Full 3D forward kinematics of the SO-101, validated against MuJoCo |
| [2026-10-14 to 2026-10-20](#2026-10-14-to-2026-10-20--assembly-calibration-and-first-teleoperation-of-the-so-101-pair) | Assembly, calibration and first teleoperation of the SO-101 pair |
| [2026-10-12 to 2026-10-13](#2026-10-12-to-2026-10-13--forward-kinematics-of-the-so-101) | Forward kinematics of the SO-101 |
| [2026-10-06 to 2026-10-07](#2026-10-06-to-2026-10-07--first-simulations-single-joint-dynamics-and-a-6-joint-pose-sequence) | First simulations: single-joint dynamics and a 6-joint pose sequence |
| [2026-09-25 to 2026-09-26](#2026-09-25-to-2026-09-26--leader-arm-configuration-and-preparation-of-the-simulation-track) | Leader-arm configuration and preparation of the simulation track |
| [2026-09-23 to 2026-09-25](#2026-09-23-to-2026-09-25--public-repository-version-control-and-documentation-workflow) | Public repository, version control and documentation workflow |
| [2026-09-19 to 2026-09-23](#2026-09-19-to-2026-09-23--hardware-bring-up-servo-configuration-and-the-communication-layer) | Hardware bring-up: servo configuration and the communication layer |
| [2026-09-12](#2026-09-12--project-planning-and-development-environment-setup) | Project planning and development environment setup |

---

### 2026-10-20 to 2026-10-24 · Full 3D forward kinematics of the SO-101, validated against MuJoCo

**Method and references**
- My exercises and study follow reference robotics courses. They give me guidance and set the academic level of thinking I aim for on this robot: K. Lynch & F. Park, *Modern Robotics* (2017), §4.1.1 (product of exponentials); Georgia Tech ECE 4560 (Fall 2025), lectures 2–4 (rotations and transforms); R. Tedrake, *Robotic Manipulation* (MIT), Ch. 3.
- I work every step by hand first: derivations and sketches in my notebook, closed-book recall of the previous lesson, and an explanation of each step in my own words. Only then do I code it. An AI tutor asks me questions, makes me explain my reasoning and checks my numbers.
- Each result is then checked against the official SO-101 model in MuJoCo, using real numbers.

**Achieved**

> [!IMPORTANT]
> **Milestones**
> - **First full 3D forward kinematics of the SO-101 (5 joints, base to gripper), validated against MuJoCo**: maximum position error 1.3 × 10⁻¹² mm over 20 random poses within the joint limits, i.e. floating-point level (position only; orientation not yet compared).

- Code: [`ex5_so101_fk3d.py`](sim/exercises/lesson_B/ex5_so101_fk3d.py). I wrote it, thought it through and designed its structure: rotation functions with a sign per joint, one 4×4 transform per joint, a running product from the base outward, and a comparison with MuJoCo. AI helped me find errors and helped with some vocabulary and code, and it asked me questions that made me explain each part. I tested it in increasing difficulty: zero pose, pan only, one joint at a time, then 20 random poses.
- I diagnosed and fixed a teleoperation fault: after re-plugging, the follower went limp while the leader moved by itself. Linux numbers serial ports in plug order, so the two boards had swapped names and the leader was receiving the motion commands. I isolated the cause by connecting one board at a time.

**Formation — questions worked through**
- Where do the rotation matrices come from? Write a point as (x, y) = |r|(cos φ₀, sin φ₀) and rotate it by α. Expanding cos(φ₀ + α) and sin(φ₀ + α) with the addition formulas gives x′ = x cos α − y sin α, y′ = x sin α + y cos α, which is R_z. Each column shows where an axis lands (at 90°, R_z sends x → y). The cyclic order x → y → z → x then gives R_x and R_y, with R_y's minus sign in the bottom-left. The columns are orthonormal (Rᵀ R = I, det = +1), so lengths are preserved.
- How does a joint's axis direction fix the sign of its angle? A rotation by θ about −axis equals a rotation by −θ about +axis. From the model's axis vectors: pan (0, 0, −1) → R_z(−θ), lift/elbow/wrist_flex (0, 1, 0) → R_y(+θ), wrist_roll (−1, 0, 0) → R_x(−θ), each checked in MuJoCo. A wrong sign mirrors the arm: the tip lands at y = +0.1763 m instead of −0.1763 m at pan 30°, 35 cm apart.
- Why does a joint need a 4×4 transform rather than a 3×3 matrix? R turns vectors about the origin only, so a point is turned about an axis through c as p′ = c + R(p − c). For the elbow axis point at pan 30° this gives (0.0802, −0.0450) m, matching MuJoCo, while R·p alone lands 2 cm off. Rewritten, p′ = R p + t with t = c − R c, and a constant shift cannot come from a matrix product (R·0 = 0). Appending a 1 to the point puts t in a fourth column: T = [R t; 0 1].
- How does the tip follow from the rotation of every joint about its own axis? tip(θ) = T_pan(θ₁) T_lift(θ₂) T_elbow(θ₃) T_wflex(θ₄) T_roll(θ₅) [p₀; 1], where p₀ is the tip at the zero pose. The matrices act right to left, so the joint nearest the tip turns first while every joint nearer the base is still at zero. Each axis point c therefore keeps its zero-pose value, read once from the model, and moving the arm means calling the same function with new angles. The product turns each joint's shift by the joints nearer the base (combined shift R_pan t_lift + t_pan). Multiplied in the reverse order, the elbow point at pan 30° + lift 30° is 29 mm off. Formal name: product of exponentials, space form.

**Not achieved / open**
- The orientation half of the validation is not done: I have not yet compared the gripper's rotation with MuJoCo's.
- The serial ports still have no stable per-device names, which is what allowed the teleoperation fault.

---

### 2026-10-14 to 2026-10-20 · Assembly, calibration and first teleoperation of the SO-101 pair

**Achieved**

> [!IMPORTANT]
> **Milestones**
> - **First teleoperation of my SO-101 pair**: the follower copies the hand-guided leader on all 6 joints at 59.1 Hz (target 60 Hz), 0 of 4769 control ticks over budget.
> - **I assembled and calibrated both arms**, 6/6 joints each.

- I found the same bus fault on both arms: servos beyond ID 2 did not answer, which placed the break in the servo 2 → 3 cable. I re-soldered a broken connector pin.

<p align="center">
  <img src="docs/media/so101_first_teleop.gif" width="260" alt="Follower arm copying the motion of the hand-guided leader arm">
  <br>
  <em><b>Figure 1.</b> First teleoperation on hardware: the follower copies the hand-guided leader joint by joint, 60 Hz loop, 5° per-tick safety cap. Phone video, 11.4 s.</em>
</p>

<p align="center">
  <img src="docs/media/so101_pair_assembled_front.jpg" width="360" alt="Assembled SO-101 leader and follower arms clamped to a desk edge">
  <br>
  <em><b>Figure 2.</b> Assembled leader (front) and follower, clamped about 10 cm apart in the same orientation.</em>
</p>

**Formation — questions worked through**
- Why must a joint's travel never cross the encoder's 4095 → 0 wrap, and how does calibration prevent it? The servo computes error = goal − present on a straight number line, so a 1.4° move from 4090 to 10 reads as −4080 counts ≈ −358°. Calibration sets a homing offset, reported = (raw − offset) mod 4096, with offset = raw − 2047 at the pose the arm is held in, so that pose sits opposite the wrap (raw 4038 → offset 1991). The margin left on each side is (4096 − travel)/2: 855 counts ≈ ±75° for shoulder_lift.
- How do two arms with different raw counts agree on "the same position"? Each arm's calibration maps counts to degrees, with 0° = (min + max)/2 of the recorded travel and degrees = (count − mid) · 360/4095; degrees are what is sent. Example: leader 1490 → −45.3° → follower 1442.
- Why does a position servo trail a moving target? Its torque is proportional to the position error, so following at speed ω needs an error that grows with ω. Measured on one fast wrist move (preliminary): 5–6° behind at ≈ 50°/s, a lag of ≈ 0.11 s, of which communication is ≲ 20 ms.
- Does a learned imitation policy need inverse kinematics? No: the human solves it by moving the leader. A scripted inverse-kinematics grasp does, and its spread contains only mechanical and control error, so comparing it with the policy isolates the policy's share.

**Not achieved / open**
- I have no commanded-vs-measured data on the real follower yet.
- The re-soldered pins sit on the most-moved shoulder cable of both arms, a reliability risk.

---

### 2026-10-12 to 2026-10-13 · Forward kinematics of the SO-101

**Achieved**

> [!IMPORTANT]
> **Milestones**
> - **My first forward-kinematics model of the real SO-101**: the planar chain shoulder_lift → elbow_flex → wrist_flex predicts the gripper position of the MuJoCo model on 10 random poses with a max error of 3 × 10⁻¹³ mm.

- Method: I read the joint positions and axes from the MuJoCo model to get the arm's real geometry: link lengths 0.1160 / 0.1350 / 0.1594 m and the angle of each link at zero encoder reading (+76.03°, −73.82°, −5.05°). I derived the model by hand; the comparison script was written by AI.
- I wrote n-joint forward kinematics in NumPy: a cumulative sum turns relative joint angles into link directions, then one matrix product [cos φ; sin φ] (2 × n) · L (n) gives the tip (x, y). I checked it on two hand-solved poses, both (0.10, 0.10) m.

**Formation — questions worked through**
- How does the tip position follow from the joint angles? Each encoder measures its link relative to the previous one, so link k points along the running sum of angles: x = Σ Lₖ cos(θ₁ + … + θₖ), y = Σ Lₖ sin(θ₁ + … + θₖ).
- Why can one target have two joint solutions? The elbow lies on a circle of radius L₁ around the base and of radius L₂ around the target; two circles meet in 2, 1 or 0 points (elbow-up, elbow-down, or unreachable).
- Why is full stretch the worst place for a task? For two equal links, |tip|² = 2L² + 2L² cos φ₂ = 4L² cos²(φ₂/2), so r = 2L cos(φ₂/2) and dr/dφ₂ = −L sin(φ₂/2). With L = 0.10 m: 1.23 mm of radial motion per elbow degree at 90° bend, 0.03 mm at 2°. Near the stretched pose (a singularity) the tip barely responds to the joints.
- Why does kinematics follow the line between joint axes, not the shape of the part? On the SO-101 the elbow axis sits 2.8 cm to the side of the upper arm, which tilts the effective link by 14°; ignoring it misplaces the elbow by about 2.8 cm.

**Not achieved / open**
- I had not started full 3D kinematics (adding shoulder_pan and wrist_roll).

---

### 2026-10-06 to 2026-10-07 · First simulations: single-joint dynamics and a 6-joint pose sequence

**Achieved**

> [!IMPORTANT]
> **Milestones**
> - **My first simulation commanding all 6 SO-101 joints together**, recorded and plotted per joint (commanded vs. actual).
> - **First choreographed motion:** 7 poses (ready, reach, grasp, lift with wrist roll, reach, release, home), no floor contact, largest arm-joint tracking gap 0.013 rad.

- My first hand-written simulation model: a one-joint pendulum stepped from Python (simulated swing period ≈ 1.2 s).
- I inspected the SO-101 model from Python: 8 bodies, 6 joints, 6 position actuators, 31 geometry elements.
- Simulated 0.5 rad step on one joint: overshoot to 0.627 rad, settled by ≈ 0.43 s, 0.0007 rad residual offset.
- Tracking error vs. move duration (0.5 rad move): largest gap 0.0047, 0.023, 0.33 rad at 2.0, 0.5, 0.1 s.
- These are simulation results only. The motor parameters are borrowed from another robot model, so the control error has to come from the real arm.

<p align="center">
  <img src="docs/media/ex4_pose_sequence.gif" width="480" alt="Simulation of the public SO-101 model moving all 6 joints through a 7-pose sequence">
  <br>
  <em><b>Figure 1.</b> Simulated 7-pose sequence on the public SO-101 MuJoCo model: ready → reach right (gripper opens) → grasp → lift with wrist roll → reach left → release → home. Linear interpolation of joint targets at 50 Hz.</em>
</p>

<p align="center">
  <img src="docs/media/ex4_pose_sequence.png" width="720" alt="Commanded vs. actual angle for each of the 6 joints during the simulated pose sequence">
  <br>
  <em><b>Figure 2.</b> Commanded (dashed) vs. actual (solid) angle of each joint during the sequence in Figure 1. The two curves overlap: largest gap 0.013 rad on the arm joints, 0.04 rad on the gripper during its fast moves.</em>
</p>

**Formation — questions worked through**
- How is a robot described for a physics engine? (MJCF nested bodies, joints, geometry; visual vs. collision shapes; units)
- How is a simulation driven from Python? (compiled model vs. state, time stepping, actuator targets, live viewer)
- How are revolute-joint sign conventions defined unambiguously? (joint axis, right-hand rule, parallel axes forming a planar sub-chain)
- Which physical effects make up a simulated servo joint, and what does each contribute? (gravity load, link inertia, reflected rotor inertia J·N², feedback "spring", damping, torque limit)
- Why does a position-controlled joint overshoot when its torque saturates? (proportional feedback, bang-bang behaviour, momentum carrying past the target)
- How does interpolating joint targets trade motion speed against tracking error? (linear interpolation, 50 Hz targets on 500 Hz physics)
- Why should interpolation track progress through the move rather than add a constant increment? (α as fraction completed 0→1, accumulated rounding, real-clock timing)
- How is a multi-joint simulation recorded and analysed in Python? (per-step arrays stacked into a time × joint table, view vs. copy, column slicing, stacked plots)
- How are simulation frames rendered offscreen and compressed for documentation? (fixed camera, GIF export, cropping, frame skipping, palette reduction)

**Not achieved / open**
- No hardware progress: I had not assembled the follower, and the leader IDs were still unverified.
- I had not started forward kinematics.

---

### 2026-09-25 to 2026-09-26 · Leader-arm configuration and preparation of the simulation track

**Method and references**
- Backbone: Georgia Tech ECE 4560 (Maegan Tucker), a course built on the SO-101. I use it as a reference, not step by step.
- Where I deliberately differ: simulation first, forward kinematics and sensitivity before inverse kinematics, and a prediction vs. measurement in every exercise.
- Supplements: MIT 6.4210 *Robotic Manipulation*, Chapter 3; Northwestern *Modern Robotics* (Lynch & Park).
- Simulation model: TheRobotStudio's public SO-101 MuJoCo model (SO-ARM100 repository).
- Learning-design evidence: de Jong, Linn & Zacharia (2013), *Science*, on combining physical and virtual laboratories.

**Achieved**
- Leader arm: I matched 6/6 servos to their joints by gear ratio and checked them against the official bill of materials.
- I assigned leader IDs 1–6 with the single working board; not yet confirmed by a bus scan.
- I corrected my earlier "leader blocked" status: ID assignment needs one board; two are needed only for teleoperation.
- I loaded the public SO-101 simulation model in MuJoCo 3.14 in a test environment; joint names and order match LeRobot.
- I computed the tip shift per encoder step (0.088°) from the model: 0.25–0.54 mm, depending on joint and pose.
- I found that the stock gripper collision shapes cannot hold a cube in simulation.

**Formation — questions worked through**
- On a shared servo bus, which operations need one adapter, and which need two at once? (daisy-chain addressing, ID assignment vs. teleoperation)
- How do supply voltage and gear reduction set a servo's torque and backdrivability? (three leader gear ratios, 5 V supply on 7.4 V-rated motors)
- How does joint encoder resolution translate into end-effector position error, and why does it depend on pose? (arc length, Jacobian)
- Why are forward kinematics and the Jacobian a prerequisite for an error budget, ahead of inverse kinematics?
- How should simulation, programming, kinematics and physical assembly be sequenced? (combining physical and virtual laboratories)
- How can control logic be shared between a simulated and a physical arm? (adapter layer, radians vs. degrees, simulated vs. real time)
- What happens when a command line runs a Python module? (shell search path, interpreter flags, argument passing, conda environments)
- Through which software layers does one servo command travel? (Python packet builder, serial library, kernel driver, board and servo firmware)

**Not achieved / open**
- Leader IDs not verified; I still needed a second driver board to run both arms together.
- I had not started physical assembly; I deferred it deliberately to avoid reassembly and recalibration.

---

### 2026-09-23 to 2026-09-25 · Public repository, version control and documentation workflow

**Achieved**
- I created the public repository with a documented structure: overview, progress log, and a README per folder.
- I excluded my private working notes and tool configuration from version control, and verified the exclusion before publishing.
- I wrote the public objectives document, including a researched overview of the current physical-AI landscape.
- I installed and configured an AI coding agent with project instructions and an approval-gated routine for this log.

**Formation — questions worked through**
- How does a Unix shell locate executables, and when do startup-file changes take effect? (search path, symbolic links, per-shell startup files)
- How does version control model a project's history? (working directory, staging area, commits)
- What distinguishes a local repository from a hosted remote?
- Why does untracking a file not remove it from history, and what can ignore rules not do?
- How are public engineering repositories conventionally structured? (reference layouts, per-folder documentation, changelog conventions)
- How does an AI coding agent act on a filesystem, and how is its authority bounded? (permission gating, standing instructions, skills)

**Not achieved / open**
- An early version of the repository included my private notes in its history; I rebuilt the repository with a clean history.
- The routine for drafting this log needed several redesigns before the first entry.
- No hardware progress: the leader arm was still blocked and assembly had not started.
- I have not yet chosen a license for the repository.

---

### 2026-09-19 to 2026-09-23 · Hardware bring-up: servo configuration and the communication layer

**Achieved**
- Follower arm: I assigned unique bus IDs to 6/6 servos, configuring one servo at a time.
- I isolated a defective driver board by substitution: 1 of 2 boards powered and enumerated but relayed no data.
- I filed a warranty claim for the defective board and identified a low-cost backup adapter.
- I configured serial-port access persistently through group membership.

**Formation — questions worked through**
- How is a robotic manipulator decomposed into functional layers, and how do these map onto the error budget?
- How do joint angles determine end-effector position? (forward kinematics, at the intuition level)
- How is information physically transmitted between a computer and a peripheral? (UART bit timing, baud rate, USB differential signalling)
- How does a motor command become bytes on a shared servo bus? (packet structure, device IDs, registers, checksum)
- How does the Linux kernel expose a hardware device to user programs? (character devices, major/minor numbers, udev)
- How does a Unix shell resolve variables, programs and access rights? (environment variables, search path, permissions, groups)

**Not achieved / open**
- The leader arm was not configured; it was blocked on a second working driver board.
- A diagnostic script I wrote briefly mimicked a hardware fault; the cause was a silently caught software error.
- I had not started physical assembly and calibration.

---

### 2026-09-12 · Project planning and development environment setup

**Achieved**
- I estimated a semester time budget against my course load; single-semester completion is a stretch goal.
- I set my working method: concepts built one at a time from physical intuition, alongside hands-on work.
- I revised the camera setup to two cameras (wrist-mounted and overview) and sourced the hardware kit.
- I installed Ubuntu 24.04 LTS as dual-boot, with NVIDIA GPU drivers for later policy training.
- I installed LeRobot with Feetech servo support in a dedicated Python 3.12 environment and verified the import.
- I installed my development tooling: version control, code editor, Python package manager.

**Formation — questions worked through**
- Where does the boundary between hardware and software lie? (transistors as switches, bits, memory from feedback latches)
- How does a processor execute a stored program? (instruction sets, assembly, fetch–execute cycle)
- What is an operating system kernel, and what role do device drivers play?
- How do programs communicate with peripherals? (device protocols such as Modbus, memory-mapped I/O)
- Why is Linux the prevailing platform for robotics development? (ecosystem, real-time kernel extensions, file-based device access)
- How are Python dependencies isolated per project? (conda environments, interpreter version requirements)

**Not achieved / open**
- My first LeRobot install failed: third-party guides specify Python 3.10, while current LeRobot requires 3.12 or newer.
- I had not yet evaluated the measurement method (camera fiducials vs. mechanical fixture).
- I had not yet fixed the task geometry or the choice of policy.
