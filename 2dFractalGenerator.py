import bpy
import math
import random
import mathutils
import copy
from bpy.props import BoolProperty
from bpy_extras.io_utils import unpack_list

print("initialize")
################################
###   CREATE CURVE OBJECT    ###
################################
fractalCurveData = bpy.data.curves.new(name="FractalCurve", type='CURVE')
obj = bpy.data.objects.new("CurveObj", fractalCurveData)
bpy.context.scene.objects.link(obj)
obj.data.resolution_u     = 1
obj.data.bevel_depth      = 0.1
obj.data.bevel_resolution = 1
obj.data.dimensions = '3D'
obj.data.fill_mode = 'FULL'



def main(context):
	print("main process")





#########################################
##########     FRAME HANDLER     ######## 
#########################################
def my_handler(scene): 
	fractalCurveData.splines.clear()

	origin = mathutils.Vector((0,0,0))
	seg_length = bpy.context.scene.segLength
	splits = bpy.context.scene.segSplits
	split_angle = bpy.context.scene.segSplitAngle
	gen_max = bpy.context.scene.genMax
	gen_size = bpy.context.scene.genSize
	gen_thick = bpy.context.scene.genThick
	gen_thick_mod = bpy.context.scene.genThickMod
	
	gen_array_data = []#[generation number][point][0=location,1=rotation]
	#starting point
	current_gen = 0
	pointA=mathutils.Vector((0,0,0))
	#generation 0 no split just add offset and create line.
	spline = fractalCurveData.splines.new('BEZIER')
	spline.bezier_points.add(1)
	#spline.bezier_points.foreach_set("co", unpack_list(coordinate_Pairs))
	spline.bezier_points[0].co=mathutils.Vector((0,0,0))
	spline.bezier_points[1].co=mathutils.Vector((seg_length,0,0))
	spline.bezier_points[0].radius = .01
	spline.bezier_points[1].radius = .01
	gen_array_data=[[tuple([mathutils.Vector((seg_length,0,0)),mathutils.Vector((0,0,0))])]]
	print("new frame-----------------------------------------------------------------------")
	for i in range(1,int(gen_max+1)):
		gen_array_data.append([])
		lastGenerationPoints = gen_array_data[i-1]
		#create two new points for each old point
		for a in lastGenerationPoints:				#a = gen_array_data[i-1][a](loc,rot)
			center = copy.copy(a[0]) 
			for split in range(splits):
				newLocation = center + mathutils.Vector(((seg_length*(gen_size**i)),0,0))
				newRotation = copy.copy(a[1][2])	#z axis rotation
				#newRotation = split*(180/splits)+center[1]
				if splits > 1:
					newRotation += (-split_angle/2)+(split*(split_angle/(splits-1)))
				else:
					break
				newRotation_unformatted = newRotation
				if abs(newRotation) != newRotation:
					newRotation == -1*(newRotation % 360) 
				else:
					newRotation == (newRotation % 360)
				if newRotation < 0 :
					newRotation=360-newRotation
				newPoint = rotate_point(newLocation, center, newRotation)
				print("gen:",i," segment:",split," angle = ",newRotation_unformatted," CENTER:",center," newlocation:",newPoint)
				#create edges
				spline = fractalCurveData.splines.new('BEZIER')
				spline.bezier_points.add(1)
				spline.bezier_points[0].co=a[0]
				spline.bezier_points[1].co=newPoint
				spline.bezier_points[0].handle_left_type='VECTOR'
				spline.bezier_points[0].handle_right_type='VECTOR'
				spline.bezier_points[1].handle_left_type='VECTOR'
				spline.bezier_points[1].handle_right_type='VECTOR'

				spline.bezier_points[0].radius = .01
				spline.bezier_points[1].radius = .01




				#append point to gen_array_data
				#print(gen_array_data)
				gen_array_data.append([])
				newTuple = (mathutils.Vector((newPoint)),mathutils.Vector((0,0,newRotation)))
				gen_array_data[i].append(newTuple)

