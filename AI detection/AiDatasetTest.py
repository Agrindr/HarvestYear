import os
import torch
from PIL import Image, ImageDraw
from torchvision import transforms

# Define paths
dataset_path = "C:/Users/agina/Downloads/exp10/weights/best.pt"  # Your custom model
input_folder = "C:/Users/agina/Downloads/Rice Leaf.v2i.yolov5pytorch/valid/images"  # Your input folder
output_folder = "output"  # Output folder in the workspace

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the custom YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=dataset_path)
model.eval()  # Set model to evaluation mode

# Function to perform detection and save results
def detect_and_save(image_path, output_path):
    try:
        # Load image
        image = Image.open(image_path).convert("RGB")
        
        # Perform detection
        results = model(image)
        
        # Parse results
        detections = results.xyxy[0]  # Get detections
        if detections is not None and len(detections) > 0:
            detections = detections.cpu().numpy()  # Move to CPU and convert to numpy
            
            # Draw bounding boxes on the image
            draw = ImageDraw.Draw(image)
            for detection in detections:
                x1, y1, x2, y2, conf, cls = detection
                label = model.names[int(cls)]  # Get class label from model
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)  # Draw bounding box
                draw.text((x1, y1), f"{label} {conf:.2f}", fill="red")  # Add label and confidence score
        
        # Save the output image
        image.save(output_path)
        print(f"Processed and saved: {output_path}")
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Scan the input folder for images
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
if not image_files:
    print("No images found in the input folder.")
else:
    for filename in image_files:
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)
        
        # Perform detection and save the result
        detect_and_save(input_image_path, output_image_path)

print("Detection completed. Check the output folder for results.")