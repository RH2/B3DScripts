import bpy
import math
import mathutils
import copy
from bpy.props import BoolProperty
print("RUNNING...")
if not 'Reactors' in bpy.data.groups:
    bpy.ops.group.create(name="dynaLines") 

lineMaterial=[]
for material in bpy.data.materials:
    if material.name == "line" or "Line" or "LINE":
        lineMaterial=material
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_same_group(group="Points")
pointList= []
pointList=copy.copy(bpy.context.selected_objects)



def my_handler(scene): 
    override = {'selected_bases': list(bpy.context.scene.object_bases)}
    if bpy.context.scene['lineGenActivate'] == False:
        a=1 
    #print("Frame Change", scene.frame_current)
    if bpy.context.scene['lineGenActivate'] == True:
        ANIM_DIST=bpy.context.scene['animDist']
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_same_group(group="dynaLines")
        bpy.ops.object.delete() 
        #go through each object in the group
        xLength = len(pointList) #-1 
        a=0
        childCurveIndex=0 
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.curve.primitive_bezier_curve_add()
        obj = bpy.context.object
        bpy.ops.object.group_link(group='dynaLines')
        obj.material_slots.data.active_material= lineMaterial
        obj.data.dimensions = '3D'
        obj.data.fill_mode = 'FULL'
        obj.data.bevel_depth = 0.1#-(1-distance/ANIM_DIST)*.08
        obj.data.bevel_resolution = 0 #0=4points,#1=6points
        obj.data.resolution_u=1
        for x in pointList:
            a= a+1
            if a <= xLength:
                for indexY in range(a,xLength):
                    y= pointList[indexY]
                    locX=x.location
                    locY=pointList[indexY].location
                    distance = math.sqrt( (locX[0] - locY[0])**2 + (locX[1] - locY[1])**2 + (locX[2] - locY[2])**2)
                    if distance <= ANIM_DIST:
                        # set first point to centre of sphere1
                        obj.data.splines[childCurveIndex].bezier_points[0].co = locX
                        obj.data.splines[childCurveIndex].bezier_points[0].handle_left_type = 'VECTOR'
                        # set second point to centre of sphere2
                        obj.data.splines[childCurveIndex].bezier_points[1].co = locY
                        obj.data.splines[childCurveIndexa].bezier_points[1].handle_left_type = 'VECTOR'
                        bpy.ops.object.group_link(group='dynaLines')
                        childCurveIndex=childCurveIndex+1                                  
        #bpy.ops.object.select_all(action='DESELECT')
        #bpy.ops.object.select_same_group(group="dynaLines")
class ToolsPanel(bpy.types.Panel):
    bl_label = "Animatable Threshold Line Generator"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        row= layout.row()
        row.prop(context.scene, "animDist")
        layout = self.layout
        row= layout.row()
        row.prop(context.scene, "lineGenActivate")
        #FILE_TICK
        #SNAP_NORMAL
def register():
    bpy.types.Scene.lineGenActivate = BoolProperty(name="Active",description="activates line animation per frame", default=True)
    bpy.types.Scene.animDist = bpy.props.FloatProperty(name="Distance", description="Distance Threshold", default=5.0, min=0.001, max=1000)
    bpy.utils.register_module(__name__)
def unregister():
    del(bpy.types.Scene.animDist)
    del(bpy.types.Scene.lineGenActivate)
    
bpy.app.handlers.frame_change_pre.append(my_handler)
if __name__ == "__main__":
    register()