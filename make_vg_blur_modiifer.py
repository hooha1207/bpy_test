import bpy



actob = bpy.context.active_object
selob = [i for i in bpy.context.selected_objects if i!=actob]

GeometryNodeTree_n = 'blur_vg'

interators = 10
weight = 1.0


for ob in selob:
    bpy.context.view_layer.objects.active = ob
    
    ### make geometry node
    # add node
    geometry_ng = bpy.data.node_groups.new(name=GeometryNodeTree_n, type='GeometryNodeTree')
    geometry_ng.use_fake_user = True

    n_input = geometry_ng.nodes.new(type="NodeGroupInput")
    n_input.location = (0,0)
    geometry_ng.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')

    n_output = geometry_ng.nodes.new(type="NodeGroupOutput")
    n_output.location = (700,0)
    geometry_ng.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    
    
    ### make modiifer
    modf = ob.modifiers.new(name='blur_vg',type='NODES')
    modf.node_group = geometry_ng
    
    loc_tmp = 0
    before_geo = n_input.outputs['Geometry']    
    for vg in ob.vertex_groups:
        
        vgn = vg.name
        
        before_socket_idx = len(n_input.outputs)
        interface_socket_idx = len(geometry_ng.interface.items_tree)
        
        vgn_in_socket = geometry_ng.interface.new_socket(name=vgn, in_out='INPUT', socket_type='NodeSocketString')
        iterator_in_socket = geometry_ng.interface.new_socket(name=vgn+'_iterators', in_out='INPUT', socket_type='NodeSocketInt')
        weight_in_socket = geometry_ng.interface.new_socket(name=vgn+'_weight', in_out='INPUT', socket_type='NodeSocketFloat')
        
        
        n_named = geometry_ng.nodes.new(type="GeometryNodeInputNamedAttribute")
        n_named.data_type = 'FLOAT'
        n_named.inputs[0].default_value = vgn
        n_named.location = (100,loc_tmp)
        
        n_blur = geometry_ng.nodes.new(type="GeometryNodeBlurAttribute")
        n_blur.location = (200,loc_tmp)
        
        n_store = geometry_ng.nodes.new(type="GeometryNodeStoreNamedAttribute")
        n_store.data_type = 'FLOAT'
        n_store.domain = 'POINT'
        n_store.inputs[2].default_value = vgn
        n_store.location = (300,loc_tmp)
        
        geometry_ng.links.new(n_input.outputs[before_socket_idx-1], n_named.inputs[0])
        geometry_ng.links.new(n_input.outputs[before_socket_idx], n_blur.inputs['Iterations'])
        geometry_ng.links.new(n_input.outputs[before_socket_idx+1], n_blur.inputs['Weight'])
        geometry_ng.links.new(before_geo, n_store.inputs['Geometry'])
        geometry_ng.links.new(n_named.outputs[1], n_blur.inputs[0])
        geometry_ng.links.new(n_blur.outputs[0], n_store.inputs[4])
        
        
        geometry_ng.interface.items_tree[interface_socket_idx].default_value = vgn
        geometry_ng.interface.items_tree[interface_socket_idx+1].default_value = interators
        geometry_ng.interface.items_tree[interface_socket_idx+2].default_value = weight
        modf[vgn_in_socket.identifier] = vgn
        modf[iterator_in_socket.identifier] = interators
        modf[weight_in_socket.identifier] = weight
        
        
        before_geo = n_store.outputs['Geometry']
        
        loc_tmp+=300
    
    
    # geometry node connect
    geometry_ng.links.new(n_output.inputs['Geometry'], n_store.outputs['Geometry'])
    
    
    # move modifier to top
    bpy.ops.object.modifier_move_to_index(modifier=modf.name,index=0)