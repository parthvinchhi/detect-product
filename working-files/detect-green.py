import cv2
import numpy as np

# Convert hex color code to BGR
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return tuple(reversed(rgb))  # OpenCV uses BGR format

# Convert hex color code to HSV
def hex_to_hsv(hex_color):
    bgr_color = hex_to_bgr(hex_color)
    bgr_color = np.uint8([[bgr_color]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

# Path to the input video
video_path = 'b-side/b1.mp4'

# Output file names
output_contoured_frame = 'contoured_frame.png'
output_cropped_frame = 'cropped_frame.png'

# Hex color code
hex_color = '#256658'
hsv_color = hex_to_hsv(hex_color)

# Define color range in HSV
def get_color_range(hsv_color, tolerance=10):
    lower_bound = np.array([hsv_color[0] - tolerance, 50, 50])
    upper_bound = np.array([hsv_color[0] + tolerance, 255, 255])
    return lower_bound, upper_bound

def detect_color(frame, lower_bound, upper_bound):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Find contours of the colored regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("Color not detected.")
        return None, None
    
    # Draw contours on the frame
    contoured_frame = frame.copy()
    cv2.drawContours(contoured_frame, contours, -1, (0, 255, 0), 2)
    
    # Create a mask with the colored regions
    mask = np.zeros_like(frame)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
    
    # Apply the mask to the frame
    masked_frame = cv2.bitwise_and(frame, mask)
    
    # Get bounding box of the colored regions
    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    cropped_frame = masked_frame[y:y+h, x:x+w]
    
    return contoured_frame, cropped_frame

def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error opening video file.")
        return
    
    # Move to the last frame
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    
    # Read the last frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the video frame.")
        cap.release()
        return
    
    # Get the color range
    lower_bound, upper_bound = get_color_range(hsv_color)
    
    # Detect color and crop image
    contoured_frame, cropped_frame = detect_color(frame, lower_bound, upper_bound)
    
    if contoured_frame is not None and cropped_frame is not None:
        # Save the contoured frame
        cv2.imwrite(output_contoured_frame, contoured_frame)
        
        # Save the cropped frame
        cv2.imwrite(output_cropped_frame, cropped_frame)
        
        print(f"Frames saved: \n- Contoured Frame: '{output_contoured_frame}' \n- Cropped Frame: '{output_cropped_frame}'")
    else:
        print("Could not process the color.")
    
    # Release the video capture object
    cap.release()

# Run the video processing
process_video(video_path)
