# Overview
This project focuses on detecting driver drowsiness through a camera and sounding a buzzer when the driver starts to fall asleep. For additional security, it also sends an immediate message to a registered number. The system uses facial landmarks based drowsy driver detection implemented with OpenCV and dlib.

# Features
- Drowsiness Detection: Monitors the driver’s eyes and alerts when signs of drowsiness are detected.
- Real-Time Alerts: Sounds a buzzer to wake the driver.
- Emergency Messaging: Sends a message to a registered number if the driver is detected to be drowsy.
- Facial Landmarks: Utilizes advanced facial landmarks detection for accurate monitoring.
  
# How It Works
The system uses a camera to capture the driver’s face and analyzes the eye aspect ratio (EAR) to determine if the driver is drowsy. OpenCV is used for image processing, and DLib is used for detecting facial landmarks. When drowsiness is detected, the system sounds a buzzer and sends an emergency message to a pre-registered phone number.

# License
This project is licensed under the MIT License. See the LICENSE file for details.
