import bpy
import bmesh


add_armature_name = 'ring_to_armature'
add_bone_name = 'ring_to_bone'


actob = bpy.context.active_object
actob_n = actob.name

bm = bmesh.from_edit_mesh(actob.data)
#bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()



seledge = [i for i in bm.edges if i.select]
actedge = bm.select_history.active

start_act_v = None
for av in bm.select_history.active.verts:
    if len([i for i in av.link_edges if i.select]) == 1:
        start_act_v = av



sort_edges = []

start_edge = actedge
start_vert = start_act_v


#print('\n')
while not len(sort_edges) == len(seledge):
    current_edge = [i for i in start_vert.link_edges if not i in sort_edges and i in seledge][0]
    sort_edges.append(current_edge)
    start_vert = [i for i in current_edge.verts if i != start_vert][0]





sort_edges_idx = [i.index for i in sort_edges]

sort_edges_vco = {}
for edge in sort_edges:
    v_dic = {}
    for v in edge.verts:
        v_dic[v.index] = v.co
    sort_edges_vco[edge.index] = v_dic



use_v = []
use_v.append(start_act_v.index)


#print(sort_edges_idx)
#print(use_v)
#print(sort_edges_vco)



add_arob = bpy.data.objects.new(add_armature_name, bpy.data.armatures.new(add_armature_name))
bpy.context.collection.objects.link(add_arob)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.view_layer.objects.active = add_arob
bpy.ops.object.mode_set(mode='EDIT')

cnt = 1

for edge in sort_edges_idx:
    if cnt == 1:
        vidx = [i for i in actob.data.edges[edge].vertices if not i in use_v]
        add_ebone = add_arob.data.edit_bones.new(add_bone_name)
        
        add_ebone.head = sort_edges_vco[edge][use_v[0]]
        add_ebone.tail = sort_edges_vco[edge][vidx[0]]
        before_tail = sort_edges_vco[edge][vidx[0]]
        
        check_addbone_n = add_ebone.name
        addb_vg = actob.vertex_groups.new(name = check_addbone_n)
        addb_vg.add(use_v, 1.0, 'REPLACE')
        addb_vg.add(vidx, 1.0, 'REPLACE')
        cnt -= 1
        
        use_v.append(vidx[0])
        
        before_addbone_n = check_addbone_n
    else:
        vidx = [i for i in actob.data.edges[edge].vertices if not i in use_v]
        add_ebone = add_arob.data.edit_bones.new(add_bone_name)
        add_ebone.parent = add_arob.data.edit_bones[before_addbone_n]
        
        add_ebone.head = before_tail
        add_ebone.tail = sort_edges_vco[edge][vidx[0]]
        before_tail = sort_edges_vco[edge][vidx[0]]
        
        check_addbone_n = add_ebone.name
        addb_vg = actob.vertex_groups.new(name = check_addbone_n)
        addb_vg.add(vidx, 1.0, 'REPLACE')
        
        use_v.append(vidx[0])
        
        before_addbone_n = check_addbone_n


modf = actob.modifiers.new(add_armature_name, "ARMATURE")
modf.object = add_arob
