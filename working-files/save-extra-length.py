import cv2
import os

def trim_video_to_last_part(video_path, output_dir):
    """Trims the video to the last part, ensuring it's less than 1 second."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error opening video file {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total frame count
    duration = frame_count / fps  # Duration in seconds
    
    # Determine the start frame (from the last full second)
    start_time = duration - (duration - int(duration))
    start_frame = int(start_time * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    output_filename = os.path.splitext(os.path.basename(video_path))[0] + '_trimmed.mp4'
    output_path = os.path.join(output_dir, output_filename)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if out is None:
            h, w = frame.shape[:2]
            out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        
        out.write(frame)
    
    cap.release()
    if out is not None:
        out.release()
        print(f"Trimmed video saved to {output_path} with duration {duration - start_time:.2f} seconds")
        return output_path
    else:
        return None

def process_videos_in_directory(directory):
    """Processes each video in the directory, trimming the last part of each."""
    output_dir = os.path.join(directory, '../new-video')
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(directory, filename)
            try:
                trimmed_path = trim_video_to_last_part(video_path, output_dir)
                if trimmed_path:
                    # continue
                    print(f"Trimmed video saved to {trimmed_path}")
                else:
                    print(f"Failed to trim video {filename}")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    directory = './b-side'  # Change this to your directory path
    process_videos_in_directory(directory)
