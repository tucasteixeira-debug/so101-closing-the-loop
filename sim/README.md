# sim/

Simulation work on the public SO-101 model in MuJoCo. Everything here runs on the simulated arm, not the hardware.

- [`exercises/`](exercises/): my study exercises, each derived by hand first and then coded and checked against MuJoCo. Only selected exercises are published.

## Setup

The exercises use TheRobotStudio's official SO-101 model and MuJoCo's Python bindings:

```bash
git clone https://github.com/TheRobotStudio/SO-ARM100 ~/SO-ARM100
conda activate lerobot
pip install mujoco
```

The scripts expect the model at `~/SO-ARM100/Simulation/SO101/scene.xml`.
