"""
SO-101 measurement rig, v4 (build123d). All dimensions in mm.

v4 (13 Nov) = v3 after the batch-1 fit test (printed 12 Nov):
  - OV9732 plate: UNCHANGED. All three bolts fit once the board sits on the posts (it had been
    mounted on the flat face by mistake). Measured gold-hole pitch 28.0-28.2; the slots absorb it.
  - webcam: real height ~25.8 (not 24): pillars 21.5 -> 24.3 so the strap bows ~0.5 again
    (the v3 strap was bowed ~4 mm, ~45 MPa: reprint it).
  - webcam pocket 22 -> 21.2 deep: test print had ~1 mm front-back play (camera could tip ~2-4 deg).

v3 (9 Nov) = v2d re-verified against the real cameras. Changes and why:
  - webcam stub is on the BOTTOM (not the back): round clearance pocket in the cradle floor
  - webcam height from the tape is only +-1.5 mm: clamp height is now ADJUSTABLE with printed
    spacers (0-4.5 mm) + 0.5 mm washers, instead of a pillar height that assumes one number
  - cable leaves the back ~13 mm from one end, ~5 mm up: open-top cable notches at BOTH ends
  - front lip split into two end lips, clear of the lens bezel
  - OV9732: lens-holder screws stick out of the board's back at mid-height: the two full-height
    standoff bars became four separate posts; slot travel +-2 (pitch read as 27.8 x 29.4 +-1)
  - D_SIDE 150 -> 155 (webcam sharpness falls faster closer than farther: 5 mm hedge)
  - every clearance is a named TOLERANCE below

Coordinates (the rig's own frame):
  origin = the measured point on the gripper (fixed-jaw tip), projected down onto the desk
  +x     = along the arm's reach (away from the robot base)
  +y     = to the left of the arm, seen from behind the robot
  z = 0  = desk surface
  In the room, rotate the whole rig so +x follows the arm (19 deg at the "best" pose).

Front camera (OV9732) sits at +x and looks back along -x at the gripper.
Side camera (webcam) sits at -y and looks across along +y.

Printed parts = the STL files only. Cameras, board, lens, feet and the red point are "ghosts".

Run:   terminal 1:  conda activate cad ; python -m ocp_viewer   (http://127.0.0.1:3939/viewer)
       terminal 2:  conda activate cad ; python rig.py           (--check: prints every fit and exits)
"""
import sys

from build123d import *

# ------------------------------------------------------------------------------
# MEASUREMENTS (tape + photos, 8-9 Nov 2026). Nominal value, then how sure.
# ------------------------------------------------------------------------------
D_SIDE = 155.0     # webcam lens -> measured point. Ruler test: sharpest ~15-16 cm, worse faster when closer
D_FRONT = 100.0    # OV9732 lens -> measured point. Screw focus, set after mounting
H = 92.0           # fixed-jaw tip above the desk at "best" (tape 90-95)

# webcam (Seeed X10), stand removed
CAM_L, CAM_L_TOL = 70.0, 1.5     # length (tape + photos 70-71)
CAM_D, CAM_D_TOL = 20.5, 0.35    # front-back thickness. v4: test print (pocket 22 CAD) left ~1 mm play -> ~20.5
CAM_H, CAM_H_TOL = 25.8, 1.0     # top-bottom height. v4: fit-test photos 13 Nov: 25.4 / 25.7 / 26.2 (3 methods), was 24 +-2
CAM_FLAT = 50.0                  # flat part of the top/bottom (the ends are rounded)
STUB_OD, STUB_LEN = 14.0, 6.0    # hollow stub, centred on the bottom (OD 13-14, ID 11-12, 6 long)
CABLE_FROM_END, CABLE_Z, CABLE_D = 13.0, 5.0, 4.0   # cable leaves the back face (photos, +-3)
LENS_BEZEL = 17.0                # black ring around the lens, roughly centred (+-2.5)

