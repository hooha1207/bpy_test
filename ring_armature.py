import bpy
import numpy as np
import bmesh

threshold = 0.04
add_amarture_name = 'hair_card_Armature'
add_bone_name = 'hair_card_bone'

bone_size = 0.08
rebatch = -(0.5-bone_size/2)







actob = bpy.context.active_object #mesh_object
mesh_object_n = actob.name

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(actob.data)

bm.edges.ensure_lookup_table()
sel_edge_idx = [i.index for i in bm.edges if i.select][0]
start_middle_vector = (bm.edges[sel_edge_idx].verts[0].co + bm.edges[sel_edge_idx].verts[1].co) / 2


bpy.ops.mesh.loop_multi_select(ring=True)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(actob.data)

sel_ringedge_idx = [i.index for i in bm.edges if i.select]
sel_ringverts_idx = []
for i in bm.edges:
    if i.select:
        print(i.verts)
        sel_ringverts_idx +=[i.verts]

print(sel_ringverts_idx)

tmp = {}
for edge in [i for i in bm.edges if i.select]:
    middle_v = ((edge.verts[0].co + edge.verts[1].co)/2)
    distance = ((edge.verts[0].co + edge.verts[1].co)/2) - start_middle_vector
    distance = (distance[0]**2 + distance[1]**2 + distance[2]**2)**1/2
    if distance == 0.0:
        first_edge_idx = edge.index
    another_edges = [i for i in edge.verts[0].link_edges if not i.index == edge.index]
    
    #find_nearest_ring_edge
    averts_ring = []
    for aedge in another_edges:
        for averts in aedge.verts:
            for av_edge in averts.link_edges:
                if av_edge.index in sel_ringedge_idx and not av_edge in averts_ring and edge != av_edge:
                    averts_ring.append(av_edge)
    if distance != 0.0 and len(averts_ring) == 1:
        last_edge_idx = edge.index
    tmp[edge.index] = [middle_v, [edge.verts[0].index], [edge.verts[1].index], averts_ring]

#print(tmp)


sort_edge = []
sort_edge.append(first_edge_idx)

print(first_edge_idx)


use_index = first_edge_idx
for i in range(len(tmp.keys())-1):
    for redge in tmp[use_index][-1]:
         if not redge.index in sort_edge:
             use_index = redge.index
             sort_edge.append(redge.index)


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.armature_add()
bpy.context.active_object.name = add_amarture_name
check_add_armature_n = bpy.context.active_object.name

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_more()
bpy.context.selected_editable_bones[0].name = add_bone_name



head_move = False
first = True
before_co = None
for edgeidx in sort_edge:
    if first:
        bpy.data.objects[add_amarture_name].data.edit_bones[0].head = tmp[edgeidx][0]
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = add_bone_name)
        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        head_move = True
        first = False
#        print(tmp[edgeidx][0])
    elif head_move:
        bpy.data.objects[add_amarture_name].data.edit_bones[0].tail = tmp[edgeidx][0]
        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        head_move = False
        bpy.data.objects[add_amarture_name].data.edit_bones[0].select_head = False
        bpy.data.objects[add_amarture_name].data.edit_bones[0].select = False
#        print(tmp[edgeidx][0])
    else:
        bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value":tmp[edgeidx][0] - before_co})
        bpy.ops.armature.select_more()
        vg_n = bpy.context.selected_editable_bones[0].name
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = vg_n)
#        check_add_vg_n = vg.name
        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].parent.select_tail = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].select = False
#        print(tmp[edgeidx][0])
