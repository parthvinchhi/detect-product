import cv2
import numpy as np

# Coordinates of the polygon
# polygon_coords = np.array([
#     [1243, 91], [1225, 649], [1050, 719], [982, 719], [1186, 647], [1206, 106], [597, 6], [785, 6]
# ], dtype=np.int32)
polygon_coords = np.array([
    [210, 386], [505, 390], [626, 477], [593, 479], [509, 407], [209, 402], [120, 478], [90, 479]
], dtype=np.int32)


# Path to the input video
video_path = 'rotated-video/output_horizontal_video.mp4'

# Output file names
output_contoured_frame = 'contoured_frame.png'
output_cropped_frame = 'cropped_frame.png'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Move to the last frame
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

# Read the last frame
ret, frame = cap.read()
if not ret:
    print("Failed to read the video frame")
    cap.release()
    exit()

# Draw the contours on the frame
cv2.polylines(frame, [polygon_coords], isClosed=True, color=(0, 255, 0), thickness=2)

# Save the contoured frame
cv2.imwrite(output_contoured_frame, frame)

# Create a mask with the same dimensions as the frame
mask = np.zeros_like(frame)
cv2.fillPoly(mask, [polygon_coords], (255, 255, 255))

# Apply the mask to the frame
masked_frame = cv2.bitwise_and(frame, mask)

# Crop the image to the bounding box of the polygon
x, y, w, h = cv2.boundingRect(polygon_coords)
cropped_frame = masked_frame[y:y+h, x:x+w]

# Save the cropped frame
cv2.imwrite(output_cropped_frame, cropped_frame)

# Release the video capture object
cap.release()

print(f"Frames saved: \n- Contoured Frame: '{output_contoured_frame}' \n- Cropped Frame: '{output_cropped_frame}'")
