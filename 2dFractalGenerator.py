import bpy
import math
import random
import mathutils
import copy
from bpy.props import BoolProperty
from bpy_extras.io_utils import unpack_list

def angle_to_rad(x):
	return x * (math.pi / 180);
def rotate_point(point, center, angle):
	angleInRadians = angle_to_rad(angle)
	cosTheta = math.cos(angleInRadians)
	sinTheta = math.sin(angleInRadians)
	pointC = mathutils.Vector((cosTheta * (point.x-center.x)-sinTheta*(point.y-center.y)+center.x , sinTheta*(point.x-center.x)+cosTheta*(point.y-center.y)+center.x))
	return pointC

origin = mathutils.Vector((0,0,0))
seg_length = 2
splits = 2
split_angle = 0
gen_max= 4
gen_size = 0.8
gen_thick = 12
gen_thick_mod = 0.8

#[generation number][point][0=location,1=rotation]
gen_array_data = []

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


#starting point
current_gen = 0
pointA=mathutils.Vector((0,0,0))


#generation 0 no split just add offset and create line.
spline = fractalCurveData.splines.new('BEZIER')
spline.bezier_points.add(1)
#spline.bezier_points.foreach_set("co", unpack_list(coordinate_Pairs))
spline.bezier_points[0].co=mathutils.Vector((0,0,0))
spline.bezier_points[1].co=mathutils.Vector((seg_length,0,0))
gen_array_data=[[tuple([mathutils.Vector((seg_length,0,0)),mathutils.Vector((0,0,0))])]]


for i in range(1,int(gen_max+1)):
	lastGenerationPoints = gen_array_data[i-1]
	#create two new points for each old point
	for a in lastGenerationPoints:				#a = gen_array_data[i-1][a](loc,rot)
		center = copy.copy(a[0]) 
		for split in range(int(splits)):
			newLocation = mathutils.Vector((center[0][0]+seg_length,center[0][1],center[0][2]))
			newPoint = rotate_point(newLocation, center, split*(90/splits))
			#create edges
			spline = fractalCurveData.splines.new('BEZIER')
			spline.bezier_points.add(1)
			spline.bezier_points[0].co=center[0]
			spline.bezier_points[1].co=newPoint
			gen_array_data=[[tuple([mathutils.Vector((seg_length,0,0)),mathutils.Vector((0,0,0))])]]

			#append point to gen_array_data
			gen_array_data[i].append(mathutils.Vector((newPoint)),mathutils.Vector((0,0,split*(90/splits)+center[1])))


	



	


	#add offset to point and create point a =(x+length,y,z)
	#rotate point a around point b
	#create segment
	#do this for branch x and y
	#store points in generation
	#create points from generation set n-1(a) and n(children)




class ToolsPanel(bpy.types.Panel):
    bl_label = "Animatable Threshold Line Generator"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        row= layout.row()
        row.prop(context.scene, "lineGenActivate")
def register():
    bpy.types.Scene.curveOutward = BoolProperty(name="outward",description="forces curve outward away from 0,0,0", default=False)
    bpy.types.Scene.segLength = bpy.props.FloatProperty(name="segment length", description="changes the base length of fractal edges", default=1, min=-10, max=10)
    bpy.types.Scene.segSplits = bpy.props.FloatProperty(name="generation splits", description="changes the number of splits", default=1, min=-10, max=10)
    bpy.types.Scene.segSplitAngle = bpy.props.FloatProperty(name="angle modulation", description="angle modulation of splits", default=0, min=0, max=180)
    bpy.types.Scene.genMax = bpy.props.FloatProperty(name="number of generations", description="WARNING: KEEP LOW (change script if you want something beyond 10)", default=4, min=0, max=10)
    bpy.types.Scene.genSize = bpy.props.FloatProperty(name="generation length modulation", description="generation * length", default=0.95, min=-10, max=10)
    bpy.types.Scene.genThick = bpy.props.FloatProperty(name="base generation weight", description="base thickness", default=0.95, min=-10, max=10)
    bpy.types.Scene.genThickMod = bpy.props.FloatProperty(name="generation weight modulation", description="generation * base thickness", default=1, min=-5, max=5)

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

if __name__ == "__main__":
    register()