# OV9732 board
BOARD = 38.0
HOLE_PITCH = 28.6  # gold holes, centre to centre: photo 27.8 (one way) x 29.4 (other), +-1. M2.5 passes (tested)
LENS_REACH = 13.0  # board face -> lens front at 10 cm focus (10-15)
BACK_SCREW_X, BACK_SCREW_ZMAX = 11.5, 2.5   # lens-holder screw heads on the back: |x| <= ~11.5, |z| <= ~2.5
PLUG_W, PLUG_IN = 12.6, 7.4      # plug on the back, centred on one edge, 12.6 wide, reaches 7.4 in from that edge

# ------------------------------------------------------------------------------
# TOLERANCES  (the design rule: only the cameras "fit"; everything else is clearance)
# ------------------------------------------------------------------------------
PRINT_SHRINK = 0.3      # printed holes come out ~0.2-0.3 mm small
CLR_POCKET = 2.0        # radial clearance around things that only need to pass (stub, plug, cable)
M3_CLEAR = 3.6          # M3 through hole (3.0 + shrink + 0.3 play)
M25_SLOT_W = 3.2        # M2.5 slot width
NUT_CLR = 0.4           # extra on nut pockets
SLOT_TRAVEL = 2.0       # OV slots: each hole may sit +-2 mm along its diagonal -> pitch 25.8-31.4

# ------------------------------------------------------------------------------
# FASTENERS AND CLAMP
# ------------------------------------------------------------------------------
M3_NUT_AF, M3_NUT_AC, M3_NUT_T = 5.5, 6.35, 2.4
BOLT_M3 = 16.0          # bought: M3 x 16 stainless, cylinder head
RUB = 1.0               # bike inner tube on the camera's top: takes up roughness, NOT the spring
BOW = 0.5               # camera+rubber stand this much above the strap's pivot line -> the strap bows = the spring
STRAP_T, STRAP_W = 3.0, 14.0
RIDGE_H, RIDGE_W = 1.0, 3.0      # pivot ridge on the strap's underside at each bolt (simply supported strap)
SPACERS = (0.6, 1.0, 1.0, 2.0)   # per side; 0.6 = 3 printed layers, replaces the 0.5 mm steel washers -> 0..4.6 mm, worst step error 0.3
SPACER_MAX = sum(SPACERS)

# frame
CH_W, CH_FLOOR, CH_RIB = 30.0, 2.0, 10.0
PAD_SIDE, PAD_FRONT, PAD_FRONT_Y = 70.0, 50.0, 15.0
FOOT = 3.0
BASE_TOP = FOOT + CH_FLOOR

# ------------------------------------------------------------------------------
# WEBCAM CRADLE
# ------------------------------------------------------------------------------
pocket_l = CAM_L + 2 * CAM_L_TOL                 # 73
pocket_d = CAM_D + 2 * CAM_D_TOL                 # 22
PIL_W = 11.0
pil_x = pocket_l / 2 + PIL_W / 2
CAM_H_MIN = CAM_H - CAM_H_TOL
# pillar top: with zero spacers, the shortest camera stands BOW above the strap's pivot line
PIL_TOP = CAM_H_MIN + RUB - BOW - RIDGE_H        # strap ridge sits on pillar + spacers
NUT_TOP = PIL_TOP - 4.0                          # 4 mm of plastic above the nut
NUT_Z = NUT_TOP - (M3_NUT_T + NUT_CLR) / 2
CRADLE_L = pocket_l + 2 * PIL_W
STOP_T = 3.0
CRADLE_DEPTH = pocket_d + 2 * STOP_T
STOP_H = 10.0
LIP_H, LIP_X0 = 4.0, LENS_BEZEL / 2 + 2.5 + 2.0  # end lips start beyond the bezel (+ its position tolerance + 2)
FLOOR_T = 4.0
STUB_POCKET_D = STUB_OD + 2 * CLR_POCKET         # 18
STUB_POCKET_DEPTH = STUB_LEN + 2.0               # 8 (goes 4 mm into whatever is under the floor)
NOTCH_X0 = CAM_L / 2 - CABLE_FROM_END - 3 - CABLE_D / 2 - 1   # cable notch from here ...
NOTCH_X1 = CAM_L / 2 - CABLE_FROM_END + 3 + CABLE_D / 2 + 1   # ... to here (both ends)
SLOT_IN = pil_x - (M3_NUT_AC / 2 + NUT_CLR)
SLOT_OUT = pil_x + PIL_W / 2 + 1


