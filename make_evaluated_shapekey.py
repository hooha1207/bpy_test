import bpy
import bmesh


shapeKey_n = 'sign_shapekey'
from_mix = False



sk = bpy.context.active_object.shape_key_add(name=shapeKey_n, from_mix=from_mix)
skn = sk.name

depsgraph = bpy.context.evaluated_depsgraph_get()
vis_ob = bpy.context.active_object.evaluated_get(depsgraph)
vrange = range(len(vis_ob.data.vertices))


target_ob = [i for i in bpy.context.selected_objects if i!=bpy.context.active_object][0]




vvs = []
#vvs_x = []
#vvs_y = []
#vvs_z = []
for idx in vrange:
#    vvs_x.append(vis_ob.data.vertices[idx].co.copy().x)
#    vvs_y.append(vis_ob.data.vertices[idx].co.copy().y)
#    vvs_z.append(vis_ob.data.vertices[idx].co.copy().z)
    vvs.append([vis_ob.data.vertices[idx].co.copy().x, vis_ob.data.vertices[idx].co.copy().y, vis_ob.data.vertices[idx].co.copy().z])

tvs = []
#tvs_x = []
#tvs_y = []
#tvs_z = []
for idx in vrange:
#    tvs_x.append(target_ob.data.vertices[idx].co.copy().x)
#    tvs_y.append(target_ob.data.vertices[idx].co.copy().y)
#    tvs_z.append(target_ob.data.vertices[idx].co.copy().z)
    tvs.append([target_ob.data.vertices[idx].co.copy().x, target_ob.data.vertices[idx].co.copy().y, target_ob.data.vertices[idx].co.copy().z])




bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
bm.verts.ensure_lookup_table()

modfvs = []
#modfvs_x = []
#modfvs_y = []
#modfvs_z = []
for idx in vrange:
#    modfvs_x.append((bm.verts[idx].co + (tvs[idx] - vvs[idx])).copy().x)
#    modfvs_y.append((bm.verts[idx].co + (tvs[idx] - vvs[idx])).copy().y)
#    modfvs_z.append((bm.verts[idx].co + (tvs[idx] - vvs[idx])).copy().z)
    modfvs.append([bm.verts[idx].co.copy().x + tvs[idx][0] - vvs[idx][0], bm.verts[idx].co.copy().y + tvs[idx][1] - vvs[idx][1], bm.verts[idx].co.copy().z + tvs[idx][2] - vvs[idx][2]])

bpy.ops.object.mode_set(mode='OBJECT')

print('\n')
print(vvs)
print(tvs)
print(modfvs)



for idx, v in enumerate(sk.data):
#    v.co = modfvs[idx]
    v.co.x = modfvs[idx][0]
    v.co.y = modfvs[idx][1]
    v.co.z = modfvs[idx][2]

bpy.context.active_object.data.shape_keys.key_blocks[skn].value = 1.0

