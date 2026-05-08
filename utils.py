import cv2
import math
import numpy as np


# ── Colour palette ────────────────────────────────────────────────────────
GREEN  = (50,  205, 50)
RED    = (60,   60, 240)
YELLOW = (30,  200, 230)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
DARK   = (20,  20,  20)
CYAN   = (230, 190, 30)
# ─────────────────────────────────────────────────────────────────────────


def draw_status_banner(frame, status):
    """Coloured banner at top of frame showing posture status."""
    h, w = frame.shape[:2]
    colour = GREEN if status == "CORRECT" else (RED if status == "INCORRECT" else YELLOW)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 56), colour, -1)
    cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)
    cv2.putText(frame, f"Posture: {status}", (16, 38),
                cv2.FONT_HERSHEY_DUPLEX, 1.1, WHITE, 2, cv2.LINE_AA)
    return frame


def draw_issues(frame, issues):
    """Render issue list in bottom-left corner."""
    h, w = frame.shape[:2]
    y0 = h - (len(issues) * 30) - 10
    for i, issue in enumerate(issues):
        y = y0 + i * 30
        cv2.putText(frame, f"! {issue}", (12, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.56, RED, 1, cv2.LINE_AA)
    return frame


def draw_angle_table(frame, angles):
    """Small table in top-right showing computed angles."""
    h, w = frame.shape[:2]
    entries = []
    if angles.get("neck") is not None:
        entries.append(("Neck dev", f"{abs(180 - angles['neck']):.0f}deg"))
    if angles.get("trunk") is not None:
        entries.append(("Trunk", f"{angles['trunk']:.0f}deg"))
    if angles.get("shoulder_tilt") is not None:
        entries.append(("Shoulder tilt", f"{angles['shoulder_tilt']:.1f}%"))

    box_w, row_h = 190, 26
    x0 = w - box_w - 10
    y0 = 70

    overlay = frame.copy()
    cv2.rectangle(overlay, (x0 - 6, y0 - 20),
                  (x0 + box_w, y0 + len(entries) * row_h + 4), DARK, -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, "Angles", (x0, y0 - 4),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, CYAN, 1)
    for i, (name, val) in enumerate(entries):
        y = y0 + (i + 1) * row_h - 4
        cv2.putText(frame, f"{name}:", (x0, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, WHITE, 1)
        cv2.putText(frame, val, (x0 + 130, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, YELLOW, 1)
    return frame


def draw_angle_arc(frame, a, b, c, angle_val, colour=WHITE):
    """Draw an arc at joint B between vectors BA and BC."""
    if None in (a, b, c) or angle_val is None:
        return frame
    radius = 30
    angle_ab = math.atan2(a[1] - b[1], a[0] - b[0])
    angle_cb = math.atan2(c[1] - b[1], c[0] - b[0])
    start_deg = int(math.degrees(angle_ab))
    end_deg   = int(math.degrees(angle_cb))
    cv2.ellipse(frame, b, (radius, radius), 0, start_deg, end_deg, colour, 2)
    cv2.putText(frame, f"{angle_val:.0f}deg",
                (b[0] + radius + 4, b[1] + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, colour, 1, cv2.LINE_AA)
    return frame


def draw_keypoint_dot(frame, pt, colour=WHITE, radius=6):
    """Draw a filled circle at a keypoint."""
    if pt:
        cv2.circle(frame, pt, radius, colour, -1)
        cv2.circle(frame, pt, radius + 1, BLACK, 1)
    return frame


def draw_fps(frame, fps):
    """Render FPS counter."""
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    return frame