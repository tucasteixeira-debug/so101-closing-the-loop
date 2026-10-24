# SO-101: Error Anatomy

Where does a learned robot policy's placement error actually come from?

I'm building an **error budget** for the SO-101, a low-cost open-source 6-DOF arm (Feetech STS3215 servos, Hugging Face LeRobot). On a precision placement task, I split its imprecision into three contributions:
- **mechanical**: backlash and compliance in the joints;
- **control**: how the servos are tuned;
- **policy**: the learned imitation policy (ACT) itself.

Every result is measured with ground truth independent of the arm's own sensors, using ISO 9283-style repeatability statistics. Once I know the dominant source, I apply one targeted intervention and quantify the improvement.

> **Status (2026-10-24):** both arms are assembled, calibrated and teleoperating. Full 3D forward kinematics is validated against the MuJoCo model. Next: the Jacobian, which maps joint errors to tip errors, and the independent measurement rig. No error-budget measurements yet.

## Why I'm doing this

I'm a Robotics & Mechatronics master's student, and this project is how I train myself:
- **Academic formation.** I study robotics at university level (kinematics, dynamics, control, measurement), using university courses as references (Georgia Tech ECE 4560, MIT *Robotic Manipulation*, *Modern Robotics*), and derive everything by hand before I code it. See [how I learn](PROGRESS.md#how-i-learn-method-and-references).
- **Real skills.** Python, Linux, electronics, simulation, machine learning and vision, each pulled in when the build needs it.
- **A contribution of my own.** The pieces exist separately in the literature (repeatability tests, servo backlash, policy benchmarks), but nobody has combined them into one quantified error budget for this arm. That is my twist. See [the gap](docs/about.md#why-this-project).
- **Full-stack robotics.** From packets on the servo bus up to the learned policy.
- **Working with AI agents, out of curiosity.** AI agents act as my tutor and reviewer: they ask me questions, make me explain, and catch errors. They also run parts of my workflow, such as drafting this log for my review.

More on the motivation and my starting point: [`docs/about.md`](docs/about.md).

## Where to find what

| If you want… | Go to |
|---|---|
| What has actually been done, with numbers, figures and what I studied | [`PROGRESS.md`](PROGRESS.md), the dated log, newest first |
| Why the project exists, the prior work it builds on, and my goals | [`docs/about.md`](docs/about.md) |
| The error-budget report | [below](#the-error-budget-report); not written yet |
| My study exercises (derived by hand, coded, checked in simulation) | [`sim/exercises/`](sim/exercises/) |
| The physical platform and its bring-up | [`hardware/`](hardware/) |
| The experimental conditions and their results | [`experiments/`](experiments/) |
| Code for measurement and analysis | [`src/`](src/) |

Every folder has its own README explaining what goes in it and what state it's in.

## The approach, briefly

I measure the same task under progressively more complex conditions:

1. **Scripted motion** (no learning), which gives the raw mechanical + control repeatability
2. **A bench-level servo backlash test**, which isolates the mechanical share
3. **A trained policy**, which adds the policy's own variance on top

If these error sources are roughly independent, their variances add, and each contribution can be estimated by subtraction. That independence is an assumption to check against the data, not something to take for granted.

## The error-budget report

*Not written yet. This section is reserved for it.* The report will live in [`docs/`](docs/) and will be linked here once the measurements exist. Planned contents:

1. **The question and the task**: the placement task and what counts as an error.
2. **Method**: the independent measurement rig, ISO 9283-style statistics, and how errors in the joints propagate to the tip through the kinematics.
3. **Results per condition**: scripted motion, servo backlash, learned policy ([`experiments/01`–`03`](experiments/)).
4. **The budget**: each source's share, with uncertainties.
5. **The intervention**: what was changed and the measured improvement ([`experiments/04`](experiments/)).

## How this log is written

I draft the log entries from my private working notes with an AI-assisted workflow: Claude Code and a custom documentation skill. I review and approve each entry by hand before it is committed.
