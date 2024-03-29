#bone의 head가 위치할 mesh edge를 선택한 다음, 해당 스크립트를 실행하면,
#bone과 weight paint가 생성된다
#뿐만 아니라, edge를 선택할 때 연결된 여러 edge를 선택해도 된다

import bpy
import numpy as np
import bmesh

add_modifier = True


add_amarture_name = 'hair_card_Armature'
add_bone_name = 'hair_card_bone'








actob = bpy.context.active_object #mesh_object
mesh_object_n = actob.name

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(actob.data)

bm.edges.ensure_lookup_table()
sel_edge_idx = [i.index for i in bm.edges if i.select][0]
sel_edge_idx_le = [i.index for i in bm.edges if i.select]
start_middle_vector = bm.edges[0].verts[0].co - bm.edges[0].verts[0].co

for i in sel_edge_idx_le:
    start_middle_vector += bm.edges[i].verts[0].co
    start_middle_vector += bm.edges[i].verts[1].co

start_middle_vector = start_middle_vector / (len(sel_edge_idx_le) *2)



bpy.ops.mesh.loop_multi_select(ring=True)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(actob.data)

sel_ringedge_idx = [i.index for i in bm.edges if i.select]
sel_ringedge_idx_buf = sel_ringedge_idx.copy()

selsel_ringedge_idx_le = {}


print('\n')
bm.edges.ensure_lookup_table()

#edge_idx : link_edge
edge_dic = {}


for edge_i in sel_ringedge_idx_buf:
    
    for ve in edge_dic.values():
        if edge_i in list(set([i.index for i in ve])):
            continue
    find_last_link_l = []
    edge = bm.edges[edge_i]
    find_last_link_l.append(edge)
    ex_edge_l = [i for i in edge.verts[0].link_edges if i.index in sel_ringedge_idx and not i in find_last_link_l and edge != i]
    ex_edge_r = [i for i in edge.verts[1].link_edges if i.index in sel_ringedge_idx and not i in find_last_link_l and edge != i]
    while len(ex_edge_l) >= 1:
#        print(ex_edge[0].index)
        find_last_link_l.append(ex_edge_l[0])
        edge = ex_edge_l[0]
        ex_edge_l = [i for i in edge.verts[0].link_edges if i.index in sel_ringedge_idx and not i in find_last_link_l and edge != i]
    while len(ex_edge_r) >= 1:
#        print(ex_edge[0].index)
        find_last_link_l.append(ex_edge_r[0])
        edge = ex_edge_r[0]
        ex_edge_r = [i for i in edge.verts[1].link_edges if i.index in sel_ringedge_idx and not i in find_last_link_l and edge != i]
    if not set(find_last_link_l) in [set(i) for i in edge_dic.values()]:
        edge_dic[edge_i] = find_last_link_l



#sel_ringverts_idx = []
#for i in edge_dic:
#    bm.edges[i]
#    sel_ringverts_idx +=[i.verts]
print('edge_dic_k', edge_dic.keys())
print('edge_dic', [[j.index for j in i] for i in edge_dic.values()])

tmp = {}
before_distance = 99999.9
for edge_dic_k in edge_dic:
    
    edges = edge_dic[edge_dic_k]
    
    middle_v = bm.edges[0].verts[0].co - bm.edges[0].verts[0].co
    for edge_ in edges:
        middle_v += edge_.verts[0].co
        middle_v += edge_.verts[1].co
#        print(edge_.verts[0].co)
#        print(edge_.verts[1].co)
    middle_v = middle_v / (len(edges) * 2)
    distance = middle_v - start_middle_vector
    distance = (distance[0]**2 + distance[1]**2 + distance[2]**2)**1/2
    if distance < before_distance:
        before_distance = distance
        first_edge_idx = edge_dic_k
    another_edges = [i for i in edges[0].verts[0].link_edges if not i in edges]
    
    for edge_dic_k1 in edge_dic:
        if edges[0] in edge_dic[edge_dic_k1]:
            connect_edge = edge_dic[edge_dic_k1]
    print('connect_edge', [i.index for i in connect_edge])
    print('edges', edges[0].index)
    
    print('another_edge',[i.index for i in another_edges])
    
    #find_nearest_ring_edge
    averts_ring = []
    for aedge in another_edges:
        for averts in aedge.verts:
            if not averts in edges[0].verts:
                for av_edge in averts.link_edges:
                    if av_edge.index in sel_ringedge_idx and not av_edge in averts_ring and not av_edge in edges:
                        for edge_dic_k2 in edge_dic:
                            if av_edge in edge_dic[edge_dic_k2]:
                                av_edge = edge_dic_k2
                                break
                        if not av_edge in averts_ring:
                            averts_ring.append(av_edge)
#                        averts_ring.append(av_edge.index)
    if distance != 0.0 and len(another_edges) == 1:
        last_edge_idx = edge_dic_k
    edges = [i.index for i in edges]
    print('averts_ring', averts_ring)
    tmp[edge_dic_k] = [middle_v, edges, averts_ring]


print('tmp',tmp)
sort_edge = []
sort_edge.append(first_edge_idx)



use_index = first_edge_idx
for i in range(len(tmp.keys())-1):
    
    averts_idx = tmp[use_index][-1]
    
    print(use_index)
    use_index = [i for i in averts_idx if not i in sort_edge][0]
    sort_edge.append(use_index)
    print(use_index)
    
    
    
        
    
#    for tmp_k in tmp:
#        if use_index in tmp[tmp_k][-1]:
#            use_index = tmp_k
#    
#    for redge in tmp[use_index][-1]:
#        print('redge',redge)
#        for edge_dic_k3 in edge_dic:
#            if bm.edges[redge] in edge_dic[edge_dic_k3]:
#                redge = edge_dic_k3
#        if not redge in sort_edge:
#            sort_edge.append(redge)
#            print(tmp[use_index][-1])
#            print(use_index)

print('sort_edge', sort_edge)

#for ceis in sort_edge:
#    print(bm.edges[ceis].verts[0].co + bm.edges[ceis].verts[1].co)


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
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].head = tmp[edgeidx][0]
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = add_bone_name)
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].name = vg.name
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        head_move = True
        first = False
        print(tmp[edgeidx][0])
        print('a')
    elif head_move:
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].tail = tmp[edgeidx][0]
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        head_move = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].select_head = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].select = False
        print(tmp[edgeidx][0])
        print('b')
    else:
        bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value":tmp[edgeidx][0] - before_co})
        bpy.ops.armature.select_more()
        vg_n = bpy.context.selected_editable_bones[0].name
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = vg_n)
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][1], 1.0, "REPLACE")
#        vg.add(tmp[edgeidx][2], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].parent.select_tail = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].select = False
        print(tmp[edgeidx][0])
        print('c')


bpy.ops.object.mode_set(mode='OBJECT')
if add_modifier:
    mod = actob.modifiers.new("ring_armature","ARMATURE")
    mod.object = bpy.data.objects[check_add_armature_n]
bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = actob
bpy.ops.object.mode_set(mode='EDIT')
