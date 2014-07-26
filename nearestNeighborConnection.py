import bpy
import math
import random
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
    randomConnections = bpy.context.scene.randomConnections
    handle_random_mul = bpy.context.scene.randomizeInfluence
    randomNum=[]
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
                    if (randomConnections):
                            randomNum = random.random()*100
                            if randomNum <= bpy.context.scene.randomConnections_threshold:
                                if distance >= ANIM_DIST:
                                    distance = ANIM_DIST*0.9
                            if randomNum >= bpy.context.scene.randomConnections_threshold:
                                distance = ANIM_DIST*3
                    else:
                        distance = ANIM_DIST*2
                    if distance <= ANIM_DIST:
                        minimumRadius = bpy.context.scene.radius_minimum
                        radius_multiplier = bpy.context.scene.radius_multiplier
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
                            left_dx = bpy.context.scene.left_dx
                            left_dy = bpy.context.scene.left_dy
                            left_dz = bpy.context.scene.left_dz
                            
                            right_dx = bpy.context.scene.right_dx
                            right_dy = bpy.context.scene.right_dy
                            right_dz = bpy.context.scene.right_dz
                            spline.bezier_points[i].handle_left[0]  = coordinate_Pairs[i][0]+left_dx
                            spline.bezier_points[i].handle_left[1]  = coordinate_Pairs[i][1]+left_dy
                            spline.bezier_points[i].handle_left[2]  = coordinate_Pairs[i][2]+left_dz

                            spline.bezier_points[i].handle_right[0] = coordinate_Pairs[i][0]+right_dx
                            spline.bezier_points[i].handle_right[1] = coordinate_Pairs[i][1]+right_dy
                            spline.bezier_points[i].handle_right[2] = coordinate_Pairs[i][2]+right_dz
                            if(bpy.context.scene.randomHandles):
                                spline.bezier_points[i].handle_left[0]  +=(0.5-random.random())*handle_random_mul 
                                spline.bezier_points[i].handle_left[1]  +=(0.5-random.random())*handle_random_mul 
                                spline.bezier_points[i].handle_left[2]  +=(0.5-random.random())*handle_random_mul 
                                spline.bezier_points[i].handle_right[0] +=(0.5-random.random())*handle_random_mul 
                                spline.bezier_points[i].handle_right[1] +=(0.5-random.random())*handle_random_mul 
                                spline.bezier_points[i].handle_right[2] +=(0.5-random.random())*handle_random_mul 
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
        row.prop(context.scene, "lineGenActivate")
        row= layout.row()
        row.prop(context.scene, "randomConnections")
        row.prop(context.scene, "randomConnections_threshold")
        row= layout.row()
        row.prop(context.scene, "animDist")
        row= layout.row()
        row.prop(context.scene, "radius_multiplier")
        row= layout.row()
        row.prop(context.scene, "radius_minimum")

        row= layout.row()
        row= layout.row()
        row.prop(context.scene, "left_dx")
        row.prop(context.scene, "right_dx")
        row= layout.row()
        row.prop(context.scene, "left_dy")
        row.prop(context.scene, "right_dy")
        row= layout.row()
        row.prop(context.scene, "left_dz")
        row.prop(context.scene, "right_dz")
        row= layout.row()
        row.prop(context.scene, "randomHandles")
        row.prop(context.scene, "randomizeInfluence")
        row= layout.row()
        row.prop(context.scene, "angleMod")
        row.prop(context.scene, "angleInfluence")


        #FILE_TICK
        #SNAP_NORMAL
def register():
    bpy.types.Scene.randomConnections = BoolProperty(name="Randomize Connections",description="ignores distance threshold", default=False)
    bpy.types.Scene.randomConnections_threshold =  bpy.props.FloatProperty(name="random %", description="chance of random connection", default=50, min=0, max=100)
    bpy.types.Scene.randomHandles = BoolProperty(name="Randomize Handles",description="adds random offsets to connector handles", default=False)
    bpy.types.Scene.randomizeInfluence = bpy.props.FloatProperty(name="Random Influence", description="left handle X axis offset", default=1, min=0, max=100)
    bpy.types.Scene.angleMod = BoolProperty(name="Handle Angle Mod",description="takes connector angles into account", default=False)
    bpy.types.Scene.angleInfluence = bpy.props.FloatProperty(name="left dX", description="left handle X axis offset", default=1, min=0, max=100)


    bpy.types.Scene.lineGenActivate = BoolProperty(name="Active",description="activates line animation per frame", default=True)
    bpy.types.Scene.animDist = bpy.props.FloatProperty(name="Distance", description="Distance Threshold", default=5.0, min=0.001, max=1000)

    bpy.types.Scene.radius_multiplier = bpy.props.FloatProperty(name="radius_multiplier", description="how much distance affects radius", default=1.0, min=0, max=100)
    bpy.types.Scene.radius_minimum = bpy.props.FloatProperty(name="radius_minimum", description="minimum radius", default=0.1, min=0.001, max=50)

    bpy.types.Scene.left_dx = bpy.props.FloatProperty(name="left dX", description="left handle X axis offset", default=0.0, min=-100, max=100)
    bpy.types.Scene.left_dy = bpy.props.FloatProperty(name="left dY", description="left handle Y axis offset", default=0.0, min=-100, max=100)
    bpy.types.Scene.left_dz = bpy.props.FloatProperty(name="left dZ", description="left handle Z axis offset", default=0.0, min=-100, max=10)
    bpy.types.Scene.right_dx = bpy.props.FloatProperty(name="right dX", description="right handle X axis offset", default=0.0, min=-100, max=100)
    bpy.types.Scene.right_dy = bpy.props.FloatProperty(name="right dY", description="right handle Y axis offset", default=0.0, min=-100, max=100)
    bpy.types.Scene.right_dz = bpy.props.FloatProperty(name="right dZ", description="right handle Z axis offset", default=0.0, min=-100, max=100)

    bpy.app.handlers.frame_change_pre.append(my_handler)
    bpy.utils.register_module(__name__)
def unregister():
    del(bpy.types.Scene.randomConnections)
    del(bpy.types.Scene.randomConnections_threshold)
    del(bpy.types.Scene.randomHandles)
    del(bpy.types.Scene.randomizeInfluence)
    del(bpy.types.Scene.angleMod)
    del(bpy.types.Scene.angleInfluence)

    del(bpy.types.Scene.animDist)
    del(bpy.types.Scene.lineGenActivate)

    del(bpy.types.Scene.radius_multiplier)
    del(bpy.types.Scene.radius_minimum)

    del(bpy.types.Scene.left_dx)
    del(bpy.types.Scene.left_dy)
    del(bpy.types.Scene.left_dz)
    del(bpy.types.Scene.right_dx)
    del(bpy.types.Scene.right_dy)
    del(bpy.types.Scene.right_dz)

    bpy.app.handlers.frame_change_pre.remove(my_handler)
if __name__ == "__main__":
    register()