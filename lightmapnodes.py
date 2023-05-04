import bpy

#mode 0: add the nodes
#mode 1: set the image node to active
#mode 2: reload all images

mode = 2

# Get a reference to the node group by name
light_group = bpy.data.node_groups.get("lm_group")

# Check if the node group exists
if light_group is not None:
    # Do something with the node group
    print(f"Found node group '{light_group.name}' with {len(light_group.nodes)} nodes.")
else:
    print("Node group not found.")
    
    
    
    
# Get the selected object
if mode is 0:
    selected_obj = bpy.context.selected_objects[0]
    # Loop through all materials of the selected object
    for material_slot in selected_obj.material_slots:
        material = material_slot.material
        
        # Get the node tree of the material
        node_tree = material.node_tree
        if node_tree is None:
            break
        # Get reference to the existing output node
        output_node = node_tree.nodes.get("Output")

        # Create a new node group and add it to the node tree
        #new = bpy.ops.node.add_node(type="ShaderNodeGroup", use_transform=True, settings=[{"name":"node_tree", "value":"bpy.data.node_groups['lm_group']"}])
        newgroup  = node_tree.nodes.new(type='ShaderNodeGroup')
        newgroup.node_tree = light_group
        newgroup.name = "LIGHTMAP NODE"
        
        newgroup.location = (50, 0)
            
            
        #surface_node = output_node.inputs["Surface"].links[0].from_node
        bsdf_node = node_tree.nodes.get("Material")
        node_tree.links.new(bsdf_node.outputs["BSDF"], newgroup.inputs["Shader"])
        node_tree.links.new(newgroup.outputs["Shader"], output_node.inputs["Surface"])
        
        
        #select the image node
        image_node = None
        for node in newgroup.node_tree.nodes:
            if node.name == 'Image Texture':
                if node.image == bpy.data.images['lm']:
                    image_node = node
                    break
        
        # Iterate over the nodes in the group tree to find the "Image Texture" node
if mode is 1:
    image_node = None
    for node in newgroup.node_tree.nodes:
        if node.name == 'Image Texture':
            if node.image == bpy.data.images['lm']:
                image_node = node
                break

    # Select the image node
    image_node.select = True
    
if mode is 2:
    for image in bpy.data.images:
        image.reload()
