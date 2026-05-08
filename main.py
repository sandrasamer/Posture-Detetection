"""Offline posture detection app.

Run with:
    python main.py

Keyboard:
    F       cycle image-processing view
    S       save a screenshot for the report
    Q / Esc quit
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import time

import cv2
import numpy as np

from ai_feedback import format_feedback_lines, get_feedback
from detector import PoseDetector
from posture_classifier import classify_posture
from utils import (
    BLACK,
    CYAN,
    WHITE,
    draw_angle_table,
    draw_fps,
    draw_issues,
    draw_keypoint_dot,
    draw_status_banner,
)


FILTER_MODES = [
    "normal",
    "gaussian",
    "contrast",
    "histogram",
    "canny",
    "sobel",
    "laplacian",
    "fft",
    "contours",
    "features",
]

SCREENSHOT_DIR = Path(__file__).with_name("screenshots")
LOG_DIR = Path(__file__).with_name("logs")
LOG_INTERVAL_SECONDS = 1.0
AUTO_SCREENSHOT_SECONDS = 8.0


def preprocess_frame(frame, mode):
    """Apply classic image-processing techniques for analysis/demo views."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if mode == "gaussian":
        return cv2.GaussianBlur(frame, (7, 7), 0)

    if mode == "contrast":
        return cv2.convertScaleAbs(frame, alpha=1.25, beta=18)

    if mode == "histogram":
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        y_channel, cr, cb = cv2.split(ycrcb)
        y_channel = cv2.equalizeHist(y_channel)
        enhanced = cv2.merge((y_channel, cr, cb))
        return cv2.cvtColor(enhanced, cv2.COLOR_YCrCb2BGR)

    if mode == "canny":
        edges = cv2.Canny(gray, 80, 160)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if mode == "sobel":
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = cv2.magnitude(grad_x, grad_y)
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        return cv2.cvtColor(magnitude.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    if mode == "laplacian":
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
        laplacian = cv2.convertScaleAbs(laplacian)
        return cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)

    if mode == "fft":
        spectrum = np.fft.fft2(gray)
        spectrum = np.fft.fftshift(spectrum)
        magnitude = 20 * np.log(np.abs(spectrum) + 1)
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        spectrum_bgr = cv2.cvtColor(magnitude.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        return cv2.applyColorMap(spectrum_bgr, cv2.COLORMAP_TURBO)

    if mode == "contours":
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 70, 150)
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        output = frame.copy()
        cv2.drawContours(output, contours, -1, (0, 255, 255), 1)
        return output

    if mode == "features":
        output = frame.copy()

        if hasattr(cv2, "SIFT_create"):
            detector = cv2.SIFT_create(nfeatures=120)
            label = "SIFT keypoints"
        else:
            detector = cv2.ORB_create(nfeatures=120)
            label = "ORB keypoints"

        keypoints = detector.detect(gray, None)
        output = cv2.drawKeypoints(output, keypoints, None, color=(0, 255, 255))

        cv2.putText(
            output,
            label,
            (12, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        return output

    return frame.copy()


def draw_feedback(frame, feedback):
    lines = format_feedback_lines(feedback)

    x = 12
    y = 78
    max_width = min(frame.shape[1] - 24, 720)
    height = 26 + len(lines) * 24

    overlay = frame.copy()
    cv2.rectangle(overlay, (8, 60), (max_width, 60 + height), BLACK, -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    cv2.putText(
        frame,
        "Feedback",
        (x, y),
        cv2.FONT_HERSHEY_DUPLEX,
        0.55,
        CYAN,
        1,
        cv2.LINE_AA,
    )

    for i, line in enumerate(lines[:4]):
        cv2.putText(
            frame,
            line,
            (x, y + 26 + i * 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            WHITE,
            1,
            cv2.LINE_AA,
        )

    return frame


def draw_score(frame, score, risk_level):
    h, w = frame.shape[:2]
    score = int(score or 0)

    if score >= 80:
        colour = (50, 205, 50)
    elif score >= 55:
        colour = (30, 200, 230)
    else:
        colour = (60, 60, 240)

    x0 = w - 230
    y0 = h - 64

    overlay = frame.copy()
    cv2.rectangle(overlay, (x0, y0), (w - 10, h - 12), BLACK, -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    cv2.putText(
        frame,
        f"Score {score}%",
        (x0 + 10, y0 + 24),
        cv2.FONT_HERSHEY_DUPLEX,
        0.58,
        colour,
        1,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Risk: {risk_level}",
        (x0 + 10, y0 + 46),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        WHITE,
        1,
        cv2.LINE_AA,
    )

    cv2.rectangle(frame, (x0 + 116, y0 + 13), (w - 24, y0 + 30), WHITE, 1)

    bar_width = int((w - x0 - 146) * score / 100)

    cv2.rectangle(
        frame,
        (x0 + 118, y0 + 15),
        (x0 + 118 + bar_width, y0 + 28),
        colour,
        -1,
    )

    return frame


def draw_mode_panel(frame, mode, saved_message, bad_posture_seconds, session_average):
    h = frame.shape[0]

    lines = [
        f"Mode: {mode.title()}",
        f"Bad posture time: {bad_posture_seconds:.1f}s",
        f"Session average: {session_average:.1f}%",
        "F: filter  S: save  Q/Esc: quit",
    ]

    if saved_message:
        lines.append(saved_message)

    x = 12
    y = h - 122

    overlay = frame.copy()
    cv2.rectangle(overlay, (8, y - 22), (430, y + len(lines) * 24), BLACK, -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    for i, line in enumerate(lines):
        if i == 0:
            colour = CYAN
        else:
            colour = WHITE

        cv2.putText(
            frame,
            line,
            (x, y + i * 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            colour,
            1,
            cv2.LINE_AA,
        )

    return frame


def save_screenshot(frame, status, mode, reason):
    SCREENSHOT_DIR.mkdir(exist_ok=True)

    filename = SCREENSHOT_DIR / (
        f"posture_{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
        f"{status.lower()}_{mode}_{reason}.png"
    )

    cv2.imwrite(str(filename), frame)

    return filename


def open_log_file():
    LOG_DIR.mkdir(exist_ok=True)

    filename = LOG_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    file = filename.open("w", newline="", encoding="utf-8")
    writer = csv.writer(file)

    writer.writerow(
        [
            "time",
            "mode",
            "status",
            "risk_level",
            "score",
            "neck_angle",
            "trunk_angle",
            "shoulder_tilt",
            "head_offset",
            "issues",
        ]
    )

    return filename, file, writer


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check camera permission or try another camera index."
        )

    detector = PoseDetector()
    previous = time.time()

    mode_index = 0
    saved_message = ""
    saved_message_until = 0.0

    bad_posture_seconds = 0.0
    last_log_time = 0.0
    last_auto_screenshot_time = 0.0

    score_total = 0.0
    score_count = 0

    log_filename, log_file, log_writer = open_log_file()

    try:
        while True:
            ok, frame = cap.read()

            if not ok:
                break

            frame = cv2.flip(frame, 1)

            mode = FILTER_MODES[mode_index]
            processed_frame = preprocess_frame(frame, mode)

            analysis_only_modes = {
                "canny",
                "sobel",
                "laplacian",
                "fft",
                "contours",
                "features",
            }

            if mode in analysis_only_modes:
                detection_frame = frame
            else:
                detection_frame = processed_frame

            results = detector.detect(detection_frame)
            landmarks = detector.extract_landmarks(detection_frame, results)

            status, issues, measurements = classify_posture(landmarks)
            feedback = get_feedback(status, issues)

            score = measurements.get("score", 0)
            risk_level = measurements.get("risk_level", "Unknown")

            display_frame = processed_frame.copy()
            detector.draw_pose(display_frame, results)

            for point in landmarks.values():
                draw_keypoint_dot(display_frame, point)

            now = time.time()
            delta = now - previous
            fps = 1.0 / max(delta, 0.000001)
            previous = now

            if status in ("WARNING", "INCORRECT"):
                bad_posture_seconds += delta

            score_total += score
            score_count += 1
            session_average = score_total / max(score_count, 1)

            draw_status_banner(display_frame, status)
            draw_feedback(display_frame, feedback)
            draw_angle_table(display_frame, measurements)
            draw_score(display_frame, score, risk_level)

            draw_issues(
                display_frame,
                [issue.replace("_", " ").title() for issue in issues],
            )

            draw_fps(display_frame, fps)

            if now > saved_message_until:
                saved_message = ""

            draw_mode_panel(
                display_frame,
                mode,
                saved_message,
                bad_posture_seconds,
                session_average,
            )

            if now - last_log_time >= LOG_INTERVAL_SECONDS:
                log_writer.writerow(
                    [
                        datetime.now().isoformat(timespec="seconds"),
                        mode,
                        status,
                        risk_level,
                        score,
                        measurements.get("neck"),
                        measurements.get("trunk"),
                        measurements.get("shoulder_tilt"),
                        measurements.get("head_offset"),
                        "|".join(issues),
                    ]
                )

                log_file.flush()
                last_log_time = now

            if status == "INCORRECT" and bad_posture_seconds >= AUTO_SCREENSHOT_SECONDS:
                if now - last_auto_screenshot_time >= AUTO_SCREENSHOT_SECONDS:
                    filename = save_screenshot(display_frame, status, mode, "auto")
                    saved_message = f"Auto saved: {filename.name}"
                    saved_message_until = time.time() + 2.5
                    last_auto_screenshot_time = now

            cv2.imshow("Offline Posture Detection", display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("f"):
                mode_index = (mode_index + 1) % len(FILTER_MODES)

            if key == ord("s"):
                filename = save_screenshot(display_frame, status, mode, "manual")
                saved_message = f"Saved: {filename.name}"
                saved_message_until = time.time() + 2.5

            if key in (ord("q"), 27):
                break

    finally:
        log_file.close()
        print(f"Session log saved to: {log_filename}")

        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
