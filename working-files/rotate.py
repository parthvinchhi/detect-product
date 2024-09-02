from moviepy.editor import VideoFileClip

def rotate_video(input_file, output_file):
    # Load the video
    video = VideoFileClip(input_file)
    
    # Rotate the video by 90 degrees
    rotated_video = video.rotate(90)  # Use -90 for counter-clockwise rotation
    
    # Write the rotated video to a file
    rotated_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

# Example usage
input_file = 'b-side/b1.mp4'
output_file = 'rotated-video/output_horizontal_video.mp4'

rotate_video(input_file, output_file)
