import bpy
import math
import random
import mathutils
import copy
from bpy.props import BoolProperty
from bpy_extras.io_utils import unpack_list

def angle_to_rad(x):
	return x * (Math.PI / 180);
def rotate_point(point, center, angle):
	angleInRadians = angle_to_rad(angle)
	cosTheta = Math.cos(angleInRadians)
	sinTheta = Math.sin(angleInRadians)
	pointC = Vector((cosTheta * (point.x-center.x)-sinTheta*(point.y-center.y)+center.x , sinTheta*(point.x-center.x)+cosTheta*(point.y-center.y)+center.x)))
	return pointC

#define origin 
origin = Vector((0,0,0))
#define number of generations
gen_max= 4
#define number of splits
splits = 2
#define angle split (modulation) (if not zero, set offset )
split_angle = 0
#define segment length
seg_length = 2
#define generation shrinkage
gen_size = 0.8
#define generation default & thickness mod
gen_thick = 12
gen_thick_mod = 0.8

#generations
array_generations = []
#generation array index returns list of points
array_generation_points = []
#each point has location and rotation
array_generation_data = []

#for i in array_generations[x].array.generation.points[]:
#	location = array_generations[x].array.generation.points[i].array_generation_data[0]
#	roation = array_generations[x].array.generation.points[i].array_generation_data[1]


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
pointA=Vector((0,0,0))


#generation 0 no split just add offset and create line.
spline = curvedata.splines.new('BEZIER')
spline.bezier_points.add(1)
spline.bezier_points.foreach_set("co", unpack_list(coordinate_Pairs))
spline.bezier_points[0]=Vector((0,0,0))
spline.bezier_points[1]=Vector((seg_length,0,0))

#generation n
for(i in gen_max):
	current_gen_size = i * gen_size
	point_population += i ** 2

	



#add offset to point and create point a =(x+length,y,z)
#rotate point a around point b
#create segment
#do this for branch x and y
#store points in generation
#create points from generation set n-1(a) and n(children)









