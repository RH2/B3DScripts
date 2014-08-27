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

class VIEW3D_OT_PIE_object_exportOptions(Menu):
    bl_label = "Quick Export"
    bl_idname = "object.exportpie"
    bl_context = "object"
    def draw(self, context):
        #newContext = bpy.context.selected_objects
        layout = self.layout
        pie = layout.menu_pie() 
        pie.operator("export_scene.fbx","FBX")
        pie.operator("export_scene.obj","OBJ")
        pie.operator("wm.collada_export","DAE")
        pie.operator("export_mesh.stl","STL")                    


def register():
    bpy.utils.register_class(VIEW3D_PIE_selectMode)  
    bpy.utils.register_class(VIEW3D_PIE_edgeOps)  
    bpy.utils.register_class(VIEW3D_OT_PIE_object_exportOptions)  
     
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh", space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON5MOUSE","PRESS", shift=False,ctrl=False).properties.name="mesh.selectMode"
    kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON4MOUSE","PRESS", shift=False,ctrl=False).properties.name="mesh.edgeOps"
    km2 = wm.keyconfigs.addon.keymaps.new(name="Object", space_type="VIEW_3D")
    kmi = km2.keymap_items.new("wm.call_menu_pie", 'PAGE_UP',"PRESS", shift=False,ctrl=False).properties.name="object.exportpie"
def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_selectMode)
    bpy.utils.unregister_class(VIEW3D_PIE_edgeOps)  
    bpy.utils.unregister_class(VIEW3D_OT_PIE_object_exportOptions) 
if __name__ == "__main__":
    register()