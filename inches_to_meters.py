import bpy

a = bpy.context.active_object.dimensions
b = a * 0.0254 
bpy.context.active_object.dimensions = b