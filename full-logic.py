import cv2
import numpy as np
import os

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

def detect_obstruction_and_check_line(video_path, polygon_coords):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total number of frames: {total_frames}")

    obstruction_detected = False
    object_beyond_line = False

    # Convert the coordinates to a numpy array of integer points
    polygon = np.array(polygon_coords, np.int32)
    polygon = polygon.reshape((-1, 1, 2))

    # Loop through all the frames
    for frame_num in range(total_frames):
        ret, frame = video.read()

        if not ret:
            print(f"Error: Could not read frame {frame_num}.")
            continue

        # Create a mask with the same dimensions as the frame
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        # Fill the polygon on the mask
        cv2.fillPoly(mask, [polygon], 255)

        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the green color range in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        # Threshold the HSV image to get only green colors
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        # Apply the polygon mask to isolate the area of interest
        green_masked = cv2.bitwise_and(green_mask, green_mask, mask=mask)

        # Check for non-zero pixels within the polygon
        if cv2.countNonZero(green_masked) > cv2.countNonZero(mask):
            print(f"Obstruction detected in frame {frame_num}.")
            obstruction_detected = True

        # Find contours (objects)
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if any bounding box intersects with the green line
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            bbox = (x, y, w, h)
            
            if bbox_intersects_polygon(bbox, polygon):
                object_beyond_line = True
                break

        if object_beyond_line:
            break

    if obstruction_detected:
        print("Obstruction detected in the video.")
    else:
        print("No obstruction detected throughout the video.")
    
    if object_beyond_line:
        print("Object detected beyond the green line.")
    else:
        print("No object detected beyond the green line.")
    
    # Release the video capture object
    video.release()

# Coordinates of the green line polygon
# polygon_coords = [
#     [1086, 175], [1078, 449], [792, 718], [743, 715], 
#     [1055, 441], [1060, 191], [847, 6], [900, 8]
# ]
polygon_coords = [
    [210, 386], [505, 390], [626, 477], [593, 479], [509, 407], [209, 402], [120, 478], [90, 479]
]

# Replace 'your_video.mp4' with the path to your video file
video_path = 'b-side/b3.mp4'
detect_obstruction_and_check_line(video_path, polygon_coords)