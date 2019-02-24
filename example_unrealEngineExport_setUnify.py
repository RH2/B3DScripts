#ue4export header version 0.1  --back up your data before running, will overwrite file structure
#last tested with b-v2.79 ue4export-v0.2.1
import bpy
import datetime
S_time =  datetime.datetime.now()
print("---RUNNING-UE4  ::: "+str(S_time)+"---")

#list of actions
ActionList=[
'M4_ADS_RELOAD',
'M4_ADS_FIRE',
'M4_ADS_Transition',
'M4_hipFire',
'M4_hipFire2',
'M4_hipFire3',
'M4_hipFire4',
'M4_PoseLib',
'M4_putAway']

#list of armatures to include
ObjectList=[
'ARMS',
'AR_RIG',
'HELPER']


#context
original_context = bpy.context.area.type

#Remove all animation data (Clean Slate)
for rig in ObjectList:
	rigObj = bpy.data.objects[rig]
	rigObj.animation_data_clear()
    #bpy.data.objects[rig].animation_data_clear()

#Export one action set at a time
for focusedAction in ActionList:
    for rig in ObjectList:
        rigObj = bpy.data.objects[rig]
        for action in bpy.data.objects[rig].exportActionList: 
            action.use = False
            if action.name == focusedAction:
               action.use = True
               rigObj.animation_data_clear()
               rigObj.animation_data_create()
               actiondata = bpy.data.actions[focusedAction]
               if actiondata.users>1: #blender cannot play same animation on multiple rigs, so copies are made here
                  newAction = bpy.data.actions[focusedAction].copy()
                  newAction.name = focusedAction+' copy'+rig
                  actiondata=newAction
               rigObj.animation_data.action = actiondata
               ####Create NLA strips
               track = rigObj.animation_data.nla_tracks.new()
               newStrip = track.strips.new(actiondata.name, actiondata.frame_range[0], actiondata)
               rigObj.animation_data.action = None
               bpy.context.area.type = "NLA_EDITOR"
               bpy.ops.nla.actionclip_add(action=focusedAction)
               bpy.ops.anim.channels_clean_empty()
    bpy.ops.object.exportforunreal()

bpy.context.area.type = original_context