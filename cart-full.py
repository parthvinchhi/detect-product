import cv2
import numpy as np

# Define the green line using the provided coordinates
green_line_coords = np.array([[210, 386], [505, 390], [626, 477], [593, 479], 
                              [509, 407], [209, 402], [120, 478], [90, 479]])

# Initialize video capture
cap = cv2.VideoCapture('b6.mp4')  # Replace with your video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale (optional, depending on your detection method)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Simple thresholding to detect objects (you can replace this with a more sophisticated method)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours (objects)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through contours to find objects above the green line
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        object_center = (x + w // 2, y + h // 2)

        # Check if the object's center is inside the green line polygon
        if cv2.pointPolygonTest(green_line_coords, object_center, False) >= 0:
            print('Cart is 80% full')
            break  # Stop after detecting the first object that crosses the line

    # Optionally, draw the green line on the frame (for visualization)
    cv2.polylines(frame, [green_line_coords], isClosed=True, color=(0, 255, 0), thickness=2)

    # Display the frame (optional for debugging)
    # cv2.imshow('Frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# Release resources
cap.release()
cv2.destroyAllWindows()
