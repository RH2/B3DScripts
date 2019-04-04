#blender unified animation system
import bpy
import datetime
S_time =  datetime.datetime.now()
print("---Unifying Actions  ::: "+str(S_time)+"---")

rigList=['Cube.000','Cube.001']                             ### IMPORTANT STUFF GOES HERE ###
actionList=['jump','roll','spin','kick',"walk"]           ### IMPORTANT STUFF GOES HERE ###
activeAction = "jump"


#ACTION>RIG
#First, we create all appropriate actions; and assign fake users.
def initialize():
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
def assignToRigList(String_activeAction):
    for rigString in rigList:
        try:
            #if(bpy.data.objects[rigString].animation_data is None):
            #    bpy.data.objects[rigString].animation_data_create()
            #    bpy.data.objects[rigString].animation_data.action = bpy.data.actions[activeAction+"_"+rigString]
            bpy.data.objects[rigString].animation_data.action = bpy.data.actions[activeAction+"_"+rigString]
        except KeyError:
            print("AssignToRigList: Rig Does Not Exist")
def GET_activeAction():
    return(activeAction)
initialize()
def UNIFY_UPDATE():
    activeAction=GET_activeAction()
    print(activeAction)
    #if active object belongs to the rigList, set all other objects on rigList to activeAction
    if(bpy.context.active_object is not None and existCheck2(bpy.context.active_object.name,rigList)):
        activeObjectName= bpy.context.active_object.name
        if(bpy.data.objects[activeObjectName].animation_data.data is not None):
            #print(activeAction)
            activeAction_2=str.split(bpy.data.objects[activeObjectName].animation_data.action.name,"_")[0]
            if(activeAction != activeAction_2):
                for rigString in rigList:
                    try:
                        bpy.data.objects[rigString].animation_data_create()
                        bpy.data.objects[rigString].animation_data.action = bpy.data.actions[activeAction+"_"+rigString]
                    except KeyError:
                        print("UPDATE: Rig Does Not Exist")
                activeAction=activeAction_2


#interval time update! :D
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            UNIFY_UPDATE()
        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
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
