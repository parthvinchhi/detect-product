import os
from PIL import Image

def get_gif_duration(gif_path):
    """Calculates the duration of a GIF in seconds."""
    with Image.open(gif_path) as gif:
        # Number of frames in the GIF
        n_frames = gif.n_frames
        # Duration per frame in milliseconds
        frame_duration = gif.info['duration']  # Duration is in milliseconds
        
        # Total duration in seconds
        total_duration = (n_frames * frame_duration) / 1000.0
        return total_duration

def check_gif_lengths(directory):
    """Checks and prints the length of each GIF in the directory."""
    for filename in os.listdir(directory):
        if filename.lower().endswith('.gif'):
            gif_path = os.path.join(directory, filename)
            try:
                duration = get_gif_duration(gif_path)
                print(f"{filename}: {duration:.2f} seconds")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    directory = './gif-videos'  # Change this to your directory path
    check_gif_lengths(directory)
