#mathutils.geometry.normal(Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,0)))
#Vector((-0.0, 0.0, 1.0))


import bpy
import math
import mathutils 
from mathutils import Vector
def get_distance():
    """
    return: float. Distance of the two objects
    Must select two objects
    """
    l = []  # we store the loacation vector of each object
    for item in bpy.context.selected_objects:
        l.append(item.location)

    distance = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
    print(distance)  # print distance to console, DEBUG
    return distance
def add_prism(pointA,pointB,thickness):
    originPoint=Vector((0,0,0))

    LineNormal = mathutils.geometry.normal(pointA,pointB,originPoint)
    
    #six verts
    #verts=[pointA,pointB]
    #verts+=[pointA + Vector((1,0,0))*LineNormal,pointB + Vector((1,0,0))*LineNormal] 
    #verts+=[pointA + Vector((0,1,0))*LineNormal,pointB + Vector((0,1,0))*LineNormal] 
    verts=[pointA,pointB,pointA + Vector((1,0,0))*LineNormal,pointB + Vector((1,0,0))*LineNormal,pointA + Vector((0,1,0))*LineNormal,pointB + Vector((0,1,0))*LineNormal]
    #5 faces
    faces= [
    (0,1,3,2),
    (2,3,5,4),
    (1,0,4,5),
    (2,4,0),
    (1,5,3)
    ]
    mesh_data = bpy.data.meshes.new("prism")    
    mesh_data.from_pydata(verts, [], faces)    
    mesh_data.update() # (calc_edges=True) not needed here    
        
    cube_object = bpy.data.objects.new("Prism", mesh_data)    
        
    scene = bpy.context.scene      
    scene.objects.link(cube_object)      
    cube_object.select = True  

    
#for ob in bpy.context.selected_objects:  
#for ob in bpy.data.objects:
#    obLoc= ob.location
def main():
    add_prism(bpy.data.objects['Cube.001'].location,bpy.data.objects['Cube'].location,0)
main()


if __name__ == "__main__":
    main()