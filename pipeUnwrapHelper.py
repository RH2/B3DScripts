#Brute Force Pipe Unwrap
import bpy

print("--<<RUNNING>>--")
def main(context):
	print("----main----")
	#obj = bpy.context.object 
	#original_type = bpy.context.area.type
	obj = bpy.data.objects['BezierCurve.002']
	bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action="DESELECT")
	#bpy.context.area.type = "VIEW_3D"
	a = len(obj.data.polygons)
	for index in range(a):

		obj.data.polygons[index].select=True
		obj.data.polygons.active = index
		bpy.ops.mesh.select_linked_pick(deselect=True, limit=True)
		bpy.ops.uv.follow_active_quads('INVOKE_DEFAULT',mode='LENGTH_AVERAGE')
		#f.hide=False 
		#bpy.ops.mesh.reveal()
	bpy.ops.object.mode_set(mode = 'OBJECT')
	#bpy.context.area.type = original_type




class ToolsPanel(bpy.types.Panel):
	bl_label = "Pipe Unwrap (BRUTE FORCE)"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "scene"
	def draw(self, context):
		layout = self.layout
		row=layout.row()
		row.operator("object.unwrap_pipes",icon="FORCE_TEXTURE")



class OBJECT_OT_unwrapPipes(bpy.types.Operator):
	'''Click on ME'''
	bl_idname = "object.unwrap_pipes"
	bl_label = "Unwrap Pipes"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
def register():
	bpy.utils.register_module(__name__)
def unregister():
	bpy.utils.unregister_module(__name__)
if __name__ == "__main__":
	register()