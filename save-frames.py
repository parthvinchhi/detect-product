import cv2
import os

def save_last_frame(video_path, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Set the frame position to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    
    # Read the last frame
    ret, frame = cap.read()
    
    if not ret:
        print(f"Error: Could not read the last frame of {video_path}")
        cap.release()
        return

    # Save the last frame as an image
    cv2.imwrite(output_path, frame)

    # Release the video capture object
    cap.release()
    print(f"Saved last frame of {video_path} as {output_path}")

def process_videos_in_directory(directory, output_directory):
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add other video file extensions if needed
            video_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_last_frame.png")
            save_last_frame(video_path, output_path)

# Define the directory containing videos and the output directory
video_directory = 'a-side'
output_directory = 'a-side-frames'

# Process videos
process_videos_in_directory(video_directory, output_directory)
