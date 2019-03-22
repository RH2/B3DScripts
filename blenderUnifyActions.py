#blender unified animation system
#multiple rigs can use the same action
#frame handler 
#bones with the same name can possibly cause trouble.
import bpy
import datetime
S_time =  datetime.datetime.now()
print("---Unifying Actions  ::: "+str(S_time)+"---")

rigList=[
'rig1',
'rig2',
'rig3',
'rig4']

actionCopies=[]
specialAction='MainAction'
specialActionData = bpy.data.actions[specialAction]
specialActionData.use_fake_user = True
lastActiveObject = None
for rig in rigList: #setup: create copy of action and assign copies rigs in the list.
    rigData = bpy.data.objects[rig]
    newActionCopy = specialActionData.copy()
    actionCopies.append(newActionCopy)
    rigData.animation_data_clear()
    rigData.animation_data_create()
    rigData.animation_data.action = newActionCopy
def cleanUnusedActions():
    for action in bpy.data.actions:
        if(action.users==0):
            bpy.data.actions.remove(action)
def checkIfActiveIsImportant(inputList):
    for listString in inputList:
        if(bpy.context.active_object.name==listString):
            return(true)
        else:
            return(false)
def unify_actionSwap(objA, objB):
    if(checkIfActiveIsImportant(rigList)):
        actionAa= objA.action
        actionB= objB.action
        objA.action = specialActionData
        objB.action = actionA
def unify_actionCopy():
    if(checkIfActiveIsImportant(rigList)):
        currentAction = bpy.context.active_object.action
        for index,actionCopy in enumerate(actionCopies):
            actionCopy = currentAction.copy()
            if rigList[index]!=bpy.context.active_object:
                riglist[index].action = actionCopy
def unfiyAction_handler(scene):
    activeObject = bpy.context.activeObject
    if(checkIfActiveIsImportant(rigList)):
        if(lastActiveRig!=None):
            if(activeObject==lastActiveObject):
                unify_actionCopy()
            else:
                unify_actionSwap(bpy.context.active_object,lastActiveRig)                
        lastActiveRig=bpy.context.active_object
    lastActiveObject = bpy.context.activeObject
    #print("Frame Change", scene.frame_current)
    print("scene_update_post: "+str(S_time))
    cleanUnusedActions()

def register():
    bpy.app.handlers.scene_update_post.append(unfiyAction_handler)

def unregister():
    bpy.app.handlers.scene_update_post.remove(unfiyAction_handler)
    


