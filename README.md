# :rocket: Real-time Object Measurement with Camera Calibration

# Introduction
This project provides a real-time object measurement solution using cameras and traditional computer vision techniques (contour detection) enhanced with camera calibration. This calibration is important for correcting lens distortion, ensuring measurement accuracy across frames. Measurement results are displayed in meters (m).

The system works by detecting a reference object with known physical dimensions (e.g. an ID card or other rectangular object) in each frame. A pixels per millimeter ratio (pixels_per_mm) is then calculated from this reference object, and used to convert the pixel dimensions of other detected objects into real-world physical sizes.

Key Features of Camera Calibration: Uses the ChArUco pattern to obtain the camera's intrinsic parameters and distortion coefficients, which enables correction of lens distortion in the video frame. Real-time Measurement: Capable of detecting and measuring object dimensions directly from the camera feed. Dynamic Reference Object: Uses a reference object with known physical dimensions to dynamically determine the measurement scale (pixels to millimeters) in each frame. Output in Meters: Object width and height measurement results are displayed in meters. Pure OpenCV: OpenCV-based implementation with no additional deep learning model training required (such as YOLO).

# 📽️Project Structure📽️

├── utlis.py       # Skrip untuk melakukan kalibrasi kamera

├── Objectmeasurement.py        

├── assets/                   #optional

│   └── charuco_board.png

└── README.md                 

# 🎶System Requirements
- Python 3.x
- Camera (webcam or external camera)
- Reference object with known physical dimensions (e.g. ID card)
- Development environment (VS Code recommended)

# 🖥️Installation
Clone Repository:

Create a Virtual Environment (Recommended):

python -m venv venv
##  On Windows:
.\venv\Scripts\activate
##  On macOS/Linux:
source venv/bin/activate

Install Dependencies:

pip install opencv-python numpy

Real-Time Object Measurement with Camera Calibration


# Measurement Workflow
## - Image Undistortion: 
Each frame from the camera is first undistorted using the camera_matrix and dist_coeffs obtained from calibration. This removes the "warping" effect of the lens.
## - Contour Detection: 
The undistorted image is then processed (grayscale, blur, Canny edge detection) to find the contours of the object.
## - Reference Object Identification: 
The script searches for a rectangular contour whose aspect ratio and size are closest to the reference object for which you have specified dimensions.
Scale Determination (Pixels to Millimeters): Once the reference object is detected, the pixels_per_mm ratio is calculated by dividing the pixel dimensions of the reference object by its millimeter physical dimensions. This ratio is dynamic for each frame as the distance of the object to the camera may vary.
## - Measurement of Other Objects: 
Other detected rectangular contours (other than the reference object) are then measured. Its pixel dimensions are divided by pixels_per_mm to get the size in millimeters.
## - Conversion to Meters: 
The result in millimeters is then divided by 1000 to be displayed in meters.
Limitations and Potential Improvements
## - Planar Assumption: 
The best accuracy is achieved when the reference object and the measured object are on a relatively flat plane and parallel to the camera image plane. Objects that are far away or highly tilted will have degraded accuracy.
Simple Contour Detection: 
Simple contour detection methods may struggle in complex environments, with poor lighting, or if there are many similar objects that can be confusing.
## - Robustness: 
The identification of the reference object and the object to be measured currently depends on aspect ratio and area. This can be improved by using segmentation techniques or deep learning-based object detection (such as YOLO) after the undistortion process.
## - Offline Calibration: 
Camera calibration is performed offline. For scenarios where the camera may move significantly, systems that monitor the camera pose in real-time (e.g. with ArUco marker tracking) can improve accuracy.
