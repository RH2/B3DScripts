#src= http://blender.stackexchange.com/questions/tagged/particles
#extra = http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Simulations
import bpy

# Set these to False if you don't want to key that property.
KEYFRAME_LOCATION = True
KEYFRAME_ROTATION = True
KEYFRAME_SCALE = False
KEYFRAME_VISIBILITY = False  # Viewport and render visibility.

def create_objects_for_particles(deadParticles, obj, end_frame):
    # Duplicate the given object for every particle and return the duplicates.
    # Use instances instead of full copies.
    obj_list = []
    livingParticles=[]
    mesh = obj.data
    for i, _ in enumerate(deadParticles):
        dupli = bpy.data.objects.new(
                    name="particle.{:03d}".format(i),
                    object_data=mesh)
        bpy.context.scene.objects.link(dupli)
        obj_list.append(dupli)
    return obj_list
def notAliveAtEnd(ps,end_frame):
    deadParticles = []
    bpy.context.scene.frame_set(end_frame)
    for p in ps.particles:
        if p.alive_state== "DEAD":
            deadParticles.append(p)
    return deadParticles
def match_and_keyframe_objects(deadParticles, obj_list, start_frame, end_frame):
    # Match and keyframe the objects to the particles for every frame in the
    # given range.
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        for p, obj in zip(deadParticles, obj_list):
            match_object_to_particle(p, obj)
            keyframe_obj(obj)
def MarkDirty(obj_list):
    for ob in obj_list:
        bpy.context.scene.objects.active = ob
        bpy.ops.object.group_link(group="Reactors")
        #ob.group_link(group="Reactors")
def match_object_to_particle(p, obj):
    aliveOnThisFrame=False
    if p.alive_state== "ALIVE":
        aliveOnThisFrame=True
    bpy.context.scene.frame_set(bpy.context.scene.frame_current+1)    
    aliveOnNextFrame=False
    if p.alive_state== "ALIVE":
        aliveOnNextFrame=True
    bpy.context.scene.frame_set(bpy.context.scene.frame_current-1)    
    if aliveOnThisFrame==True and aliveOnNextFrame==False:
    #if p.alive_state == 'DYING':
        bpy.context.scene.objects.active = obj
        bpy.ops.object.shade_smooth()
        bpy.ops.object.particle_system_add()
        psys = obj.particle_systems[-1]
        psys.name='Reactor_SET.A'
        pset = psys.settings
        pset.count = 200
        pset.frame_start = bpy.context.scene.frame_current
        pset.frame_end = bpy.context.scene.frame_current+5
        pset.effector_weights.gravity = 0
        pset.normal_factor= 8
        pset.use_render_emitter= False
        pset.render_type = "OBJECT"
        pset.dupli_object= bpy.data.objects["Reactor_spark"]
        pset.particle_size = 1 
        pset.use_dynamic_rotation = True
        pset.angular_velocity_factor= 8.5
        pset.rotation_factor_random = 0.5
        pset.phase_factor_random = 0.4
    loc = p.location
    rot = p.rotation
    size = p.size
    obj.location = loc
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = rot
    obj.scale = (size, size, size)

def keyframe_obj(obj):
    # Keyframe location, rotation, scale and visibility if specified.
    if KEYFRAME_LOCATION:
        obj.keyframe_insert("location")
    if KEYFRAME_ROTATION:
        obj.keyframe_insert("rotation_quaternion")
    if KEYFRAME_SCALE:
        obj.keyframe_insert("scale")
    if KEYFRAME_VISIBILITY:
        frameA=bpy.context.scene.frame_current
        obj.keyframe_insert("hide")
        obj.keyframe_insert("hide_render")


def main():
    # Assume only 2 objects are selected.
    # The active object should be the one with the particle system.
    if not 'Reactors' in bpy.data.groups:  
        bpy.ops.group.create(name="Reactors")   
    ps_obj = bpy.context.object
    obj = [obj for obj in bpy.context.selected_objects if obj != ps_obj][0]
    ps = ps_obj.particle_systems[0]  # Assume only 1 particle system is present.
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    ps=notAliveAtEnd(ps,end_frame)
    obj_list = create_objects_for_particles(ps, obj, end_frame)
    MarkDirty(obj_list)
    match_and_keyframe_objects(ps, obj_list, start_frame, end_frame)

if __name__ == '__main__':
    main()