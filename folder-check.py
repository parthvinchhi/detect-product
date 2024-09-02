import cv2
import numpy as np
import os

# Define the green line using the provided coordinates
# green_line_coords = np.array([[210, 386], [505, 390], [626, 477], [593, 479], 
#                               [509, 407], [209, 402], [120, 478], [90, 479]], dtype=np.int32)
green_line_coords = np.array([[1243, 91], [1225, 649], [1050, 719], [982, 719], 
                              [1186, 647], [1206, 106], [597, 6], [785, 6]], dtype=np.int32)


def line_intersect(p1, p2, p3, p4):
    """ Check if line segments (p1p2) and (p3p4) intersect """
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4))

def bbox_intersects_polygon(bbox, polygon):
    """ Check if a bounding box intersects with a polygon """
    x, y, w, h = bbox
    bbox_polygon = np.array([
        [x, y],
        [x + w, y],
        [x + w, y + h],
        [x, y + h]
    ], dtype=np.int32)

    # Convert polygon to the correct format
    polygon = polygon.reshape((-1, 1, 2))

    # Check if any bbox edge intersects with the polygon edges
    for i in range(len(bbox_polygon)):
        for j in range(len(polygon)):
            next_j = (j + 1) % len(polygon)
            if line_intersect(tuple(bbox_polygon[i]), tuple(bbox_polygon[(i + 1) % len(bbox_polygon)]),
                              tuple(polygon[j][0]), tuple(polygon[next_j][0])):
                return True

    # Check if any bbox point is inside the polygon
    for point in bbox_polygon:
        point = tuple(map(int, point))  # Ensure point is a tuple of integers
        if cv2.pointPolygonTest(polygon, point, False) >= 0:
            return True

    return False

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
    green_polygon = green_line_coords.reshape((-1, 1, 2))

    # Check if any bounding box intersects with the green line
    object_beyond_line = False

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bbox = (x, y, w, h)
        
        if bbox_intersects_polygon(bbox, green_polygon):
            object_beyond_line = True
            break

    # Print the result
    if object_beyond_line:
        print(f'{video_path}: Cart is 80% full')
    else:
        print(f'{video_path}: No product is beyond the line')

    # Release resources
    cap.release()

# Directory containing video files
video_directory = 'b-side'  # Replace with the path to your directory

# Process each video in the directory
for filename in os.listdir(video_directory):
    if filename.endswith('.mp4'):  # Adjust if your video files have different extensions
        video_path = os.path.join(video_directory, filename)
        process_video(video_path)
