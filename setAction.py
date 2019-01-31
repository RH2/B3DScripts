import bpy
import datetime
S_time =  datetime.datetime.now()
print("---RUNNING ::: "+str(S_time)+"---")
action = bpy.data.actions["putAway"]
bpy.data.objects["AR_RIG"].animation_data.action = action
bpy.data.objects["ARMS"].animation_data.action = action
bpy.data.objects["HELPER"].animation_data.action = action