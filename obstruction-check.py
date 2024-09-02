import cv2
import numpy as np

def detect_obstruction(video_path, polygon_coords):
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
            break

    if not obstruction_detected:
        print("No obstruction detected throughout the video.")

    # Release the video capture object
    video.release()

# Coordinates of the green line polygon
polygon_coords = [
    [1243, 91], [1225, 649], [1050, 719], [982, 719], 
    [1186, 647], [1206, 106], [597, 6], [785, 6]
]

# Replace 'your_video.mp4' with the path to your video file
video_path = 'b-side/b3.mp4'
detect_obstruction(video_path, polygon_coords)
