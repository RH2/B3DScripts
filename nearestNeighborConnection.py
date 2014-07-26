import bpy
import math
import mathutils
import copy
from bpy.props import BoolProperty
from bpy_extras.io_utils import unpack_list

###################################################
####################    SECTION 1      BEGIN SCRIPT
###################################################

print("RUNNING...")
bpy.ops.object.select_all(action='DESELECT')
if not 'dynaLines' in bpy.data.groups:
    bpy.ops.group.create(name="dynaLines") 

###################################################
####################    SECTION 2    MATERIAL SETUP
###################################################    

lineMaterial=[]
for material in bpy.data.materials:
    if material.name == "line" or "Line" or "LINE":
        lineMaterial=material

###################################################
########### SECTION 3   SELECT POINTS TO OPERATE ON 
###################################################


bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_same_group(group="Point")
bpy.ops.object.select_same_group(group="Points")
bpy.ops.object.select_same_group(group="point")
bpy.ops.object.select_same_group(group="points")

pointList= []
pointList=copy.copy(bpy.context.selected_objects)


curvedata = bpy.data.curves.new(name="Curve", type='CURVE')
obj = bpy.data.objects.new("CurveObj", curvedata)
bpy.context.scene.objects.link(obj)
obj.data.resolution_u     = 1
obj.data.bevel_depth      = 0.1
obj.data.bevel_resolution = 1
obj.data.dimensions = '3D'
obj.data.fill_mode = 'FULL'


###################################################
####################    SECTION 4     FRAME HANDLER    
###################################################

def my_handler(scene): 
    frame = scene.frame_current
    activationFlag = bpy.context.scene.lineGenActivate
    ANIM_DIST=bpy.context.scene.animDist
    print(str(activationFlag) + " " +str(ANIM_DIST))
    if activationFlag == True:
        
        #go through each object in the group (set up index boundaries)
        xLength = len(pointList) #-1 
        indexA=0
        bpy.ops.object.select_all(action='DESELECT')
        curvedata.splines.clear()
        for x in pointList:
            indexA= indexA+1
            if indexA <= xLength:
                for indexY in range(indexA,xLength):
                    y= pointList[indexY]
                    locX=x.location
                    locY=pointList[indexY].location
                    distance = math.sqrt( (locX[0] - locY[0])**2 + (locX[1] - locY[1])**2 + (locX[2] - locY[2])**2)
                    if distance <= ANIM_DIST:
                        minimumRadius = 0.1
                        radius_multiplier = 1
                        pointRadius = (1 - (distance / ANIM_DIST))*radius_multiplier + minimumRadius
                        coordinate_Pairs = []
                        print(locX)
                        print(locY)
                        coordinate_Pairs.append(locX)
                        coordinate_Pairs.append(locY)

                        spline = curvedata.splines.new('BEZIER')
                        spline.bezier_points.add(1)
                        spline.bezier_points.foreach_set("co", unpack_list(coordinate_Pairs))
                        #spline.bezier_points.foreach_set("radius"-1, pointRadius)
                        for i in range(0,1):
                            spline.bezier_points[i].radius = pointRadius

###################################################
####################    SECTION 5   UI/REGISTRATION
###################################################


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
    bpy.app.handlers.frame_change_pre.append(my_handler)
    bpy.utils.register_module(__name__)
def unregister():
    del(bpy.types.Scene.animDist)
    del(bpy.types.Scene.lineGenActivate)
    bpy.app.handlers.frame_change_pre.remove(my_handler)
if __name__ == "__main__":
    register()