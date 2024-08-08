import bpy
from mathutils import Vector, Matrix


rigob_n = bpy.context.active_object.name
rigob = bpy.data.objects[rigob_n]


infl_ob = bpy.data.objects['rig_MCH']

meshob_n = [i for i in bpy.context.selected_objects if i != rigob][0].name

depsgraph = bpy.context.evaluated_depsgraph_get()
meshob = depsgraph.objects[meshob_n]



selbn = [i.name for i in bpy.context.selected_pose_bones]


bpy.ops.object.mode_set(mode='EDIT')

info = {}
for bn in selbn:
    info[bn] = {}
    info[bn]['locx'] = rigob.data.edit_bones[bn].head.x
    info[bn]['locy'] = rigob.data.edit_bones[bn].head.y
    info[bn]['locz'] = rigob.data.edit_bones[bn].head.z


bpy.ops.object.mode_set(mode='OBJECT')

for bn in info:
    b_loc = Vector((info[bn]['locx'],info[bn]['locy'],info[bn]['locz']))
    before_dis = 9999999
    nearest_vid = 0
    for vid, v in enumerate(meshob.data.vertices):
        dis = (v.co - b_loc).length
        if dis < before_dis:
            before_dis = dis
            nearest_vid = vid
        
    info[bn]['Nvid'] = nearest_vid
    info[bn]['vgns'] = [meshob.vertex_groups[vg.group].name for vg in meshob.data.vertices[nearest_vid].groups]
    info[bn]['ws'] = [vg.weight for vg in meshob.data.vertices[nearest_vid].groups]



bpy.ops.object.mode_set(mode='POSE')

for bn in info:
    cstrt = rigob.pose.bones[bn].constraints.new('ARMATURE')
    for idx, vgn in enumerate(info[bn]['vgns']):
        cstrt_t = cstrt.targets.new()
        cstrt_t.target = infl_ob
        cstrt_t.subtarget = vgn
        cstrt_t.weight = info[bn]['ws'][idx]


"""
해당 스크립트는 bone과 mesh object를 선택해서 실행하면
bone에서 가장 가까운 vertex를 찾아 weight, vg를 추출해서
해당 정보를 기반으로 bone에 armature constraints를 추가한다

해당 스크립트는 shape2bone 스크립트와 사용하기 위해 만들었다
"""
