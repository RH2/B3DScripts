import bpy
import math
import random
import mathutils
import copy
from bpy.props import BoolProperty
from bpy_extras.io_utils import unpack_list

print("running")
def main(context):
    print("hello this is main")
def createFromObjName(context):
    selection = copy.copy(bpy.context.selected_objects)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in selection:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=str(ob.name))
        if not str(ob.name) in bpy.data.groups:
            bpy.ops.group.create(name=str(ob.name))
def selectedToActive(context):
    if (bpy.context.active_object.dupli_type == 'GROUP'):
        if hasattr(bpy.context.active_object.dupli_group, "name"):
            GroupType = bpy.context.active_object.dupli_group
            for ob in bpy.context.selected_objects:
                ob.dupli_type='GROUP'
                ob.dupli_group = GroupType 
def ObjNameToGroupName(context):
    for go in bpy.data.groups:
        if go.users==1:
            for ob in go.objects:
                if hasattr(ob, "name"):
                    go.name=ob.name
                    
                else:
                    print("object had no name")
def selectedToRandomish(context):
    print("not implemented yet foo!")

#----------------------------------------------------------
class GroupToolsPanel(bpy.types.Panel):
    bl_label = "Group Tools"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.operator("object.new_groups",icon="STICKY_UVS_DISABLE")
        row=layout.row()
        row.operator("object.group_imitate_active",icon="STICKY_UVS_DISABLE")
        row=layout.row()
        row.operator("object.group_rename_to_active",icon="STICKY_UVS_DISABLE")
        row=layout.row()
        row.operator("object.group_random",icon="STICKY_UVS_DISABLE")
class OBJECT_OT_groupFromName(bpy.types.Operator):
    '''for each object in selection, create a group with objects name'''
    bl_idname = "object.new_groups"
    bl_label = "New Groups"
    @classmethod
    def poll(cls,context):
        return context.active_object is not None 
    def execute(self,context):
        createFromObjName(context)
        return{'FINISHED'}
class OBJECT_OT_activeGroup(bpy.types.Operator):
    '''each selected dupligroup object set to same dupligroup as active object'''
    bl_idname = "object.group_imitate_active"
    bl_label = "imitate active"
    @classmethod
    def poll(cls,context):
        return context.active_object is not None 
    def execute(self,context):
        selectedToActive(context)
        return{'FINISHED'}
class OBJECT_OT_renameFromObjName(bpy.types.Operator):
    '''active object group = active object.name'''
    bl_idname = "object.group_rename_to_active"
    bl_label = "group = obj name"
    @classmethod
    def poll(cls,context):
        return context.active_object is not None 
    def execute(self,context):
        ObjNameToGroupName(context)
        return{'FINISHED'}
class OBJECT_OT_activeSet(bpy.types.Operator):
    '''figures out prop set and then does: dupligroup=set[random]'''
    bl_idname = "object.group_random"
    bl_label = "imitate randomized"
    @classmethod
    def poll(cls,context):
        return context.active_object is not None 
    def execute(self,context):
        selectedToRandomish(context)
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    bpy.utils.register_class(OBJECT_OT_groupFromName)
    bpy.utils.register_class(OBJECT_OT_activeGroup)
    bpy.utils.register_class(OBJECT_OT_renameFromObjName)
    bpy.utils.register_class(OBJECT_OT_activeSet)
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.utils.unregister_class(OBJECT_OT_groupFromName)
    bpy.utils.unregister_class(OBJECT_OT_activeGroup)
    bpy.utils.unregister_class(OBJECT_OT_renameFromObjName)
    bpy.utils.unregister_class(OBJECT_OT_activeSet) 
bpy.utils.register_module(__name__)
#if __name__ == "__main__":
#    register()