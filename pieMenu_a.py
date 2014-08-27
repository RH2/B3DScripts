import bpy
from bpy.types import Menu
print("RUNNING")
# spawn an edit mode selection pie (run while object is in edit mode to get a valid output)


class VIEW3D_PIE_selectMode(Menu):
    bl_label = "Select Mode"
    bl_idname= "mesh.selectMode"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator_enum("mesh.select_mode", "type")
class VIEW3D_PIE_edgeOps(Menu):
    bl_label = "Seam/Sharp/Remove"
    bl_idname= "mesh.edgeOps"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("mesh.mark_seam", "+ seam").clear = False
        pie.operator("mesh.mark_seam", "- seam").clear = True
        pie.operator("mesh.mark_sharp", "- sharp").clear = True
        pie.operator("mesh.mark_sharp", "+ sharp").clear = False
        pie.operator("mesh.remove_doubles")

class VIEW3D_PIE_object_exportOptions(Menu):
    bl_label = "Export"
    #bl_context = "objectmode"
    def draw(self, context):
        layout = self.layout
        newContext = bpy.context.selected_objects
        pie = layout.menu_pie() 
        #pie.operator("export_scene.fbx","FBX")
        #pie.operator("export_scene.obj","OBJ")
        #pie.operator("wm.collada_export","DAE")
        #pie.operator("export_mesh.stl","STL")      
        if context.active_object:
            if(context.mode == 'EDIT_MESH'):
                pie.operator("export_scene.fbx","FBX")
                pie.operator("export_scene.obj","OBJ")
                pie.operator("wm.collada_export","DAE")
                pie.operator("export_mesh.stl","STL")

                #pie.operator("MESH_OT_faces_shade_smooth")
                #pie.operator("MESH_OT_faces_shade_flat")
            else:
                pie.operator("OT_export_scene.fbx","FBX")
                #pie.operator("export_scene.obj","OBJ")
                #pie.operator("wm.collada_export","DAE")
                #pie.operator("export_mesh.stl","STL")

                #pie.operator("OBJECT_OT_shade_smooth")
                #pie.operator("OBJECT_OT_shade_flat")                 


def register():
    bpy.utils.register_class(VIEW3D_PIE_selectMode)  
    bpy.utils.register_class(VIEW3D_PIE_edgeOps)  
    bpy.utils.register_class(VIEW3D_PIE_object_exportOptions)  
     
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON5MOUSE","PRESS", shift=False,ctrl=False).properties.name="mesh.selectMode"
    kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON4MOUSE","PRESS", shift=False,ctrl=False).properties.name="mesh.edgeOps"
    kmi = km.keymap_items.new("wm.call_menu_pie", 'PAGE_UP',"PRESS", shift=False,ctrl=False).properties.name="VIEW3D_PIE_object_exportOptions"
def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_selectMode)
    bpy.utils.unregister_class(VIEW3D_PIE_edgeOps)  
    bpy.utils.unregister_class(VIEW3D_PIE_object_exportOptions) 
if __name__ == "__main__":
    register()