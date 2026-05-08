"""Rule-based posture classifier.

This module converts body landmarks into interpretable measurements:
neck angle, trunk angle, shoulder tilt, head offset, score, and risk level.
"""

from __future__ import annotations

import math


def _point(landmarks: dict[str, tuple[int, int] | None], name: str):
    return landmarks.get(name)


def _angle(a, b, c) -> float | None:
    if a is None or b is None or c is None:
        return None

    bax = a[0] - b[0]
    bay = a[1] - b[1]
    bcx = c[0] - b[0]
    bcy = c[1] - b[1]

    mag_ba = math.hypot(bax, bay)
    mag_bc = math.hypot(bcx, bcy)

    if mag_ba == 0 or mag_bc == 0:
        return None

    cosine = (bax * bcx + bay * bcy) / (mag_ba * mag_bc)
    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(math.acos(cosine))


def classify_posture(landmarks: dict[str, tuple[int, int] | None]):
    """Classify posture from 2D pose landmarks.

    Returns:
        status, issues, measurements
    """
    left_shoulder = _point(landmarks, "left_shoulder")
    right_shoulder = _point(landmarks, "right_shoulder")
    left_hip = _point(landmarks, "left_hip")
    right_hip = _point(landmarks, "right_hip")
    left_ear = _point(landmarks, "left_ear")
    right_ear = _point(landmarks, "right_ear")
    nose = _point(landmarks, "nose")

    required = [left_shoulder, right_shoulder, left_hip, right_hip]

    if any(point is None for point in required):
        return "UNKNOWN", ["NO_PERSON"], {
            "neck": None,
            "trunk": None,
            "shoulder_tilt": None,
            "head_offset": None,
            "score": 0,
            "risk_level": "Unknown",
        }

    shoulder_mid = (
        int((left_shoulder[0] + right_shoulder[0]) / 2),
        int((left_shoulder[1] + right_shoulder[1]) / 2),
    )

    hip_mid = (
        int((left_hip[0] + right_hip[0]) / 2),
        int((left_hip[1] + right_hip[1]) / 2),
    )

    ear_points = [point for point in (left_ear, right_ear) if point is not None]

    ear_mid = None
    if ear_points:
        ear_mid = (
            int(sum(point[0] for point in ear_points) / len(ear_points)),
            int(sum(point[1] for point in ear_points) / len(ear_points)),
        )

    neck_angle = _angle(ear_mid or nose, shoulder_mid, hip_mid)
    trunk_angle = _angle(shoulder_mid, hip_mid, (hip_mid[0], hip_mid[1] + 100))

    shoulder_width = max(1, abs(left_shoulder[0] - right_shoulder[0]))

    shoulder_tilt = abs(left_shoulder[1] - right_shoulder[1]) / shoulder_width * 100

    head_offset = 0
    if ear_mid is not None:
        head_offset = abs(ear_mid[0] - shoulder_mid[0]) / shoulder_width * 100

    issues = []
    score = 100

    if head_offset > 18:
        issues.append("HEAD_FORWARD")
        score -= min(30, int((head_offset - 18) * 1.5) + 15)

    if neck_angle is not None and neck_angle < 150:
        issues.append("NECK_BENT")
        score -= min(25, int((150 - neck_angle) * 0.8) + 10)

    if trunk_angle is not None and trunk_angle > 16:
        issues.append("LEANING_FORWARD")
        score -= min(25, int((trunk_angle - 16) * 1.2) + 10)

    if shoulder_tilt > 12:
        issues.append("SHOULDER_TILT")
        score -= min(20, int((shoulder_tilt - 12) * 1.5) + 8)

    score = max(0, min(100, score))

    if score >= 80:
        status = "CORRECT"
        risk_level = "Low"
    elif score >= 55:
        status = "WARNING"
        risk_level = "Medium"
    else:
        status = "INCORRECT"
        risk_level = "High"

    measurements = {
        "neck": neck_angle,
        "trunk": trunk_angle,
        "shoulder_tilt": shoulder_tilt,
        "head_offset": head_offset,
        "score": score,
        "risk_level": risk_level,
    }

    return status, issues, measurements
