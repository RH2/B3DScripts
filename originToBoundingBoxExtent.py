import bpy
import copy
import mathutils
print("-----running")
# store the location of current 3d cursor
saved_location = mathutils.Vector(bpy.context.scene.cursor_location)  # returns a vector
list = copy.copy(bpy.context.selected_objects)
bpy.context.scene.objects.active = None
for object in list:
    object.select = True
    world_matrix = mathutils.Matrix(object.matrix_world)
    corner = mathutils.Vector((object.bound_box[1]))
    location = mathutils.Vector(world_matrix * corner)
    print(object.name,location)
    bpy.context.scene.cursor_location = location
    # set the origin on the current object to the 3dcursor location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    object.select = False

# set 3dcursor location back to the stored location
bpy.context.scene.cursor_location = saved_location