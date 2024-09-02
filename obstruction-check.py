import cv2
import numpy as np

def visualize_polygon_mask(frame, polygon_coords):
    # Convert the coordinates to a numpy array of integer points
    polygon = np.array(polygon_coords, np.int32)
    polygon = polygon.reshape((-1, 1, 2))

    # Create a mask with the same dimensions as the frame
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    # Fill the polygon on the mask
    cv2.fillPoly(mask, [polygon], 255)

    # Apply the mask to the frame to visualize it
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the masked frame
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Polygon Mask', mask)
    cv2.imshow('Masked Frame', masked_frame)
    cv2.waitKey(0)  # Wait for a key press to proceed

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

    # Loop through all the frames
    for frame_num in range(total_frames):
        ret, frame = video.read()

        if not ret:
            print(f"Error: Could not read frame {frame_num}.")
            continue

        # Visualize the polygon mask on the first frame for debugging
        if frame_num == 0:
            visualize_polygon_mask(frame, polygon_coords)

        # Convert the coordinates to a numpy array of integer points
        polygon = np.array(polygon_coords, np.int32)
        polygon = polygon.reshape((-1, 1, 2))

        # Create a mask with the same dimensions as the frame
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        # Fill the polygon on the mask
        cv2.fillPoly(mask, [polygon], 255)

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply the mask to the grayscale frame
        masked_frame = cv2.bitwise_and(gray_frame, gray_frame, mask=mask)

        # Threshold the masked grayscale image to create a binary image
        _, thresh_frame = cv2.threshold(masked_frame, 50, 255, cv2.THRESH_BINARY)

        # Check for any non-white pixels (indicating an obstruction) in the thresholded image
        if np.any(thresh_frame == 0):  # 0 indicates obstruction
            print(f"Obstruction detected in frame {frame_num}.")
            obstruction_detected = True
            break

    if not obstruction_detected:
        print("No obstruction detected throughout the video.")

    # Release the video capture object and close windows
    video.release()
    cv2.destroyAllWindows()

# Coordinates of the green line polygon
polygon_coords = [
    [1086, 175], [1078, 449], [792, 718], [743, 715], [1055, 441], [1060, 191], [847, 6], [900, 8]
]

# Replace 'your_video.mp4' with the path to your video file
video_path = 'a-side/a1.mp4'
detect_obstruction(video_path, polygon_coords)
