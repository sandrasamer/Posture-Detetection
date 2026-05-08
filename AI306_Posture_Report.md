# Real-Time Posture Detection and Feedback System Using Image Processing and Computer Vision

## 1. Problem Definition

Poor sitting posture is a common problem for students and computer users. Long periods of sitting with a forward head, rounded shoulders, leaning trunk, or uneven shoulders can cause discomfort in the neck, shoulders, and back. The goal of this project is to design and implement a real-time computer vision system that monitors sitting posture using a webcam and gives immediate visual feedback to the user.

The system processes live camera frames, applies image-processing techniques, detects human body landmarks, calculates posture-related measurements, classifies the posture, and displays feedback. The project is related to image processing and computer vision because it works on real image data and includes preprocessing, edge detection, feature visualization, pose estimation, measurement extraction, and visual output.

## 2. Project Objectives

The objectives of the project are:

- To process real-time webcam frames.
- To apply different image-processing techniques such as Gaussian blur, contrast enhancement, histogram equalization, Canny edge detection, Sobel, Laplacian, FFT spectrum, contours, and feature/keypoint detection.
- To detect body landmarks using a computer vision pose estimation method.
- To calculate meaningful posture measurements such as neck angle, trunk angle, shoulder tilt, and head offset.
- To classify posture into correct, warning, incorrect, or unknown.
- To provide visual feedback, posture score, risk level, screenshots, and CSV logs for analysis.

## 3. Recent Applied Methodologies

Several methods can be used to solve posture detection problems:

1. Manual image-processing methods  
   Traditional methods may use thresholding, edges, contours, and geometric measurements to detect body shape. These methods are interpretable but may fail when lighting, background, or clothing changes.

2. Feature-based computer vision  
   Techniques such as HOG, SIFT, ORB, contours, and keypoints can describe image regions and body structure. These methods are useful for analysis and visualization, but full human posture detection is difficult using only handcrafted features.

3. Machine learning classification  
   A model can be trained on posture examples and classify each frame as correct or incorrect. This requires a labeled dataset and training process.

4. Pose estimation methods  
   Modern systems can detect human body landmarks, then use geometric rules or classifiers to analyze posture. This project follows this approach because landmark positions make posture measurements more interpretable.

## 4. Proposed Solution and Added Value

The proposed system is a real-time posture detection application that works locally without a paid API or cloud subscription. The system uses the webcam as input and gives immediate feedback on the video frame.

The added value of this project is the integration of multiple image-processing and computer vision components into one complete system:

- Live camera input.
- Multiple preprocessing and analysis modes.
- Pose landmark detection.
- Angle and offset measurements.
- Rule-based posture scoring.
- Risk-level classification.
- Feedback messages.
- Screenshot saving.
- CSV session logging.
- Automatic results analysis and charts.

This makes the project more than a simple filter or isolated operation. It is a complete pipeline from input to processing to output.

## 5. System Pipeline

The processing pipeline is:

```text
Webcam input
-> Frame preprocessing / analysis mode
-> Pose landmark detection
-> Landmark extraction
-> Neck, trunk, shoulder, and head measurements
-> Posture score calculation
-> Status and risk classification
-> Visual feedback and report logging
```

## 6. Image-Processing Techniques Used

The application includes the following image-processing modes:

| Mode | Purpose |
|---|---|
| Normal | Shows the original camera frame. |
| Gaussian Blur | Reduces noise in the image. |
| Contrast Enhancement | Improves frame visibility. |
| Histogram Equalization | Enhances brightness distribution. |
| Canny Edge Detection | Shows strong edges in the scene. |
| Sobel Edge Detection | Calculates gradient-based edges. |
| Laplacian Edge Detection | Detects rapid intensity changes. |
| FFT Spectrum | Shows frequency-domain representation. |
| Contours | Extracts object boundaries from edges. |
| Features | Shows SIFT keypoints if available, otherwise ORB keypoints. |

These modes connect the project with the course topics, especially edge detection, frequency domain filtering, contours, and feature detection.

## 7. Posture Measurements

The system uses detected landmarks such as shoulders, hips, ears, and nose. From these points, the following measurements are calculated:

- Neck angle: used to detect neck bending.
- Trunk angle: used to detect forward leaning.
- Shoulder tilt: used to detect imbalance between left and right shoulders.
- Head offset: used to detect forward head posture.

The system then calculates a score from 0 to 100. A higher score means better posture.

| Score Range | Status | Risk Level |
|---|---|---|
| 80-100 | Correct | Low |
| 55-79 | Warning | Medium |
| 0-54 | Incorrect | High |

## 8. Results and Visual Outputs

The application produces visual results directly on the camera frame. The displayed information includes:

- Posture status.
- Feedback message.
- Angle table.
- Posture score.
- Risk level.
- Bad posture duration.
- Session average score.
- Current image-processing mode.

Example result screenshots:

1. Unknown posture case  
   `screenshots/posture_20260429_170229_unknown_normal_manual.png`  
   This shows a limitation case where the full body is not visible enough for complete posture classification.

2. Warning posture with Canny edge detection  
   `screenshots/posture_20260429_170437_warning_canny_manual.png`  
   This shows course-related edge detection while still performing posture analysis.

3. Incorrect posture with histogram mode  
   `screenshots/posture_20260429_170503_incorrect_histogram_auto.png`  
   This shows an incorrect posture case with high risk and low score.

4. Difficult side-view case  
   `screenshots/posture_20260429_170511_incorrect_histogram_auto.png`  
   This shows a difficult case where side view and extra visible person parts can affect landmark stability.

The system also generates result charts:

- `results/score_over_time.png`
- `results/risk_distribution.png`
- `results/summary.txt`

## 9. Testing Scenarios

The system should be tested using the following scenarios:

| Scenario | Expected Result |
|---|---|
| Full body visible and sitting straight | Correct / high score |
| Head moved forward | Warning or incorrect |
| Leaning forward | Incorrect / lower score |
| Uneven shoulders | Warning or incorrect |
| Poor lighting | May reduce detection quality |
| Body partially outside frame | Unknown or lower confidence |
| Side view | Less stable landmark detection |
| Background clutter / another person appears | Possible landmark confusion |

## 10. Discussion

The results show that the system can detect posture problems and provide interpretable feedback. The use of image-processing modes makes the system connected to course topics and helps visualize how different processing techniques affect the input image.

The most important strength of the system is that it is real-time and local. It does not require a paid AI API or cloud service. The posture score and risk level make the output easy to understand. The screenshots and CSV logs also help in analysis and reporting.

However, the system has limitations. If the full upper body is not visible, the system may return unknown. If the user is in a side pose, landmarks can become less stable. If another person appears in the frame, the pose detector may become confused. Lighting and camera position also affect performance.

## 11. Conclusion

This project presents a complete real-time posture detection and feedback system using image processing and computer vision. The system processes real webcam data, applies multiple course-related image-processing techniques, detects pose landmarks, extracts posture measurements, classifies posture, and provides feedback and analysis outputs.

The project satisfies the AI306 requirements because it has a clear problem, real image data, a complete pipeline, multiple techniques, visual outputs, and supporting analysis. Future work could include collecting a labeled dataset, training a custom posture classifier, adding multi-person filtering, and improving side-view robustness.

## 12. Notes Before Final Submission

Before submitting, record one clean session with:

- One correct posture screenshot.
- One warning posture screenshot.
- One incorrect posture screenshot.
- One image-processing mode screenshot.
- One limitation screenshot.

Then run:

```powershell
python analyze_results.py
```

Use the updated charts and summary in the final report.
