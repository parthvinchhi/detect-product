import cv2
import os
import imageio
from PIL import Image

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
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame_rgb))
    
    cap.release()
    return frames, fps

def save_frames_as_gif(frames, fps, output_path):
    """Saves the frames as a GIF with color preservation."""
    gif_output_path = os.path.splitext(output_path)[0] + '.gif'
    
    # Save the GIF using a better color palette
    frames[0].save(
        gif_output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),  # Duration per frame in milliseconds
        loop=0,
        optimize=True,
        quality=95,
        dither=Image.FLOYDSTEINBERG,  # Use dithering to improve color transitions
    )
    
    print(f"GIF saved to {gif_output_path}")

def process_videos_in_directory(directory):
    """Processes each video in the directory, trimming the last part and converting it to GIF."""
    output_dir = os.path.join(directory, '../gif-videos')
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(directory, filename)
            try:
                frames, fps = trim_video_to_last_part(video_path, output_dir)
                if frames:
                    output_path = os.path.join(output_dir, filename)
                    save_frames_as_gif(frames, fps, output_path)
                else:
                    print(f"Failed to extract frames from {filename}")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    directory = './b-side'  # Change this to your directory path
    process_videos_in_directory(directory)
