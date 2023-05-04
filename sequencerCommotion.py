import bpy
import os

# Path to the directory containing the videos
directory = r"C:\Users\User\Videos\"

# Get a list of all files in the directory
files = os.listdir(directory)

# Sort the files alphabetically
files.sort()

# Set the number of frames to skip between each video (change this to adjust the gap)
duration = 90
skip_frames = 10

i=0
# Loop through each file in the directory
for k,file in enumerate(files):
    # Check if the file is a video (you can adjust this to match the file extensions of your videos)
    if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mov"):
        
        if i>20:
            break
        # Calculate the frame start for the current video
        
        block_length = duration/skip_frames
        frame_start = int(i/block_length)*duration

        
        # Create a new strip in the video sequencer
        strip = bpy.context.scene.sequence_editor.sequences.new_movie(name=file, filepath=os.path.join(directory, file), channel=i, frame_start=frame_start)
        # Set the frame offset of the strip to 0
        strip.frame_offset_start = (i%block_length)*skip_frames
        strip.frame_final_duration = duration
        
        #strip.frame_start= strip.frame_offset_start
        
        print(frame_start,strip.frame_offset_start)
        i= i+1



