import os
import cv2
import torch
import pandas as pd
from PIL import Image
import numpy as np

# Define paths
DATASET_PATH = "C:/AgiCode/AI Training Facility/exp24/weights/best.pt"  # Your custom model
CSV_FILE = "detections.csv"  # CSV file to store detections

# Load the custom YOLOv5 model
print("Loading YOLOv5 model...")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=DATASET_PATH)
model.eval()  # Set model to evaluation mode
print("Model loaded successfully.")

# Confidence threshold and non-maximum suppression (NMS) IoU threshold
CONF_THRESHOLD = 0.3  # Lower confidence threshold to detect smaller/far objects
NMS_IOU_THRESHOLD = 0.5  # Slightly increase IoU threshold for better detection separation

# Create an empty DataFrame for detections if CSV does not exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Class", "X1", "Y1", "X2", "Y2", "Confidence"])
    df.to_csv(CSV_FILE, index=False)

def save_detection_to_csv(label, x1, y1, x2, y2, conf):
    # Append new detections to the CSV file
    new_data = pd.DataFrame([[label, x1, y1, x2, y2, conf]], 
                            columns=["Class", "X1", "Y1", "X2", "Y2", "Confidence"])
    
    # Read existing data (to avoid duplicates if needed)
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_existing = pd.concat([df_existing, new_data], ignore_index=True)
    else:
        df_existing = new_data
    
    # Save the updated table
    df_existing.to_csv(CSV_FILE, index=False)

# Function to perform detection and print bounding box coordinates with additional features
def detect_and_print(frame):
    try:
        # Convert OpenCV image (BGR) to PIL image (RGB)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Perform detection
        results = model(image)
        detections = results.xyxy[0]  # Get detections
        
        if detections is not None and len(detections) > 0:
            detections = detections.cpu().numpy()  # Move to CPU and convert to numpy
            
            # Filter out detections based on confidence threshold
            filtered_detections = [d for d in detections if d[4] >= CONF_THRESHOLD]
            if not filtered_detections:
                print("No objects detected above confidence threshold.")
                return
            
            # Apply Non-Maximum Suppression (NMS)
            boxes = np.array([[d[0], d[1], d[2], d[3]] for d in filtered_detections])
            scores = np.array([d[4] for d in filtered_detections])
            indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), CONF_THRESHOLD, NMS_IOU_THRESHOLD)
            
            print("Detected objects:")
            for i in indices.flatten():
                x1, y1, x2, y2, conf, cls = filtered_detections[i]
                label = model.names[int(cls)]  # Get class label from model
                print(f"{label}: (x1={x1:.2f}, y1={y1:.2f}, x2={x2:.2f}, y2={y2:.2f}), Confidence: {conf:.2f}")
                print("Pest Detected!")
                
                # Save detection to CSV
                save_detection_to_csv(label, x1, y1, x2, y2, conf)
                
                # Draw bounding boxes on the OpenCV frame with high-contrast colors
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            print("No objects detected.")
    
    except Exception as e:
        print(f"Error processing frame: {e}")

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting webcam feed. Press 'q' to exit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Resize frame to improve detection of small objects
    frame = cv2.resize(frame, (1280, 720))
    
    # Perform detection and overlay results on the frame
    detect_and_print(frame)
    
    # Show live detection feed
    cv2.imshow("Webcam Detection", frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting program.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Detection completed.")
