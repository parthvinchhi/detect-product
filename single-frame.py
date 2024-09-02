import cv2
import numpy as np

# Define the green line using the provided coordinates
# green_line_coords = np.array([[210, 386], [505, 390], [626, 477], [593, 479], 
#                               [509, 407], [209, 402], [120, 478], [90, 479]], dtype=np.int32)

# green_line_coords = np.array([[1243, 91], [1225, 649], [1050, 719], [982, 719], 
#                               [1186, 647], [1206, 106], [597, 6], [785, 6]], dtype=np.int32)

green_line_coords = np.array([[1086, 175], [1078, 449], [792, 718], [743, 715], 
                              [1055, 441], [1060, 191], [847, 6], [900, 8]], dtype=np.int32)

# Initialize video capture
cap = cv2.VideoCapture('a-side/a2.mp4')  # Replace with your video file

# Check if the video was successfully opened
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Set the video capture to the last frame
cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

# Read the last frame
ret, frame = cap.read()

# Check if the frame was successfully read
if not ret:
    print("Error reading the last frame")
    cap.release()
    exit()

# Convert frame to grayscale (optional, depending on your detection method)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Simple thresholding to detect objects (you can replace this with a more sophisticated method)
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find contours (objects)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a mask to draw the green line polygon
mask = np.zeros_like(gray)
cv2.fillPoly(mask, [green_line_coords], 255)

# Create a flag to indicate if any object intersects with the green line
object_beyond_line = False

# Function to check if any part of the rectangle overlaps with the polygon
def rect_intersects_polygon(rect, mask):
    x, y, w, h = rect
    roi = mask[y:y+h, x:x+w]
    
    # Check if any part of the ROI intersects with the polygon mask
    if np.any(roi > 0):  # Check if there are any non-zero values
        return True
    return False

# Check for intersections in the last frame
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    rect = (x, y, w, h)

    # Check if the bounding rectangle of the object intersects with the green line polygon
    if rect_intersects_polygon(rect, mask):
        object_beyond_line = True
        break

# Print the result
if object_beyond_line:
    print('Cart is 80% full')
else:
    print('No product is beyond the line')

# Release resources
cap.release()
