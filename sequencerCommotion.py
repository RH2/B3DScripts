import bpy
import os
from pathlib import Path
scene = bpy.context.scene
seq = scene.sequence_editor.sequences
current_frame = 1 
# Replace this path with the directory containing your video files
directory = r"C:\Users\Reference\Videos\leaf\fall"

# Function to get the creation date of a file
def get_file_creation_date(file_path):
    return os.path.getctime(file_path)

# Function to add a video strip to the video sequencer
def add_video_strip(file_path, frame_start, frame_end):
    bpy.context.scene.sequence_editor_create()
    bpy.ops.sequencer.movie_strip_add(filepath=file_path, frame_start=frame_start, frame_end=frame_end)

# Get a list of video files in the directory
video_files = [file for file in os.listdir(directory) if file.lower().endswith((".mp4", ".avi", ".mov"))]

# Sort the video files by their creation date
video_files.sort(key=lambda x: get_file_creation_date(os.path.join(directory, x)))

# Duration of each video strip in frames (adjust this as needed)
strip_duration = 10



# Set the number of frames to skip between each video (change this to adjust the gap)
duration = 90
skip_frames = 10

i=0
# Loop through each file in the directory
for k,file in enumerate(video_files):
    # Check if the file is a video (you can adjust this to match the file extensions of your videos)
    if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mov"):
        
        if i>20:
            break
        # Calculate the frame start for the current video
        
        block_length = duration/skip_frames
        frame_start = int(i/block_length)*duration

        
        # Create a new strip in the video sequencer
        strip = bpy.context.scene.sequence_editor.sequences.new_movie(name=file, filepath=os.path.join(directory, file), channel=0, frame_start=frame_start)
        # Set the frame offset of the strip to 0
        strip.frame_offset_start = (i%block_length)*skip_frames
        strip.frame_final_duration = skip_frames
        
        #strip.frame_start= strip.frame_offset_start
        
        print(frame_start,strip.frame_offset_start)
        i= i+1
        bpy.data.scenes["Scene"].frame_end = k*skip_frames
