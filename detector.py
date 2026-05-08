"""Camera pose detection using MediaPipe."""

import cv2


class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        try:
            from mediapipe.python.solutions import pose as mp_pose
            from mediapipe.python.solutions import drawing_utils as mp_drawing
        except ImportError as exc:
            raise RuntimeError(
                "MediaPipe is not installed correctly. Run: pip install mediapipe"
            ) from exc

        self.mp_pose = mp_pose
        self.mp_drawing = mp_drawing

        self.pose = self.mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self.pose.process(rgb)
        rgb.flags.writeable = True
        return results

    def extract_landmarks(self, frame, results):
        h, w = frame.shape[:2]

        if not results.pose_landmarks:
            return {}

        lm = results.pose_landmarks.landmark
        pose = self.mp_pose.PoseLandmark

        def point(name):
            landmark = lm[getattr(pose, name).value]

            if landmark.visibility < 0.45:
                return None

            return int(landmark.x * w), int(landmark.y * h)

        return {
            "nose": point("NOSE"),
            "left_ear": point("LEFT_EAR"),
            "right_ear": point("RIGHT_EAR"),
            "left_shoulder": point("LEFT_SHOULDER"),
            "right_shoulder": point("RIGHT_SHOULDER"),
            "left_hip": point("LEFT_HIP"),
            "right_hip": point("RIGHT_HIP"),
        }

    def draw_pose(self, frame, results):
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )

        return frame

    def close(self):
        self.pose.close()
