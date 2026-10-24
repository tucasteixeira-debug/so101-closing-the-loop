# About This Project

## The objective

Characterize and improve the placement repeatability of the SO-101 6-DOF
arm under a learned manipulation policy — measured independently of the
arm's own sensors — and identify whether the dominant source of error is
mechanical (backlash/compliance), control (servo tuning), or the learned
policy itself. Apply one targeted intervention and quantify the
improvement.

## Why this project

Physical AI — robots that combine perception, learning, and real-world
action — is what pulls me toward this space in the first place. It's
genuinely fast-moving right now: real commercial deployments already
exist, not just demos — Ambi Robotics and Pickle Robot announced the
first fully commercial truck-unloading-to-palletizing integration in
mid-2026, Agility Robotics' Digit runs in live Amazon warehouses, and
Boston Dynamics' Atlas is deployed at Hyundai. Humanoid platforms are
moving from lab demonstrations toward real pilots too — Figure AI's
robots have been tested on BMW's factory floor — though it's an honest,
mixed picture rather than a clean success story: that same pilot
reportedly ran at a fraction of human speed at first and needed a
hardware redesign along the way. Market-size projections for the space
vary by several times over depending which analyst you ask, which says
more about how unsettled the space still is than about its actual size.

Separately from the market picture, there's a specific, concrete gap
this project fills. The individual pieces it combines already exist on
their own:

- **ISO 9283-style repeatability of low-cost arms, with external ground
  truth.** PyRobot's test of the LoCoBot arm [1] measured 0.33–0.58 mm
  per pose with motion capture (10 cycles per pose), and HELENE [2], a
  3D-printed six-axis arm, measured 0.87 mm on a coordinate measuring
  machine. Neither splits the error into its sources.
- **Servo-level backlash of the STS3215**, the SO-101's own servo. An
  open-source test stand [3] measured 0.62° unloaded and 1.30° under a
  load of about 0.3 kgf.
- **A benchmark of learned policies on the SO-101** [4]. Most failed
  trials came from execution (unstable grasps, repetition loops) rather
  than perception, but no hardware quantities were measured.

Nobody has yet combined these into one quantified error budget for this
platform. There isn't even a public repeatability figure for a stock
SO-101: a question asking for one in the official hardware repository is
unanswered [5]. That's a real, specific, citable hole, not a market
claim.

I want to build genuine ability to work in this space and with this
technology — not stake out a specific lane within it yet, just get
real, hands-on capability and understanding.

## What I'm building toward

This project is deliberately structured to force real skills in, by
necessity, rather than studying them in isolation beforehand:

- **Full-stack technical maturity** — electronics, Linux, embedded
  systems, CAD, and control theory, each pulled in exactly when the
  build genuinely needs it
- **Conceptual fluency across the stack** — computer architecture,
  communication protocols, operating systems and the kernel, electronics,
  and embedded control systems — not just the high-level robotics/ML
  layer sitting on top of them
- **A mature, deliberate AI-assisted workflow** — using agents and
  Claude Code for real automation (build-log generation, recurring
  tasks), not ad hoc prompting
- **Real design judgment** — making and defending actual engineering
  decisions (measurement-rig design, the eventual intervention, task
  geometry) under real constraints, not following a prescribed path
- **An honest, dated build log** — this repo itself, written as the
  project happens rather than curated afterward
- **A genuine springboard** — a rigorous, portfolio-grade result
  relevant to physical-AI work, and a plausible foundation for further
  graduate research

## Where I'm starting from

Going in, my conceptual understanding across almost all of these areas
is close to zero — not just hands-on skill, but the underlying concepts
themselves: AI and machine learning, computer architecture, operating
systems, and most of Linux. I have some real prior exposure to embedded
control systems and electronics from earlier coursework, but it's
limited, not a strong foundation to build the rest from. The gap between
that starting point and what full-stack physical-AI work actually
demands is the real subject of this log, not something to smooth over.

## How I'm approaching it

One integrated build, not a series of separate exercises — every area
above gets pulled in only once the project genuinely needs it, learned
by doing rather than pre-studied. The measure of success isn't a flashy
end result; it's whether the engineering underneath it — the debugging,
the design choices, the honest dead ends — actually holds up.

## References

1. A. Murali et al., "PyRobot: An Open-source Robotics Framework for
   Research and Benchmarking", arXiv:1906.08236, 2019, §4.2.
   <https://arxiv.org/abs/1906.08236>
2. Herbst, Suppelt, Schäfer, Chadda, Kupnik, "HELENE: Six-Axis
   Accessible Open-Source 3D-Printed Robotic Arm for Research and
   Education", *Hardware* 3(3):7, 2025. <https://www.mdpi.com/2813-6640/3/3/7>
3. B. Kotov, "An open-source test stand for backlash measurement in
   low-cost UART servo motors", *HardwareX* 26, e00767, 2026.
   <https://doi.org/10.1016/j.ohx.2026.e00767>
4. Y. Yu, X. Qiu, "Benchmarking Vision-Language-Action Models on SO-101:
   Failure and Recovery Analysis", arXiv:2606.08881, 2026.
   <https://arxiv.org/abs/2606.08881>
5. TheRobotStudio/SO-ARM100, issue #181, "What positional repeatability
   should I expect from a stock SO-ARM101".
   <https://github.com/TheRobotStudio/SO-ARM100/issues/181>
