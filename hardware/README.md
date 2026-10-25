# hardware/

The physical platform, and anything built on top of it.

## Platform

The SO-101 is an open-source leader/follower arm pair built around Feetech STS3215-family bus servos. The leader is moved by hand to demonstrate a task, and the follower reproduces it.

| Part | Purpose |
|---|---|
| SO-ARM101 Pro servo motor kit | Servos for both arms, plus the USB bus driver boards |
| SO-101 3D-printed parts | Frames for both arms |
| 2× 1080p USB webcam (different brands) | Wrist and overview cameras for the policy. Two identical models can clash on USB identification |
| Spare Feetech ST3215-C047 (12 V, 30 kg) | Covers any follower joint. The follower's servos are identical, the leader's are not |

Total platform cost: about $343, including the frame and one camera.

## Bring-up status

| Step | Status |
|---|---|
| Follower arm motor IDs | ✅ Done: IDs 1–6 assigned (2026-09) |
| Leader arm motor IDs | ✅ Done: IDs 1–6, matched to joints by gear ratio (2026-09) |
| Mechanical assembly | ✅ Done: both arms (2026-10) |
| Calibration (`lerobot-calibrate`) | ✅ Done: both arms, 6/6 joints each (2026-10) |
| Teleoperation | ✅ Working: follower copies the leader at 59.1 Hz (target 60 Hz) |
| Stable port names (`/dev/serial/by-id/`) | Not yet set up |
| Independent measurement rig | Not yet designed |

Details and dates are in [`PROGRESS.md`](../PROGRESS.md).

## Notes worth knowing if you're building one

- **A lit power LED does not prove a driver board works.** Power delivery and USB-to-bus data relay are separate circuits, and one can fail while the other works. Test any new board with one known-good servo before trusting it.
- **Label each servo the moment its ID is written.** The follower's six servos are physically identical, and the ID is invisible once written.
- **The leader arm's servos are not interchangeable.** They use three different gear ratios across the joints (1/191, 1/345, 1/147).
- **`/dev/ttyACM#` numbering changes across reconnects.** Re-run `lerobot-find-port` rather than assuming a fixed port. With the ports swapped, teleoperation drives the leader and leaves the follower limp.
- **If servos beyond a certain ID stop answering, suspect the cable after the last one that answers.** On both of my arms, a connector pin in the servo 2 → 3 cable had broken and had to be re-soldered.

## Planned

- `measurement-rig/`: the independent ground-truth rig. The leading option is a fixed camera with fiducial markers; a mechanical fixture is the fallback. CAD files and design notes go here once it's designed. The rig will also be the sensor for the closed-loop correction, where the camera's measured residual drives a correction step (design session pending).
