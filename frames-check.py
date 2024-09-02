import cv2

def count_frames(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Print the total number of frames
    print(f"Total number of frames: {total_frames}")

    # Release the video capture object
    video.release()

# Replace 'your_video.mp4' with the path to your video file
video_path = 'b-side/b1.mp4'
count_frames(video_path)
