1. Core Functionality
The project includes several key Python scripts that perform different tasks:


LoginInterface.py and custom_utility_suite.py: These scripts work together to create a graphical user interface (GUI) with a login and registration system. The main application, "Ultimate Utility Suite," has placeholder buttons for "Notes," "Tasks," and "Settings". User credentials are saved in 

users.json.


AIDetectionTest.py: This script performs real-time object detection from a webcam feed using a YOLOv5 model. When a pest or object is detected, it draws a bounding box around it, prints the class and confidence, and saves the detection data to a 

detections.csv file.



AiDatasetTest.py: This script is used to test a dataset of images. It processes all 

.jpg, .jpeg, and .png files in a specified input folder, performs object detection with a YOLOv5 model, and saves the images with bounding boxes drawn on them to an output folder named "output".


PythonToArduino: This script uses a YOLOv5 model to detect an object from a webcam feed. If an object is detected, it sends a '1' to an Arduino via serial communication; otherwise, it sends a '0'.


PaddyBotAI&Motor function: This script uses a YOLOv8 model to detect disease from a static image file. If a disease is detected, it sends the x-coordinate of the detection to an Arduino to control a motor function.

2. Prerequisites
To run the scripts, you will need the following:

Software: Python 3.x


Libraries: The Python scripts use several libraries, including torch, ultralytics, serial, cv2 (OpenCV), pandas, tkinter, Pillow (PIL), and hashlib. You will need to install these using pip, for example: 

pip install ultralytics torch pyserial opencv-python pandas pillow

Hardware: For the motor control scripts, you will need an Arduino board connected via USB. You will also need a webcam for real-time detection.


3. Getting Started
Place the files: Ensure all Python scripts, JSON files, CSV files, and executable files are in the same directory.

Install dependencies: Open your terminal or command prompt, navigate to the project directory, and run the pip command to install the required libraries.


Prepare your AI model: The detection scripts require a pre-trained model file (best.pt). The file paths in the scripts will need to be updated to match the location of your model file.

In 

PaddyBotAI&Motor function, set model = YOLO("best.pt") to the correct path.

In 

PythonToArduino and AiDatasetTest.py, update the path argument to point to your best.pt file.


Connect Arduino: If you plan to use the motor control functionality, connect your Arduino board and update the COM port in the scripts to match your system (e.g., COM3, COM4).

4. How to Use
Login System
To use the login interface, run 

custom_utility_suite.py:

Register: If you are a new user, enter a username and password and click Register. This will save your credentials to the 

users.json file.


Login: Enter your registered username and password and click Login to access the main utility suite.

Live Detection
To start the real-time detection from your webcam, run 

AIDetectionTest.py.

The script will display a live feed from your webcam.

Detected objects will have a bounding box drawn around them.

Detection data will be logged in 

detections.csv.


To exit, press the 

'q' key on your keyboard.

Dataset Testing
To test your AI model on a set of images, run 

AiDatasetTest.py.

Place your images in the folder specified by 

input_folder.

The script will create a new folder named "output" and save the processed images with bounding boxes there.

Motor Control

PythonToArduino: Run this script to make a simple ON/OFF motor control based on object detection. It sends a '1' to the Arduino if an object is present, and a '0' if not.


PaddyBotAI&Motor function: Run this script to send an x-coordinate to the Arduino based on the location of a detected disease in a static image.
