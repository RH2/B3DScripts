import bpy
x = bpy.data.scenes["Scene"].sequence_editor.sequences_all["shuffle_aa_2__B.mp4"].transform.offset_x


# Get the selected movie tracks
selected_tracks = [track for track in bpy.context.selected_sequences if track.type == 'MOVIE']

# Set the X transform for each selected track
for track in selected_tracks:
    track.transform.offset_x = x
