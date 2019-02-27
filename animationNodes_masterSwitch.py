import bpy

switch = False

for node in bpy.data.node_groups:
    if node.bl_idname=='an_AnimationNodeTree':
        node.autoExecution.sceneUpdate =switch
        node.autoExecution.treeChanged =switch
        node.autoExecution.frameChanged =switch
        node.autoExecution.propertyChanged =switch
        

