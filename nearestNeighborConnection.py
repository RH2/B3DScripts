import bpy
import math
import mathutils
import copy
from bpy.props import BoolProperty

###################################################
####################    SECTION 1      BEGIN SCRIPT
###################################################

print("RUNNING...")
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
####################    SECTION 3    
###################################################


bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_same_group(group="Points")
pointList= []
pointList=copy.copy(bpy.context.selected_objects)


###################################################
####################    SECTION 4     FRAME HANDLER    
###################################################

def my_handler(scene): 
    #print("Frame Change", scene.frame_current)
    #if bpy.context.scene['lineGenActivate'] == False:
        #indexA=1 
    activationFlag = bpy.context.scene['lineGenActivate']
    if activationFlag == True:
        ANIM_DIST=bpy.context.scene['animDist']
        #go through each object in the group (set up index boundaries)
        xLength = len(pointList) #-1 
        indexA=0
        bpy.ops.object.select_all(action='DESELECT')


        ############################
        #       ARRAY TO HOLD POINTS    
        ############################
        coordinate_Pairs = []


        for x in pointList:
            indexA= indexA+1
            if indexA <= xLength:
                for indexY in range(indexA,xLength):
                    y= pointList[indexY]
                    locX=x.location
                    locY=pointList[indexY].location
                    distance = math.sqrt( (locX[0] - locY[0])**2 + (locX[1] - locY[1])**2 + (locX[2] - locY[2])**2)
                    if distance <= ANIM_DIST:
                        coordinate_Pairs.append(locX)
                        coordinate_Pairs.append(locY)

        #create curve from inside coordinate_Pairs
        #Curve_OBJECT = bpy.data.objects.new(name="MyObject", object_data=cu)
        #scene = bpy.context.scene
        #scene.objects.link(Curve_OBJECT)

    ############################
    # TODO GENERATE CURVE OBJECT   
    ############################







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
    bpy.app.handlers.frame_change_pre.append(my_handler)
    bpy.types.Scene.lineGenActivate = BoolProperty(name="Active",description="activates line animation per frame", default=True)
    bpy.types.Scene.animDist = bpy.props.FloatProperty(name="Distance", description="Distance Threshold", default=5.0, min=0.001, max=1000)
    bpy.utils.register_module(__name__)
def unregister():
    bpy.app.handlers.frame_change_pre.remove(my_handler)
    del(bpy.types.Scene.animDist)
    del(bpy.types.Scene.lineGenActivate)
if __name__ == "__main__":
    register()