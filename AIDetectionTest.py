import os
import cv2
import torch
from PIL import Image, ImageDraw
import numpy as np

# Define paths
dataset_path = "C:/AgiCode/AI Training Facility/exp24/weights/best.pt"  # Your custom model
output_folder = "output"  # Output folder in the workspace

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the custom YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=dataset_path)
model.eval()  # Set model to evaluation mode

def detect_and_save(frame, frame_count):
    try:
        # Convert OpenCV image (BGR) to PIL image (RGB)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Perform detection
        results = model(image)
        detections = results.xyxy[0]  # Get detections
        
        if detections is not None and len(detections) > 0:
            detections = detections.cpu().numpy()  # Move to CPU and convert to numpy
            draw = ImageDraw.Draw(image)
            
            for detection in detections:
                x1, y1, x2, y2, conf, cls = detection
                label = model.names[int(cls)]  # Get class label from model
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
                draw.text((x1, y1), f"{label} {conf:.2f}", fill="red")
            
            # Save the output image if objects are detected
            output_path = os.path.join(output_folder, f"detection_{frame_count}.jpg")
            image.save(output_path)
            print(f"Detection saved: {output_path}")
    
    except Exception as e:
        print(f"Error processing frame: {e}")

# Open webcam
cap = cv2.VideoCapture(0)
frame_count = 0

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Show live webcam feed
    cv2.imshow("Webcam Detection", frame)
    
    # Perform detection and save frame if something is detected
    detect_and_save(frame, frame_count)
    frame_count += 1
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Detection completed.")
