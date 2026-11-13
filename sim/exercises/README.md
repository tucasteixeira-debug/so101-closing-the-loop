# sim/exercises/

My study exercises. They follow university robotics courses as references (Georgia Tech ECE 4560, MIT 6.4210 *Robotic Manipulation*, Lynch & Park's *Modern Robotics*); see the method section in [`PROGRESS.md`](../../PROGRESS.md). Each one is derived by hand in my notebook, then coded and validated against the MuJoCo model.

| Exercise | What it does | Result |
|---|---|---|
| [`lesson_B/ex5_so101_fk3d.py`](lesson_B/ex5_so101_fk3d.py) | Full 3D forward kinematics of the SO-101 (5 joints, base to gripper), built from rotation matrices and one 4×4 transform per joint | Matches MuJoCo on 20 random poses, max error 1.3 × 10⁻¹² mm (position) |
| [`lesson_B/ex6_so101_fk_orientation.py`](lesson_B/ex6_so101_fk_orientation.py) | Extends ex5 with the gripper's orientation, R = R_joints · R₀ | Matches MuJoCo at pan 30° and wrist_roll 90°; zero-pose twist 2.79° |
| [`lesson_B/ex7_jacobian_2link.py`](lesson_B/ex7_jacobian_2link.py) | Jacobian of a planar 2-link arm, derived by hand; compares the linear prediction J·Δθ with the exact forward kinematics | One encoder step on both joints: prediction off by 0.0006 mm |
| [`lesson_C/C3.py`](lesson_C/C3.py) | First grasp on the real follower: all six joints move together at 50 Hz, the gripper takes an object and carries it back; logs commanded vs measured per joint | 900/900 ticks; hold offsets 0.3–1.7° |

Run from the repository root:

```bash
python sim/exercises/lesson_B/ex5_so101_fk3d.py
```

I wrote and designed the code. AI helped me find errors, with some vocabulary and code, and by asking me questions that made me explain each part.
