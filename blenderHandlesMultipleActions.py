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
lastActiveObject = ""
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
            return(True)
        else:
            return(False)
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

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            activeObject = bpy.context.active_object
            if(checkIfActiveIsImportant(rigList)):
                if(activeObject==lastActiveObject):
                    unify_actionCopy()
                else:
                    unify_actionSwap(bpy.context.active_object,lastActiveRig)
                lastActiveRig=bpy.context.active_object
            lastActiveObject = bpy.context.active_object
            #print("Frame Change", scene.frame_current)
            print("scene_update_post: "+str(S_time))
            cleanUnusedActions()
        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
