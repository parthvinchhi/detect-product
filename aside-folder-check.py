import cv2
import numpy as np
import os

# Define the green line using the provided coordinates
green_line_coords = np.array([[612, 106], [608, 301], [420, 478], [389, 479], [594, 298], [599, 114], [458, 3], [487, 2]])

def line_intersect(p1, p2, p3, p4):
    """ Check if line segments (p1p2) and (p3p4) intersect """
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4))

def bbox_edges(bbox):
    """ Get the edges of the bounding box """
    x, y, w, h = bbox
    return [
        ((x, y), (x + w, y)),
        ((x + w, y), (x + w, y + h)),
        ((x + w, y + h), (x, y + h)),
        ((x, y + h), (x, y))
    ]

def process_video(video_path):
    # Initialize video capture
    cap = cv2.VideoCapture(video_path) 

    # Check if the video was successfully opened
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Set the video capture to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # Read the last frame
    ret, frame = cap.read()
    # cv2.imshow('Frame', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Check if the frame was successfully read
    if not ret:
        print(f"Error reading the last frame of video: {video_path}")
        cap.release()
        return

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Simple thresholding to detect objects
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours (objects)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a polygon for the green line
    green_polygon = green_line_coords.reshape((-1, 2))
    
    # Check if any bounding box intersects with the green line
    object_beyond_line = False

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bbox = (x, y, w, h)
        
        bbox_edges_list = bbox_edges(bbox)
        for edge in bbox_edges_list:
            for i in range(len(green_polygon)):
                next_i = (i + 1) % len(green_polygon)
                if line_intersect(edge[0], edge[1], green_polygon[i], green_polygon[next_i]):
                    object_beyond_line = True
                    break
            if object_beyond_line:
                break
        if object_beyond_line:
            break

    # Print the result
    if object_beyond_line:
        print(f'{video_path}: Cart is 80% full')
    else:
        print(f'{video_path}: No product is beyond the line')

    # Release resources
    cap.release()

# Directory containing video files
video_directory = 'a-side'  # Replace with the path to your directory

# Process each video in the directory
for filename in os.listdir(video_directory):
    if filename.endswith('.mp4'):  # Adjust if your video files have different extensions
        video_path = os.path.join(video_directory, filename)
        process_video(video_path)
