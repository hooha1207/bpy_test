#bone의 head가 위치할 mesh edge를 선택한 다음, 해당 스크립트를 실행하면,
#bone과 weight paint가 생성된다
#뿐만 아니라, edge를 선택할 때 연결된 여러 edge를 선택해도 된다

import bpy
import bmesh
import mathutils
import math
import numpy as np

add_modifier = True


add_amarture_name = 'hair_card_Armature'
add_bone_name = 'hair_card_bone'






print('\n')

actob = bpy.context.active_object #mesh_object
mesh_object_n = actob.name



bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(actob.data)

bm.edges.ensure_lookup_table()
sel_edge_idx = bm.select_history.active.index

sel_ringedge_idx = [i.index for i in bm.edges if i.select]


# edge를 input하면 선택된 edge 중 input edge와 link 되어있는 edge를 찾아 fle_list에 index 형태로 append한다
def find_link_edges(edge):
    if not edge.index in fle_list:
        fle_list.append(edge.index)
    edges = [i for i in edge.verts[0].link_edges if i != edge and i.select and not i.index in fle_list]
    for j in [i for i in edge.verts[1].link_edges if i != edge and i.select and not i.index in fle_list]:
        edges.append(j)
    for k in edges:
        fle_list.append(k.index)
    if len(edges) > 0:
        for i in edges:
            find_link_edges(i)
edge = bm.edges[sel_edge_idx]
fle_list = []
find_link_edges(edge)
sel_edge_idx_le = fle_list
del fle_list

start_middle_vector = bm.edges[0].verts[0].co - bm.edges[0].verts[0].co
for i in sel_edge_idx_le:
    start_middle_vector += bm.edges[i].verts[0].co
    start_middle_vector += bm.edges[i].verts[1].co
start_middle_vector = start_middle_vector / (len(sel_edge_idx_le) *2)






bm.edges.ensure_lookup_table()

#edge_idx : link_edge
edge_dic = {}

for edge_i in sel_ringedge_idx:
    start = True
    for k in edge_dic:
        if edge_i in [i.index for i in edge_dic[k]]:
            start=False
            break
    if start:
        fle_list = []
        find_link_edges(bm.edges[edge_i])
        edge_dic[edge_i] = [bm.edges[i] for i in fle_list]

for _ in edge_dic:
    print('edge_dic_key',_)
    print([i.index for i in edge_dic[_]])



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
#    print(distance)
    if distance < before_distance:
        before_distance = distance
        first_edge_idx = edge_dic_k
    another_edges = [i for i in edges[0].verts[0].link_edges if not i in edges]
    
    for edge_dic_k1 in edge_dic:
        if edges[0] in edge_dic[edge_dic_k1]:
            connect_edge = edge_dic[edge_dic_k1]
#    print('connect_edge', [i.index for i in connect_edge])
#    print('edges', edges[0].index)
#    print('another_edge',[i.index for i in another_edges])
    
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
    link_face_normal = mathutils.Vector((0,0,0))
    lface_count = 0
    for i in edges:
        for j in i.link_faces:
            link_face_normal += j.normal
            lface_count += 1
    link_face_normal = link_face_normal / lface_count
    edges = [i.index for i in edges]
#    print('averts_ring', averts_ring)
    tmp[edge_dic_k] = [middle_v, edges, link_face_normal, averts_ring]


#print('tmp',tmp)
sort_edge = []
sort_edge.append(first_edge_idx)



use_index = first_edge_idx
for i in range(len(tmp.keys())-1):
    
    averts_idx = tmp[use_index][-1]
    
#    print(use_index)
    use_index = [i for i in averts_idx if not i in sort_edge][0]
    sort_edge.append(use_index)
#    print(use_index)


print('sort_edge', sort_edge)


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
#    일단 bone의 z_axis를 추출해서 face normal과 내적을 통해 cos 섹터 값을 추출한다
#    구한 cos 섹터 값을 arccos 연산으로 radius 각도로 만들어준다
#    이후 ( 180 / pi ) 를 곱해 degrees 값으로 변환한다

#    이때 추출한 bone axis vector와 normal vector는 단위 vector이기 때문에 내적 값을 구할 수 있음
    if first:
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].head = tmp[edgeidx][0]
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = add_bone_name)
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].name = vg.name
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
        head_move = True
        first = False
#        print(tmp[edgeidx][0])
#        print('a')
    elif head_move:
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].tail = tmp[edgeidx][0]

        bpy.data.objects[check_add_armature_n].data.edit_bones[0].roll = 0
        normal = tmp[edgeidx][2]
        roll = bpy.data.objects[check_add_armature_n].data.edit_bones[0].z_axis
#        roll_value = (normal.x*roll.x+normal.y*roll.y+normal.z*roll.z) / ((normal.x**2+normal.y**2+normal.z**2)**1/2 * (roll.x**2+roll.y**2+roll.z**2)**1/2)
        roll_value = math.acos(np.dot(normal, roll))
        if tmp[edgeidx][2].x <0:
            bpy.data.objects[check_add_armature_n].data.edit_bones[0].roll = -1 *roll_value
        else:
            bpy.data.objects[check_add_armature_n].data.edit_bones[0].roll = roll_value
        
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        head_move = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].select_head = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[0].select = False
#        print(tmp[edgeidx][0])
#        print('b')
    else:
        bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value":tmp[edgeidx][0] - before_co})
        bpy.ops.armature.select_more()
        vg_n = bpy.context.selected_editable_bones[0].name

        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].roll = 0
        normal = tmp[edgeidx][2]
        roll = bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].z_axis
#        roll_value = (normal.x*roll.x+normal.y*roll.y+normal.z*roll.z) / ((normal.x**2+normal.y**2+normal.z**2)**1/2 * (roll.x**2+roll.y**2+roll.z**2)**1/2)
        roll_value = math.acos(np.dot(normal, roll))
        if tmp[edgeidx][2].x <0:
            bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].roll = -1*roll_value
        else:
            bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].roll = roll_value
        
        vg = bpy.data.objects[mesh_object_n].vertex_groups.new(name = vg_n)
        for edge_l in tmp[edgeidx][1]:
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[0]], 1.0, "REPLACE")
            vg.add([bpy.data.objects[mesh_object_n].data.edges[edge_l].vertices[1]], 1.0, "REPLACE")
        before_co = tmp[edgeidx][0]
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].parent.select_tail = False
        bpy.data.objects[check_add_armature_n].data.edit_bones[vg_n].select = False
#        print(tmp[edgeidx][0])
#        print('c')


bpy.ops.object.mode_set(mode='OBJECT')
if add_modifier:
    mod = actob.modifiers.new("ring_armature","ARMATURE")
    mod.object = bpy.data.objects[check_add_armature_n]
bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = actob
bpy.ops.object.mode_set(mode='EDIT')
