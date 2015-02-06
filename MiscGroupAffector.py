import bpy
import math
import mathutils
#from mathutils import Vector,Euler,Matrix,Quaternion

print("RUNNING")
def my_handler(scene):
    for ob in bpy.data.groups['B'].objects:
      targetObject= bpy.data.objects['T']
      vector= targetObject.location-ob.location
      up_axis = mathutils.Vector([0.0, 0.0, 1.0])
      angle = vector.angle(up_axis, 0)
      axis = up_axis.cross(vector)
      euler = mathutils.Matrix.Rotation(angle, 4, axis).to_euler()
      
      coordinateNoiseInfluence =0.1
      frame = scene.frame_current/4
      euler.x += coordinateNoiseInfluence * math.cos(ob.location.x+frame)
      euler.y += coordinateNoiseInfluence * math.sin(ob.location.y+frame)
      euler.z += coordinateNoiseInfluence * math.sin(ob.location.z+frame)
      ob.rotation_euler =euler
bpy.app.handlers.frame_change_pre.append(my_handler)