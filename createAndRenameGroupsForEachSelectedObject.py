import bpy
import copy

selection = copy.copy(bpy.context.selected_objects)
bpy.ops.object.select_all(action='DESELECT')
for ob in selection:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=str(ob.name))
    if not str(ob.name) in bpy.data.groups:
        bpy.ops.group.create(name=str(ob.name))