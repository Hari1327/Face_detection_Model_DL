import streamlit as st
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np

# Load the YOLO model
model = YOLO("best.pt")  # Make sure the path is correct to your model

# Function to perform face detection
def face_detection(uploaded_image):
    img_array = np.array(uploaded_image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Resize the image for YOLO input
    img_resized = cv2.resize(img_bgr, (640, 640))

    # Perform face detection
    results = model(img_resized, imgsz=640)

    # Draw bounding boxes and confidence scores
    for result in results:
        for box in result.boxes:
            x_min, y_min, x_max, y_max = box.xyxy[0].int().tolist()
            confidence = box.conf[0].item()
            cv2.rectangle(img_resized, (x_min, y_min), (x_max, y_max), (255, 0, 0), 3)
            label = f'Confidence: {confidence:.2f}'
            cv2.putText(img_resized, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img_resized

# The app function to be called in main.py
def app():
    st.title("Upload the image and Detect Faces")
    file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if file:
        image = Image.open(file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button("Detect Faces"):
            detected_image = face_detection(image)
            detected_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
            st.image(detected_image_rgb, caption='Detected Faces', use_column_width=True)
