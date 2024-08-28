import cv2
import os

def get_video_length(video_path):
    """Returns the length of the video in seconds."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error opening video file {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total frame count
    duration = frame_count / fps  # Duration in seconds
    
    cap.release()
    return duration

def check_videos_in_directory(directory):
    """Checks the length of each video in the specified directory."""
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(directory, filename)
            try:
                length = get_video_length(video_path)
                print(f"{filename}: {length:.2f} seconds")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    directory = './b-side/new video'  # Change this to your directory path
    check_videos_in_directory(directory)
