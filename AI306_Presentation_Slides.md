# Presentation: Real-Time Posture Detection and Feedback System

## Slide 1: Title

**Real-Time Posture Detection and Feedback System Using Image Processing and Computer Vision**

AI306 Image Processing  
Student: Sandra  

Speaker notes:  
This project detects sitting posture using a webcam and gives real-time feedback to the user.

## Slide 2: Problem

- Many students sit for long periods.
- Bad posture can cause neck, shoulder, and back discomfort.
- The goal is to monitor posture automatically using computer vision.

Speaker notes:  
The problem is practical and related to real daily computer use.

## Slide 3: Project Idea

- Use a webcam as input.
- Process each video frame.
- Detect body landmarks.
- Calculate posture measurements.
- Classify posture.
- Display feedback and save results.

Speaker notes:  
The system is not only a filter. It is a full input-processing-output pipeline.

## Slide 4: System Pipeline

```text
Camera
-> Image preprocessing
-> Pose detection
-> Landmark extraction
-> Measurement calculation
-> Classification
-> Feedback and logging
```

Speaker notes:  
This pipeline satisfies the course requirement for a complete processing system.

## Slide 5: Image-Processing Techniques

- Gaussian blur
- Contrast enhancement
- Histogram equalization
- Canny edge detection
- Sobel edge detection
- Laplacian edge detection
- FFT spectrum
- Contours
- SIFT / ORB keypoints

Speaker notes:  
These techniques are connected to the course lectures on edge detection, frequency domain, contours, and features.

## Slide 6: Pose and Measurements

The system extracts:

- Shoulders
- Hips
- Ears
- Nose

Then calculates:

- Neck angle
- Trunk angle
- Shoulder tilt
- Head offset

Speaker notes:  
These measurements are interpretable, so the system is not only a black box.

## Slide 7: Classification and Score

| Score | Status | Risk |
|---|---|---|
| 80-100 | Correct | Low |
| 55-79 | Warning | Medium |
| 0-54 | Incorrect | High |

Speaker notes:  
The posture score makes the result easy to understand.

## Slide 8: Result Example - Unknown

Image: `screenshots/posture_20260429_170229_unknown_normal_manual.png`

- Body is not fully visible.
- System cannot classify posture confidently.
- This is a limitation case.

Speaker notes:  
This shows that the system handles missing information by returning unknown instead of giving a wrong result.

## Slide 9: Result Example - Canny Mode

Image: `screenshots/posture_20260429_170437_warning_canny_manual.png`

- Canny edge detection is applied.
- Posture is classified as warning.
- Score and risk are displayed.

Speaker notes:  
This connects the demo directly to the edge detection lecture.

## Slide 10: Result Example - Incorrect Posture

Image: `screenshots/posture_20260429_170503_incorrect_histogram_auto.png`

- User is leaning.
- System shows incorrect posture.
- Feedback suggests posture correction.

Speaker notes:  
The result is interpretable because it includes score, risk, angles, and text feedback.

## Slide 11: Analysis Outputs

The system saves:

- Screenshots
- CSV session logs
- Score over time chart
- Risk distribution chart
- Summary text file

Speaker notes:  
These outputs support the report results and analysis section.

## Slide 12: Testing Scenarios

- Correct sitting posture
- Forward head posture
- Leaning forward
- Uneven shoulders
- Poor lighting
- Partial body visibility
- Side view
- Background clutter

Speaker notes:  
Testing different scenarios shows robustness and limitations.

## Slide 13: Strengths

- Real-time system.
- Uses real webcam data.
- Works locally without paid API.
- Includes many image-processing modes.
- Gives visual feedback and measurable results.
- Modular code structure.

Speaker notes:  
The system is practical and complete.

## Slide 14: Limitations

- Needs the upper body visible.
- Side view can reduce accuracy.
- Extra people in frame may confuse landmarks.
- Lighting and camera distance affect detection.
- MediaPipe is a prebuilt pose model.

Speaker notes:  
The main contribution is the integrated pipeline, scoring, feedback, and analysis, not training a new pose model.

## Slide 15: Conclusion

- The project solves a clear computer vision problem.
- It uses multiple image-processing techniques.
- It provides real-time classification and feedback.
- It produces visual and analytical results.

Speaker notes:  
The project satisfies the AI306 requirements because it includes a complete pipeline, meaningful application, and supporting analysis.

## Slide 16: Demo Plan

1. Run `python main.py`.
2. Show normal posture.
3. Press `F` to show filters.
4. Show Canny, Sobel, FFT, contours, and features.
5. Show incorrect posture.
6. Press `S` to save screenshot.
7. Run `python analyze_results.py`.
8. Show generated charts.

Speaker notes:  
This demo order makes the system clear and shows both technical image processing and application output.
