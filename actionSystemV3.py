#blender unified animation system
#ONLY ARMATURES ALLOWED IN RIG LIST!
#ACTION>RIG
import bpy
import datetime
S_time =  datetime.datetime.now()
print("---Unifying Actions  ::: "+str(S_time)+"---")

rigList=['rig1','rig2','rig3',"rig4"]        ### IMPORTANT STUFF GOES HERE ###
actionList=['jump','roll','spin','kick',"walk"]   ### IMPORTANT STUFF GOES HERE ###
activeAction = ""
excludeRigs = []
#First, we create all appropriate actions; and assign fake users.
def UNIFY_INITIALIZE():
    startingActionList = []#create list of all action names:
    for action in bpy.data.actions:
        startingActionList.append(action.name)
    for actionName in actionList:#go through all possible combinations.
        for rigName in rigList:
            generatedActionName = actionName+"_"+rigName
            bFound = False
            for startingAction in startingActionList:#find match between collection of current actions and generated action name.
                if(generatedActionName==startingAction):
                    bFound = True
                    #if something is found, stop searching
                    break
            if(bFound==False):#if something needs to be done:
                #create action
                actionPointer = bpy.data.actions.new(generatedActionName)
                try:
                    #assign to rig
                    rigOBJ = bpy.data.objects[rigName]
                    if rigOBJ.animation_data is not None:
                        rigOBJ.animation_data_create().action=actionPointer
                        rigOBJ.animation_data.action=actionPointer
                        #add fake user
                        actionPointer.use_fake_user=True
                except KeyError:
                    print("Initialize: Rig Does Not Exist")
def existCheck(inputstring, inputarray):
    for index,item in enumerate(inputarray):
            splitArray1 = str.split(item,'_')
            for substring in splitArray1:
                if(substring == inputstring):
                    return(True)
    return(False)
def existCheck2(inputstring, inputarray):
    for item in inputarray:
        if(inputstring == item):
            return(True)
    return(False)
def UNIFY_UPDATE():
    activeObjectName = bpy.context.active_object.name
    activeObjectData = bpy.data.objects[activeObjectName]
    currentAction = ""
    bImportant = False
    for rig in rigList:
        if(activeObjectName==rig):
            bImportant=True
            break
    print("bImportant"+str(bImportant))
    if(bImportant):
        print("activeObjectData.animation_data is None: "+str(activeObjectData.animation_data is None))
        if(activeObjectData.animation_data is None):
            activeObjectData.animation_data_create()
        print("activeObjectData.animation_data.action is None: "+str(activeObjectData.animation_data.action is None))
        if(activeObjectData.animation_data.action is None):
            currentAction= actionList[0]
            activeObjectData.animation_data.action =bpy.data.actions[currentAction+"_"+activeObjectData.name]
        elif(activeObjectData.animation_data is not None and activeObjectData.animation_data.action is not None):
            currentAction = str.split(activeObjectData.animation_data.action.name,"_")[0]
        for rig in rigList:
            if rig in bpy.data.objects:
                bpy.data.objects[rig].animation_data_create()
                bpy.data.objects[rig].animation_data.action=bpy.data.actions[currentAction+"_"+rig]

def UNIFY_EXPORT():
    #context
    original_context = bpy.context.area.type
    #only touch relevent rigs.
    exportRigs = []
    exportRigs = rigList
    for rigExclusion in excludeRigs:
        exportRigs.remove(rigExclusion)
    for rig in rigList:
        #bpy.data.objects[rig].ExportEnum = "auto"
        bpy.data.objects[rig].ExportEnum = "export_recursive"
        bpy.data.objects[rig].exportActionEnum = "export_specific_list"
    for exclude in excludeRigs:
        bpy.data.objects[exclude].ExportEnum = "auto"
    #Remove all animation data (Clean Slate)
    for rig in rigList:
        rigObj = bpy.data.objects[rig]
        bpy.context.scene.objects.active = rigObj
        bpy.ops.object.updateobjaction()
        rigObj.animation_data_clear()
    #Export one action set at a time
    for focusedAction in actionList:
        for rig in rigList:
            rigObj = bpy.data.objects[rig]
            for actionCheckbox in rigObj.exportActionList:
                actionCheckbox.use = False
                bAction=False
                bRig=False
                for split in str.split(actionCheckbox.name,'_'):
                    if(split == focusedAction):
                        bAction=True
                    if(split == rig):
                        bRig=True
                if(bAction and bRig):
                    actionCheckbox.use = True
                    actionString = focusedAction+"_"+rig
                    rigObj.animation_data_clear()
                    rigObj.animation_data_create()
                    actiondata = bpy.data.actions[actionString]
                    rigObj.animation_data.action = actiondata
                    ####Create NLA strips
                    track = rigObj.animation_data.nla_tracks.new()
                    #newStrip = track.strips.new(actiondata.name, actiondata.frame_range[0], actiondata)
                    #rigObj.animation_data.action = None
                    #bpy.context.area.type = "NLA_EDITOR"
                    #bpy.ops.nla.actionclip_add(action=actionString)
                    #bpy.ops.anim.channels_clean_empty()
        bpy.ops.object.exportforunreal()
    bpy.context.area.type = original_context
def SAVEALLACTIONS():
    for action in bpy.data.actions:
        action.use_fake_user=True
#ease of life changes TODO: UNIFY_NEW("newActionName")
#ease of life changes TODO: UNIFY_COPY("oldActionName","newActionName")
UNIFY_INITIALIZE()
SAVEALLACTIONS()
UNIFY_UPDATE()
UNIFY_EXPORT()