def webcam_cradle(plinth=0.0):
    """Local: camera centred on x=0, y=0; floor top z=0; lens toward +y.
    plinth: extra solid under the floor (test piece only, so the stub pocket has a bottom)."""
    with BuildPart() as p:
        Box(CRADLE_L, CRADLE_DEPTH, FLOOR_T + plinth, align=(Align.CENTER, Align.CENTER, Align.MAX))
        with Locations((0, -(pocket_d / 2 + STOP_T / 2), 0)):                      # back stop = y datum
            Box(pocket_l, STOP_T, STOP_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        for s in (-1, 1):                                                          # two end lips, clear of the lens
            with Locations((s * (LIP_X0 + (pocket_l / 2 - LIP_X0) / 2), pocket_d / 2 + STOP_T / 2, 0)):
                Box(pocket_l / 2 - LIP_X0, STOP_T, LIP_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-pil_x, 0, 0), (pil_x, 0, 0)):                            # pillars
            Box(PIL_W, 20, PIL_TOP, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-pil_x, 0, PIL_TOP), (pil_x, 0, PIL_TOP)):                # bolt holes
            Hole(M3_CLEAR / 2, depth=PIL_TOP + FLOOR_T - 1)
        for s in (-1, 1):                                                          # nut slots, open to the outside
            with Locations((s * (SLOT_IN + SLOT_OUT) / 2, 0, NUT_Z)):
                Box(SLOT_OUT - SLOT_IN, M3_NUT_AF + NUT_CLR, M3_NUT_T + NUT_CLR, mode=Mode.SUBTRACT)
        for s in (-1, 1):                                                          # open-top cable notches, both ends
            with Locations((s * (NOTCH_X0 + NOTCH_X1) / 2, -(pocket_d / 2 + STOP_T / 2), 1 + STOP_H / 2)):
                Box(NOTCH_X1 - NOTCH_X0, STOP_T + 1, STOP_H, mode=Mode.SUBTRACT)
        with Locations((0, 0, 0)):                                                 # stub pocket
            Cylinder(STUB_POCKET_D / 2, STUB_POCKET_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX),
                     mode=Mode.SUBTRACT)
    return p.part


def webcam_strap():
    """Printed ridges-up; in use it is flipped so the ridges press on the pillars/spacers."""
    with BuildPart() as p:
        Box(CRADLE_L, STRAP_W, STRAP_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-pil_x, 0, STRAP_T), (pil_x, 0, STRAP_T)):
            Box(RIDGE_W, STRAP_W, RIDGE_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-pil_x, 0, 0), (pil_x, 0, 0)):
            Cylinder(M3_CLEAR / 2, 20, mode=Mode.SUBTRACT)
    return p.part


def spacers():
    """One flat set for both sides: 2 x (0.6, 1, 1, 2 mm), 11 x 14 with an M3 hole. Laid out for printing."""
    parts = []
    for i, t in enumerate(SPACERS * 2):
        parts.append(Pos(i * 16, 0, t / 2) * (Box(PIL_W, STRAP_W, t) - Cylinder(M3_CLEAR / 2, 10)))
    out = parts[0]
    for q in parts[1:]:
        out = out + q
    return out


