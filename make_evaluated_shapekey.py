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

# print('\n')
# print(vvs)
# print(tvs)
# print(modfvs)



for idx, v in enumerate(sk.data):
#    v.co = modfvs[idx]
    v.co.x = modfvs[idx][0]
    v.co.y = modfvs[idx][1]
    v.co.z = modfvs[idx][2]

bpy.context.active_object.data.shape_keys.key_blocks[skn].value = 1.0


# 기존 스크립트인 sign_shapekey_visibility 의 여러 번 실행해서 최종 결과값을 얻어야 되는 문제점을 해결하지 못했다
# 해당 문제점의 의심되는 원인으로는 bone의 행렬 연산을 고려해서 vertex를 이동하지 않았기 때문이라 생각함
# 이를 해결하려면 해당하는 vertex에 아래 식을 전개해야 된다
# 해당 vertex를 움직이는 bone의 weight * (해당 bone의 scale matrix/2) * ((target_v - vis_vert) * 해당 bone의 rotation matrix) * 해당 bone의 location matrix
# 위 과정을 거치기 위한 컴퓨팅 파워가 적절하지 않다 판단해 현재 이렇게 구현해놨으나,
# 추후 해당 과정을 거치는게 보다 합리적이다 판단되면 수정할 예정

# ex) visibility vertex를 기준으로 target vertex와 차이점을 구해서 shapekey에 해당 값만큼 vertex를 이동시켰을 때,
# 해당 vertex가 bone의 scale로 이동했다 가정하면 shapekey로 움직이는 vertex 이동량이 반감되어야 되지만
# 현 스크립트는 이를 고려하지 않고 움직이므로 결과적으로 적절한 값을 얻을 수 없게 된다

# ex) 위와 같은 상황일 때
# 해당 vertex가 bone의 rotation 90으로 이동했다 가정하면 (target_v - vis_vert) 벡터에 rotation matrix를 곱해야 되지만,
# 현 스크립트는 이를 고려하지 않고 움직이므로 결과적으로 해당 스크립트를 실행하면 실행할수록 오차가 심하게 된다