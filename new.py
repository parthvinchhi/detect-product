import cv2
import numpy as np
import os

# Function to detect green lines in the image
def detect_green_lines(image):
    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range for green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    
    # Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Find contours on the green mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

# Function to check if an image is blocking any detected green line
def check_line_blockage(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image {image_path}")
        return
    
    # Detect green lines in the image
    green_lines = detect_green_lines(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Create an empty mask
    mask = np.zeros_like(edges)
    
    # Draw the green lines on the mask
    for contour in green_lines:
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
    
    # Check if any edge intersects with the green lines
    intersection = cv2.bitwise_and(edges, mask)
    
    # Check if there's any white pixel in the intersection (indicating blockage)
    if np.any(intersection):
        print(f"{os.path.basename(image_path)}: Cart is 80% full")
    else:
        print(f"{os.path.basename(image_path)}: Cart not full")

# Process all images in the folder
image_folder = "b-side-frames"
for image_name in os.listdir(image_folder):
    if image_name.endswith('.png') or image_name.endswith('.jpg'):
        image_path = os.path.join(image_folder, image_name)
        check_line_blockage(image_path)
