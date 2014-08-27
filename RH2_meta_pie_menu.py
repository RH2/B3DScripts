#GPL license
bl_info = {
    "name": "RH2 META PIE MENU",
    "author": "MKB, RH2",
    "version": (0, 1, 0),
    "blender": (2, 7, 2),
    "location": "View3D > PIE-MENU FOR META TOOLS",
    "description": "META > Collection of different Blender Addons",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "META"}
import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty

class VIEW3D_PIE_metaA(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "META 1"
    bl_idname = "meta.piemenuA"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.object         
        mesh = context.active_object.data               

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")            
####### Edit mode -------------------------------------------------
    #Blender read the Script from the top to the Bottom
    #if you delete as example Button >_3_Bottom < the following buttons slip up
        if ob.mode == 'EDIT_MESH':
            # Edit mode
            pie.operator("mesh.mark_seam", "+ seam").clear = False
            pie.operator("mesh.mark_seam", "- seam").clear = True
            pie.operator("mesh.mark_sharp", "- sharp").clear = True
            pie.operator("mesh.mark_sharp", "+ sharp").clear = False
            pie.operator("mesh.remove_doubles")                   



class VIEW3D_PIE_metaB(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "META 2"
    bl_idname = "meta.piemenuB"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.object         
        mesh = context.active_object.data               

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")               
####### Edit mode -------------------------------------------------
    #Blender read the Script from the top to the Bottom
    #if you delete as example Button >_3_Bottom < the following buttons slip up
        if ob.mode == 'EDIT_MESH':
            pie.operator_enum("mesh.select_mode", "type")                   



class VIEW3D_PIE_metaC(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "META 3"
    bl_idname = "meta.piemenuC"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.object         
        mesh = context.active_object.data               

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
####### Object mode -----------------------------------------------
        ob = context       
        if ob.mode == 'OBJECT':
            pie.operator("export_scene.fbx","FBX")
            pie.operator("export_scene.obj","OBJ")
            pie.operator("wm.collada_export","DAE")
            pie.operator("export_mesh.stl","STL")                  
####### Edit mode -------------------------------------------------
    #Blender read the Script from the top to the Bottom
    #if you delete as example Button >_3_Bottom < the following buttons slip up
        elif ob.mode == 'EDIT_MESH':
            pie.operator("export_scene.fbx","FBX")
            pie.operator("export_scene.obj","OBJ")
            pie.operator("wm.collada_export","DAE")
            pie.operator("export_mesh.stl","STL")                        


class VIEW3D_PIE_metaD(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "META 4"
    bl_idname = "meta.piemenuA"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.object         
        mesh = context.active_object.data               

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
####### Object mode -----------------------------------------------
        ob = context       
        if ob.mode == 'OBJECT':
            # Object mode

            #_1_Left
            pie.operator("object.align_location_all",text="Align Location", icon='MAN_TRANS')
            
            #_2_Right
            pie.operator("object.align_location_y",text="Align Loc. Y", icon='GROUP')            
            
            #_3_Bottom
            pie.operator("object.distribute_osc", text="Distribution", icon="ALIGN")           
             
            #_4_Top
            pie.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")            
                     
            #_5_Top_Left
            pie.operator("object.align_rotation_all",text="Align Rotation", icon='MAN_ROT')
            
            #_6_Top_Right
            pie.operator("object.align_location_x",text="Align Loc. X", icon='GROUP')            
   
            #_7_Bottom_Left
            pie.operator("object.align_objects_scale_all",text="Align Scale", icon='MAN_SCALE')             

            #_8_Bottom_Right
            pie.operator("object.align_location_z",text="Align Loc. Z", icon='GROUP')                 
####### Edit mode -------------------------------------------------
    #Blender read the Script from the top to the Bottom
    #if you delete as example Button >_3_Bottom < the following buttons slip up
        elif ob.mode == 'EDIT_MESH':
            # Edit mode

            #_1_Left
            pie.operator("object.loops7", "Ob-Mode", icon="LAYER_ACTIVE")
            
            #_2_Right
            pie.operator("mesh.face_align_y", "Flatten Y", icon="MOD_DISPLACE")            
                 
            #_3_Bottom
            pie.operator("view3d.ruler", text="Ruler", icon="CURVE_NCURVE") 
            
            #_4_Top
            pie.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")   
                        
            #_5_Top_Left
            pie.operator("object.loops9", "Ed-Mode", icon="LAYER_ACTIVE")   
            
            #_6_Top_Right
            pie.operator("mesh.face_align_x", "Flatten X", icon="MOD_DISPLACE")            

            #_7_Bottom_Left
            pie.operator("mesh.select_similar",text="Similar Mesh", icon="ORTHO")            

            #_8_Bottom_Right
            pie.operator("mesh.face_align_z", "Flatten Z", icon="MOD_DISPLACE")                       
####### Curve menu ------------------------------------------------
        if ob.mode == 'EDIT_CURVE':
            # Curve menu
            #_1_Left
            pie.operator("object.loops7", "Ob-Mode", icon="LAYER_ACTIVE")
            
            #_2_Right
            pie.operator("mesh.face_align_y", "Flatten Y", icon="MOD_DISPLACE")            
                 
            #_3_Bottom
            pie.operator("view3d.ruler", text="Ruler", icon="CURVE_NCURVE") 
            
            #_4_Top
            pie.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")   
                        
            #_5_Top_Left
            pie.operator("object.loops9", "Ed-Mode", icon="LAYER_ACTIVE")   
            
            #_6_Top_Right
            pie.operator("mesh.face_align_x", "Flatten X", icon="MOD_DISPLACE")            

            #_7_Bottom_Left
            pie.operator("mesh.select_similar",text="Similar Mesh", icon="ORTHO")            

            #_8_Bottom_Right
            pie.operator("mesh.face_align_z", "Flatten Z", icon="MOD_DISPLACE")             
####### Surface menu ----------------------------------------------     
        if ob.mode == 'EDIT_SURFACE':
            # Surface menu
            #_1_Left
            pie.operator("object.loops7", "Ob-Mode", icon="LAYER_ACTIVE")
            
            #_2_Right
            pie.operator("mesh.face_align_y", "Flatten Y", icon="MOD_DISPLACE")            
                 
            #_3_Bottom
            pie.operator("view3d.ruler", text="Ruler", icon="CURVE_NCURVE") 
            
            #_4_Top
            pie.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")   
                        
            #_5_Top_Left
            pie.operator("object.loops9", "Ed-Mode", icon="LAYER_ACTIVE")   
            
            #_6_Top_Right
            pie.operator("mesh.face_align_x", "Flatten X", icon="MOD_DISPLACE")            

            #_7_Bottom_Left
            pie.operator("mesh.select_similar",text="Similar Mesh", icon="ORTHO")            

            #_8_Bottom_Right
            pie.operator("mesh.face_align_z", "Flatten Z", icon="MOD_DISPLACE")            
####### Metaball menu ---------------------------------------------       
        if ob.mode == 'EDIT_METABALL':
            # Metaball menu
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Lattice menu ----------------------------------------------        
        elif ob.mode == 'EDIT_LATTICE':
            # Lattice menu
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Particle menu ---------------------------------------------          
        if  context.mode == 'PARTICLE':
            # Particle menu
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Weight paint menu -----------------------------------------                   
        ob = context  
        if ob.mode == 'PAINT_WEIGHT':
            # Weight paint menu
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Vertex paint menu -----------------------------------------                                    
        elif ob.mode == 'PAINT_VERTEX':
            # Vertex paint menu
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Texture paint menu ----------------------------------------                      
        elif ob.mode == 'PAINT_TEXTURE':
            # Texture paint menu 
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Sculpt menu -----------------------------------------------                       
        elif ob.mode == 'SCULPT':
            # Sculpt menu 
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Armature menu ---------------------------------------------              
        elif ob.mode == 'EDIT':
            # Armature menu 
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right
####### Pose mode menu --------------------------------------------           
        if context.mode == 'POSE':
            # Pose mode menu
            arm = context.active_object.data   
            pie.operator_enum("VIEW3D_MT_TransformMenu", icon='MANIPUL')
            #_1_Left
            #_2_Right
            #_3_Bottom
            #_4_Top
            #_5_Top_Left
            #_6_Top_Right
            #_7_Bottom_Left
            #_8_Bottom_Right                                   




###########################################################################################
###########################################################################################   
def abs(val):
    if val > 0:
        return val
    return -val
#in this template your hotkey will be under 3D View (Global)
#this is a global overide in the user preferences input 
#look for the names in the user preferences input for a other overide
def register():
    bpy.utils.register_class(VIEW3D_PIE_metaA)
    bpy.utils.register_class(VIEW3D_PIE_metaB)
    bpy.utils.register_class(VIEW3D_PIE_metaC)
    bpy.utils.register_class(VIEW3D_PIE_metaD)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_DOWN', 'PRESS').properties.name = "meta.piemenuD"
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_UP', 'PRESS').properties.name = "meta.piemenuC"        
        kmi = km.keymap_items.new('wm.call_menu_pie', 'BUTTON5MOUSE', 'PRESS').properties.name = "meta.piemenuB"
        kmi = km.keymap_items.new('wm.call_menu_pie', 'BUTTON4MOUSE', 'PRESS').properties.name = "meta.piemenuA"
def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_metaA)
    bpy.utils.unregister_class(VIEW3D_PIE_metaB)
    bpy.utils.unregister_class(VIEW3D_PIE_metaC)
    bpy.utils.unregister_class(VIEW3D_PIE_metaD)

   
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        
        #change here the Location of your Menu_2
        km = kc.keymaps['3D View']
        
        ##########################
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu_pie':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break              
if __name__ == "__main__":
    register()