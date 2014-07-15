import bpy
import math
import mathutils
import copy

print("Running.....")
if not 'Reactors' in bpy.data.groups:
    bpy.ops.group.create(name="dynaLines")  
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_same_group(group="Points")
#go through each object in the group
pointList= []
pointList=copy.copy(bpy.context.selected_objects)
xLength = len(pointList) #-1 
a=0
for x in pointList:
    a= a+1
    if a <= xLength:
        for indexY in range(a,xLength):
            y= pointList[indexY]
            
            #check distance and add objects.
            locX=x.location
            locY=pointList[indexY].location
            distance = math.sqrt( (locX[0] - locY[0])**2 + (locX[1] - locY[1])**2 + (locX[2] - locY[2])**2)
            if distance <= 5:
                bpy.ops.curve.primitive_bezier_curve_add()
                obj = bpy.context.object
                obj.data.dimensions = '3D'
                obj.data.fill_mode = 'FULL'
                obj.data.bevel_depth = 0.08
                obj.data.bevel_resolution = 1
                obj.data.resolution_u=1
                # set first point to centre of sphere1
                obj.data.splines[0].bezier_points[0].co = locX
                obj.data.splines[0].bezier_points[0].handle_left_type = 'VECTOR'
                # set second point to centre of sphere2
                obj.data.splines[0].bezier_points[1].co = locY
                obj.data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'
                bpy.ops.object.group_link(group='dynaLines')
                                
                print("newLine")
