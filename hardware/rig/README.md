# Measurement rig v4 — print files

**v4 (13 Nov)** = v3 after the batch-1 fit test (printed 12 Nov):
- **OV9732 plate: unchanged, it works.** All three bolts fit once the board sits on the post tops.
  (First attempt had the board on the flat face, where the test foot and the plug gap squeezed it
  ~1 mm off and only the z-slot bolt would go in.) Gold-hole pitch measured from photos: 28.0–28.2.
- **Webcam:** real height ≈ 25.8 mm (photo measurements 25.4 / 25.7 / 26.2), not 24. The v3 strap
  had to bow ~4 mm (~45 MPa in PLA) → pillars 21.5 → 24.3 so it bows 0.5 again. **Reprint the strap.**
- **Webcam pocket** 22 → 21.2 deep: v3 left ~1 mm front-back play (camera could tip 2–4°);
  v4 leaves ≈ 0.4 mm after print shrink (< 1°).

Two-camera rig that watches one point on the SO-101 gripper (the fixed-jaw tip) in the
"best" pose. Design process: [`PROGRESS.md`](../../PROGRESS.md). Geometry: `rig.py` (build123d; every
measurement and every tolerance is named at the top; `python rig.py --check` prints all fits).

**v3 (9 Nov)** = v2d re-verified against the real cameras. What changed and why is in the
docstring of `rig.py`. Short version: the webcam's stub is on the bottom (pocket in the floor),
the clamp height is adjustable (camera height is only known to ±2 mm), cable notches at both
ends, OV9732 on four posts (the lens-holder screws on the board's back hit the old bars),
holes = one round datum + one slot along x + one slot along z + one plain rest post
(a rectangular pitch error, 27.8 × 29.4, cannot be absorbed by four 45° slots), D_SIDE 155.

## Design rule for tolerances

Only the cameras *fit*; everything else is clearance.

| what | rule | value |
|---|---|---|
| webcam pocket | measured ± error, camera pushed onto the back stop | length +1.5 each end, depth +0.7 (≈ 0.4 after print) |
| webcam height | not designed to a number: printed spacers (0–4.6) | covers 24.8–29.4 mm with the 1 mm rubber, 23.8–28.4 without |
| things that only pass (stub, plug, cable) | measured + 2 mm all round | stub pocket Ø18 × 8 deep |
| M3 holes / M2.5 slots | printed holes shrink 0.2–0.3 | Ø3.6 / 3.2 wide |
| OV9732 hole pitch | datum hole + x-slot + z-slot, ±2 each way | accepts 26.6–30.6 in each direction independently |
| aim (H, D) | fields are 150+ mm wide | ±5 mm is irrelevant |

## Files

| file | what | batch |
|---|---|---|
| `test_webcam_cradle.stl` | webcam mount alone (6 mm plinth so the stub pocket has a bottom), 95 × 28 × 32 | 1 |
| `rig_webcam_strap.stl` | strap, 95 × 14 × 4, **print ridges up**; in use the ridges face down | 1 |
| `rig_spacers.stl` | 6 spacers (2 × 1, 1, 2 mm), 11 × 14 | 1 |
| `test_ov9732_plate.stl` | OV9732 mount alone, with a foot, 44 × 25 × 44 | 1 |
| `rig_frame.stl` / `.step` | one-piece L-frame, 238 × 204 × 111 (fits the MK4 bed) | 2, after batch 1 fits |
| `rig_v3.png` | overview renders | — |

Batch 1 ≈ 40 g (≈ €4 at €0.10/g). Frame ≈ 121 g in the slicer ≈ €12.
Print: PLA, 0.2 mm layers, 3 walls, 15–20 % infill, **no supports** (only short bridges over
nut slots, bolt holes and the plug gap), each part flat side down as exported.

## Hardware

- 2 × M3 × 16 cylinder head + 2 nuts (strap) + **4 × M3 washers** (0.5 mm fine adjustment)
- 3 × M2.5 × 20 + nuts + **6 × M2.5 washers** (one under each countersunk head, on the board; one under each nut, on the plastic). The fourth gold hole has no bolt: that post is a rest.
- strip of bike inner tube ≈ 45 × 14 × 1 mm (on the camera's flat top)
- 5 stick-on pads (bought Ø15) ~8 mm in from the pad corners; 400 g ballast (steel bars or coins) in the troughs; zip ties

## Assembly

1. **Webcam.** Stand off (the 6 mm stub stays: it drops into the floor pocket). Camera in, lens toward
   the gripper, pushed back against the back stop; the cable goes out through whichever end notch it
   is near. Rubber strip on the flat top.
2. **Clamp height.** Put spacers on both pillars, lay the strap on (ridges down), no bolts yet.
   Goal: the strap rests on the camera and there is a **gap of about half a millimetre** between each
   ridge and its spacer stack (a 0.5 mm washer just slides in, a 1 mm spacer does not).
   Too big a gap → add a spacer or washer; strap rocks on the ridges → remove one.
   Then bolt down until the ridges touch, and stop. The bowed strap presses 6–19 N.
3. **OV9732.** Board **on the post tops, lens facing away from the plate** (not on the flat face). Plug at the BOTTOM edge (it sits in the plate's bottom gap). Bolt the bottom-left hole first
   (round datum), then bottom-right (x-slot) and top-left (z-slot); the top-right corner rests on its post. Each: washer under each countersunk head, then board, post, plate, washer, nut. Snug, not tight
   (the plated ring is thin). Focus at 10 cm, then tape the lens.
4. Feet, ballast, cables tied to the base with a loose loop up to each camera.
5. Rig's front arm along the arm's reach (19° to the desk edge at "best"); webcam on the arm's right.
6. Before any series: fix exposure/white balance by hand, warm up, run the noise test.

## Verified by `rig.py --check` and a verification script (9 Nov; output in `verify.log`)

The verification script does real boolean intersections: webcam at min/nominal/max size vs the cradle, board + plug +
lens-holder screw heads vs the plate, all ghosts vs the frame, bolt axes traced through strap → pillar → nut
slot, clamp force for every camera height in 0.5 mm steps, cable exit for both ends and both slack positions,
gold-hole pattern for every pitch combination 26.8–30.4 × 26.8–30.4. Log: `verify.log`.

All fits above, plus: M3 × 16 reaches a full nut with the maximum spacer stack (needs 14.9);
4 mm of plastic above each nut; 16 mm of floor either side of the stub pocket; end lips start at
|x| = 13, the lens bezel ends at ≤ 11; posts start at 9.3 mm from the centre, the plug ends at 6.3 and
the lens-holder screws stay within ±2.5 mm of mid-height; every STL one watertight body.

## Not yet verified

- The arm's **path** from the home pose to "best" past the side tower (only the static pose was checked).
- The v4 webcam cradle itself (only v3 was printed). Its pocket is 0.4 mm narrower and its pillars 2.8 mm taller; nothing else changed.
- Frame material: one L-frame vs two separate stands (open decision).