class ToolsPanel(bpy.types.Panel):
    bl_label = "Animatable Fractal Line Generator"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        #row= layout.row()
        #row.operator("object.generate",icon="STICKY_UVS_DISABLE")
        row= layout.row()
        row.prop(context.scene, "genMax")
        row= layout.row()
        row.prop(context.scene, "genSize")
        row= layout.row()
        row.prop(context.scene, "genThick")
        row= layout.row()
        row.prop(context.scene, "genThickMod")
        row= layout.row()
        row.prop(context.scene, "segLength")
        row= layout.row()
        row.prop(context.scene, "segSplits")
        row= layout.row()
        row.prop(context.scene, "segSplitAngle")
class Object_OT_generate(bpy.types.Operator):
	'''Generate Fractal'''
	bl_idname = "object.generate"
	bl_label = "GENERATE FRACTAL"

	@classmethod 
	def poll(cls, context):
		main(context)
		return {'FINISHED'}
def angle_to_rad(x):
	return x * (180 / math.pi );
def angle_to_degree(x):
	return x * (math.pi / 180);
def rotate_point(point, center, angle):
	angleInRadians = angle_to_rad(angle)
	cosTheta = math.cos(angleInRadians)
	sinTheta = math.sin(angleInRadians)
	pointC = mathutils.Vector((  (cosTheta*(point.x-center.x) -sinTheta*(point.y-center.y) +center.x) , (sinTheta*(point.x-center.x)+cosTheta*(point.y-center.y) +center.y)   ,0  ))
	#pointC = mathutils.Vector((  (sinTheta*(point.x-center.x)+cosTheta*(point.y-center.y) +center.y)   , (cosTheta*(point.x-center.x) -sinTheta*(point.y-center.y) +center.x)  ,0  ))
	return pointC		
def register():
    bpy.types.Scene.curveOutward= BoolProperty(name="outward",description="forces curve outward away from 0,0,0", default=False)
    bpy.types.Scene.segLength= bpy.props.FloatProperty(name="segment length", description="changes the base length of fractal edges", default=1, min=-10, max=10)
    bpy.types.Scene.segSplits= bpy.props.IntProperty(name="generation splits", description="changes the number of splits", default=1, min=-10, max=10,subtype='UNSIGNED')
    bpy.types.Scene.segSplitAngle= bpy.props.FloatProperty(name="base angle", description="angle modulation of splits", default=90, min=0, max=180)
    bpy.types.Scene.genMax= bpy.props.IntProperty(name="Generations", description="number of generations to compute",default = 5, min = 0, max=100, subtype='UNSIGNED')
    bpy.types.Scene.genSize= bpy.props.FloatProperty(name="generation length modulation", description="generation * length", default=0.95, min=-10, max=10)
    bpy.types.Scene.genThick= bpy.props.FloatProperty(name="base generation weight", description="base thickness", default=0.95, min=-10, max=10)
    bpy.types.Scene.genThickMod= bpy.props.FloatProperty(name="generation weight modulation", description="generation * base thickness", default=1, min=-5, max=5)

    bpy.app.handlers.frame_change_pre.append(my_handler)
    bpy.utils.register_module(__name__)
def unregister():
	del(bpy.types.Scene.curveOutward)
	del(bpy.types.Scene.segLength)
	del(bpy.types.Scene.segSplits)
	del(bpy.types.Scene.segSplitAngle)
	del(bpy.types.Scene.genMax)
	del(bpy.types.Scene.genSize)
	del(bpy.types.Scene.genThick)
	del(bpy.types.Scene.genThickMod)
	del(bpy.types.Scene.curveOutward)
	del(bpy.types.Scene.pointLerp)
	bpy.app.handlers.frame_change_pre.remove(my_handler)
if __name__ == "__main__":
    register()