def csk_seats():
    """Printed countersink seats for the M2.5 countersunk heads on the OV9732 board (no steel
    washers to hand). Ø8 x 2.5 puck, 90 deg cone matching the head, Ø3.0 hole (2.5 + shrink).
    Flat side down -> the cone is a 45 deg wall, prints without support. 4 (one spare)."""
    parts = []
    for i in range(4):
        puck = Box(8.0, 8.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        cone = Pos(0, 0, 2.5) * Cone(5.0 / 2 + 0.3, 0.0, 5.0 / 2 + 0.3, align=(Align.CENTER, Align.CENTER, Align.MAX))
        hole = Cylinder(3.0 / 2, 10)
        parts.append(Pos(i * 11, 0, 0) * (puck - cone - hole))
    out = parts[0]
    for q in parts[1:]:
        out = out + q
    return out


# ------------------------------------------------------------------------------
# OV9732 PLATE: four posts (not bars) so the lens-holder screws on the board's back are free
# ------------------------------------------------------------------------------
PLATE = BOARD + 6
PLATE_T = 4.0
POST = 10.0
POST_H = 5.0
PLUG_NOTCH = PLUG_W + 2 * CLR_POCKET              # 16.6 wide gap in the plate's bottom edge
NOTCH_TOP = -(BOARD / 2 - PLUG_IN - CLR_POCKET)   # notch reaches up past the plug


def ov_plate(test_foot=False):
    """Upright in XZ, centred on the origin; posts on the -y face carry the board (lens toward -y);
    bolts through slots in post + plate; nuts on the +y face. Plug at the BOTTOM edge."""
    with BuildPart() as p:
        Box(PLATE, PLATE_T, PLATE)
        for sx in (-1, 1):
            for sz in (-1, 1):
                cx, cz = sx * HOLE_PITCH / 2, sz * HOLE_PITCH / 2
                y0, y1 = -PLATE_T / 2, -PLATE_T / 2 - POST_H                     # post profile (y, z), with a
                with BuildSketch(Plane.YZ.offset(cx - POST / 2)):                # 45 deg wedge underneath so it
                    Polygon((y0, cz + POST / 2), (y1, cz + POST / 2),            # prints without support
                            (y1, cz - POST / 2), (y0, cz - POST / 2 - POST_H), align=None)
                extrude(amount=POST)
                # hole pattern that absorbs a RECTANGULAR pitch error (27.8 x 29.4 read from the photo):
                #   bottom-left  = round datum hole
                #   bottom-right = slot along x   (absorbs the x pitch)
                #   top-left     = slot along z   (absorbs the z pitch)
                #   top-right    = no bolt, the board just rests on the post (3 bolts hold a 38 mm board)
                if (sx, sz) == (1, 1):
                    continue
                with Locations((cx, -POST_H / 2, cz)):
                    with BuildSketch(Plane.XZ):
                        if (sx, sz) == (-1, -1):
                            Circle(M25_SLOT_W / 2)
                        elif (sx, sz) == (1, -1):
                            SlotCenterToCenter(2 * SLOT_TRAVEL, M25_SLOT_W, rotation=0)
                        else:
                            SlotCenterToCenter(2 * SLOT_TRAVEL, M25_SLOT_W, rotation=90)
                    extrude(amount=PLATE_T + 2 * POST_H, both=True, mode=Mode.SUBTRACT)
        with Locations((0, 0, (-PLATE / 2 + NOTCH_TOP) / 2)):                    # plug/cable gap, bottom edge
            Box(PLUG_NOTCH, PLATE_T, NOTCH_TOP + PLATE / 2, mode=Mode.SUBTRACT)
        with Locations((0, 0, -PLATE / 2)):                                      # clip the lower wedges at the
            Box(PLATE + 2, 40, 10, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)  # plate bottom
        if test_foot:
            with Locations((0, 8, -PLATE / 2)):
                Box(PLATE, 20, 4, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return p.part


# ------------------------------------------------------------------------------
# FRAME (unchanged concept: L of U-channels, two towers; material review pending)
# ------------------------------------------------------------------------------
X_BOARD = D_FRONT + LENS_REACH
X_PLATE = X_BOARD + 1.6 + POST_H + PLATE_T / 2
X_FACE = X_PLATE - PLATE_T / 2
plate = Pos(X_PLATE, 0, H) * (Rot(0, 0, -90) * ov_plate())
TOWER_F_D = 24.0
XC = X_FACE + TOWER_F_D / 2
tower_front = Pos(XC, 0, (BASE_TOP + H - PLATE / 2) / 2) * Box(TOWER_F_D, PLATE, H - PLATE / 2 - BASE_TOP)

Y_CAM = -(D_SIDE + CAM_D / 2)                      # camera pushed back against the stop: lens face at -D_SIDE
Y_CRADLE = Y_CAM - CAM_D_TOL                       # pocket centre (the camera rests on the back stop)
FLOOR_Z = H - CAM_H / 2
cradle = Pos(0, Y_CRADLE, FLOOR_Z) * webcam_cradle()
TOP_Z = FLOOR_Z - FLOOR_T
FLARE = (CRADLE_L - 34) / 2
tower_side = (Pos(0, Y_CRADLE + CRADLE_DEPTH / 2, 0) * Rot(90, 0, 0) *
              extrude(Polygon((-17, BASE_TOP), (17, BASE_TOP), (17, TOP_Z - FLARE),
                              (CRADLE_L / 2, TOP_Z), (-CRADLE_L / 2, TOP_Z), (-17, TOP_Z - FLARE)),
                      amount=CRADLE_DEPTH))
tower_side -= Pos(0, Y_CRADLE, TOP_Z) * Cylinder(STUB_POCKET_D / 2, 2 * (STUB_POCKET_DEPTH - FLOOR_T))  # stub pocket continues


def channel(x0, x1, y0, y1):
    along_x = (x1 - x0) > (y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    L = (x1 - x0) if along_x else (y1 - y0)
    part = Pos(cx, cy, FOOT + CH_FLOOR / 2) * (Box(L, CH_W, CH_FLOOR) if along_x else Box(CH_W, L, CH_FLOOR))
    for s in (-1, 1):
        rib = Box(L, 3, CH_RIB) if along_x else Box(3, L, CH_RIB)
        off = (0, s * (CH_W / 2 - 1.5)) if along_x else (s * (CH_W / 2 - 1.5), 0)
        part += Pos(cx + off[0], cy + off[1], FOOT + CH_FLOOR + CH_RIB / 2) * rib
    return part


arm_front = channel(XC - CH_W / 2, XC + CH_W / 2, Y_CRADLE - CH_W / 2, PLATE / 2)
arm_side = channel(-CRADLE_L / 2, XC + CH_W / 2, Y_CRADLE - CH_W / 2, Y_CRADLE + CH_W / 2)
pad_side = Pos(0, Y_CRADLE, FOOT + CH_FLOOR / 2) * Box(CRADLE_L, PAD_SIDE, CH_FLOOR)
pad_front = Pos(XC, PAD_FRONT_Y / 2, FOOT + CH_FLOOR / 2) * Box(PAD_FRONT, PLATE + PAD_FRONT_Y, CH_FLOOR)
frame = arm_front + arm_side + pad_side + pad_front + tower_front + tower_side + plate + cradle
TIE_Z = FOOT + CH_FLOOR + 5
for x in (62.0, 74.0):
    frame -= Pos(x, Y_CRADLE, TIE_Z) * Rot(90, 0, 0) * Cylinder(2.2, CH_W + 2)
for y in (-62.0, -74.0):
    frame -= Pos(XC, y, TIE_Z) * Rot(0, 90, 0) * Cylinder(2.2, CH_W + 2)

# ------------------------------------------------------------------------------
# ghosts (not printed)
# ------------------------------------------------------------------------------
r = CAM_H / 2
cam_body = Pos(0, Y_CAM, H) * (Box(CAM_L - CAM_H, CAM_D, CAM_H)
                               + Pos(-(CAM_L - CAM_H) / 2, 0, 0) * Rot(90, 0, 0) * Cylinder(r, CAM_D)
                               + Pos((CAM_L - CAM_H) / 2, 0, 0) * Rot(90, 0, 0) * Cylinder(r, CAM_D)
                               + Pos(0, 0, -CAM_H / 2 - STUB_LEN / 2) * Cylinder(STUB_OD / 2, STUB_LEN))
board = Pos(X_BOARD + 0.8, 0, H) * Box(1.6, BOARD, BOARD)
lens = Pos(X_BOARD - LENS_REACH / 2, 0, H) * Rot(0, 90, 0) * Cylinder(7, LENS_REACH)
point = Pos(0, 0, H) * Sphere(3)


# ------------------------------------------------------------------------------
# CHECKS: each line = a requirement, the number, pass/fail
# ------------------------------------------------------------------------------
def clamp_window():
    """Strap = simply supported on the two ridges (span 2*pil_x), pushed up at the two ends of the
    camera's flat top (x = +-CAM_FLAT/2). Returns (k N/mm, force range N, max stress MPa)."""
    E, I = 3500.0, STRAP_W * STRAP_T ** 3 / 12
    L, a = 2 * pil_x, pil_x - CAM_FLAT / 2
    k = 2 / (a ** 2 * (3 * L - 4 * a) / (6 * E * I))           # two loads P at distance a from each support
    lo, hi = k * (BOW - 0.3), k * (BOW + 0.3)                  # after shimming with 0.6/1.0 steps: +-0.3
    sigma = (hi / 2) * a * (STRAP_T / 2) / I
    return k, lo, hi, sigma


def checks():
    bb = frame.bounding_box()
    k, lo, hi, sig = clamp_window()
    bolt_need_max = STRAP_T + RIDGE_H + SPACER_MAX + (PIL_TOP - NUT_TOP) + M3_NUT_T
    h_cover = (PIL_TOP + RIDGE_H - RUB + BOW, PIL_TOP + RIDGE_H - RUB + BOW + SPACER_MAX)
    lens_bottom = CAM_H_MIN / 2 - LENS_BEZEL / 2
    rows = [
        ("bed 250 x 210 x 220 (frame long side along X)", f"{bb.size.Y:.0f} x {bb.size.X:.0f} x {bb.size.Z:.0f}",
         bb.size.Y <= 250 and bb.size.X <= 210 and bb.size.Z <= 220),
        ("webcam pocket: length slack each end / depth slack", f"{CAM_L_TOL} / {2 * CAM_D_TOL} (camera pushed onto the back stop)", True),
        ("camera heights the clamp covers (spacers 0..{:.1f})".format(SPACER_MAX),
         f"{h_cover[0]:.1f} .. {h_cover[1]:.1f} mm  vs measured {CAM_H - CAM_H_TOL:.0f}..{CAM_H + CAM_H_TOL:.0f}",
         h_cover[0] <= CAM_H - CAM_H_TOL + 0.01 and h_cover[1] >= CAM_H + CAM_H_TOL),
        ("M3 x 16 long enough at max spacers (full nut engaged)", f"needs {bolt_need_max:.1f}", bolt_need_max <= BOLT_M3),
        ("M3 x 16 not bottoming at zero spacers (hole depth below nut)", f"tip at z = {PIL_TOP + RIDGE_H + STRAP_T - BOLT_M3:.1f}, hole to z = {-FLOOR_T + 1:.0f}",
         PIL_TOP + RIDGE_H + STRAP_T - BOLT_M3 > -FLOOR_T + 1),
        ("clamp: strap bows 0.5 +-0.25 over the flat top's ends", f"k = {k:.0f} N/mm -> {lo:.0f}..{hi:.0f} N, strap {sig:.1f} MPa (creep ~12)", sig <= 12 and lo > 2),
        ("nut slot reaches past the bolt axis", f"{pil_x - SLOT_IN:.2f} >= {M3_NUT_AC / 2:.2f}", pil_x - SLOT_IN >= M3_NUT_AC / 2),
        ("pillar wall inside the nut slot", f"{SLOT_IN - (pil_x - PIL_W / 2):.1f} mm", SLOT_IN - (pil_x - PIL_W / 2) >= 1.5),
        ("plastic above the nut", f"{PIL_TOP - NUT_TOP:.1f} mm", PIL_TOP - NUT_TOP >= 3),
        ("stub pocket vs stub (radial clearance / depth margin)", f"{(STUB_POCKET_D - STUB_OD) / 2:.1f} / {STUB_POCKET_DEPTH - STUB_LEN:.1f}", True),
        ("floor either side of the stub pocket (camera flat bottom rests here)", f"{CAM_FLAT / 2 - STUB_POCKET_D / 2:.1f} mm each side", CAM_FLAT / 2 - STUB_POCKET_D / 2 >= 10),
        ("cable notch covers 13 +-3 mm from either end", f"x {NOTCH_X0:.1f}..{NOTCH_X1:.1f} (cable centre {CAM_L / 2 - CABLE_FROM_END:.1f})", True),
        ("end lips clear of the lens bezel (worst case)", f"lips from |x| = {LIP_X0:.1f}, bezel to {LENS_BEZEL / 2 + 2.5:.1f}", LIP_X0 > LENS_BEZEL / 2 + 2.5),
        ("lip below the lens bottom anyway? (not needed: lips are beside it)", f"lip {LIP_H}, lens bottom >= {lens_bottom:.1f}", True),
        ("OV holes: datum + x-slot + z-slot cover pitch (independently each way)", f"{HOLE_PITCH - SLOT_TRAVEL:.1f} .. {HOLE_PITCH + SLOT_TRAVEL:.1f} (photo 27.8 / 29.4)",
         HOLE_PITCH - SLOT_TRAVEL <= 26.8 and HOLE_PITCH + SLOT_TRAVEL >= 30.4),
        ("wall around each OV slot in its post", f"{POST / 2 - (SLOT_TRAVEL + M25_SLOT_W / 2):.1f} mm", POST / 2 - (SLOT_TRAVEL + M25_SLOT_W / 2) >= 1.3),
        ("posts clear of the lens-holder screws on the back", f"posts from |z| = {HOLE_PITCH / 2 - POST / 2:.1f}, screws within |z| <= {BACK_SCREW_ZMAX}",
         HOLE_PITCH / 2 - POST / 2 > BACK_SCREW_ZMAX + 1),
        ("posts clear of the plug (x)", f"posts from |x| = {HOLE_PITCH / 2 - POST / 2:.1f}, plug to {PLUG_W / 2:.1f}", HOLE_PITCH / 2 - POST / 2 >= PLUG_W / 2 + 2),
        ("post height vs plug / screw heads (~3)", f"{POST_H} mm", POST_H >= 4),
        ("M2.5 x 20 length: washer + board + post + plate + washer + nut", f"{0.5 + 1.6 + POST_H + PLATE_T + 0.5 + 2.0:.1f} -> {20 - (0.5 + 1.6 + POST_H + PLATE_T + 0.5 + 2.0):.1f} sticks out", True),
        ("frame CAD volume", f"{frame.volume / 1000:.0f} cm3", True),
    ]
    ok_all = True
    for name, val, ok in rows:
        print(f"  [{'OK' if ok else '!!'}] {name}: {val}")
        ok_all &= ok
    return ok_all


if __name__ == "__main__":
    print("checks:")
    ok = checks()
    exports = [("rig_frame", Rot(0, 0, 90) * Pos(0, 0, -FOOT) * frame),
               ("rig_webcam_strap", webcam_strap()),
               ("rig_spacers", spacers()),
               ("rig_csk_seats", csk_seats()),
               ("test_webcam_cradle", Pos(0, 0, FLOOR_T + 6) * webcam_cradle(plinth=6.0)),
               ("test_ov9732_plate", Pos(0, 0, PLATE / 2) * ov_plate(test_foot=True))]
    for name, part in exports:
        export_stl(part, f"{name}.stl", tolerance=0.05)
        export_step(part, f"{name}.step")
        s = part.bounding_box().size
        print(f"  wrote {name}.stl  {s.X:.0f} x {s.Y:.0f} x {s.Z:.0f} mm, {part.volume / 1000:.1f} cm3")
    if "--check" in sys.argv:
        sys.exit(0 if ok else 1)
    try:
        from ocp_vscode import show
        show(frame, webcam_strap(), cam_body, board, lens, point,
             names=["frame", "strap", "webcam (ghost)", "OV9732 board", "OV9732 lens", "measured point"],
             colors=["#5c6270", "#9aa3b2", "black", "darkgreen", "black", "red"], alphas=[1, 1, 0.5, 1, 1, 1], port=3939)
    except Exception as e:
        print("viewer not available:", e)
