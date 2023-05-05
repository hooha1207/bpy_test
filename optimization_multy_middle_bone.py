#middle stretch bone이 만들어진 bone은 active select로 설정
#vertex를 최적화시킬 mesh는 select로 설정
#armature의 pose mode로 진입하여 middle bone과 middle stretch bone을 선택하고 해당 스크립트 실행

import bpy
import numpy as np



delete_stretch_bone = True


tmp_stretch_n = 'tmp_stretch'
add_middle_stretch_n = 'process_middle_bone'





actob_n = bpy.context.object.name
selob_n = [i.name for i in bpy.context.selected_objects if not i.name == actob_n]

middle_b = [i for i in bpy.context.selected_pose_bones if 'middle' in i.name]
circle_b = [i for i in bpy.context.selected_pose_bones if not 'middle' in i.name]

bpy.ops.object.mode_set(mode='OBJECT')

scalar = {}

before_cbone_ht_bool = False

for cbone in circle_b:
    min = 10000
    mbn = ''
    min_loc = 0
    ht_bool = False
    for mbone in middle_b:
        if min >= abs(cbone.tail[0] - mbone.head[0]) + abs(cbone.tail[1] - mbone.head[1]) + abs(cbone.tail[2] - mbone.head[2]):
            min = abs(cbone.tail[0] - mbone.head[0]) + abs(cbone.tail[1] - mbone.head[1]) + abs(cbone.tail[2] - mbone.head[2])
            mbn = mbone.name
            min_loc = np.array(mbone.head)
            ht_bool = False
        if min > abs(cbone.tail[0] - mbone.tail[0]) + abs(cbone.tail[1] - mbone.tail[1]) + abs(cbone.tail[2] - mbone.tail[2]):
            if before_cbone_ht_bool:
                continue
            min = abs(cbone.tail[0] - mbone.tail[0]) + abs(cbone.tail[1] - mbone.tail[1]) + abs(cbone.tail[2] - mbone.tail[2])
            mbn = mbone.name
            min_loc = np.array(mbone.tail)
            ht_bool = True
    
    scalar[f'{cbone.name}'] = [mbn, ht_bool, min_loc]

tmp = 0

for obn in selob_n:
    for cbn in scalar:
        
        vgroup_A_name = scalar[cbn][0] #middle_bone_name
        ob = bpy.data.objects[obn]
        vgroup = ob.vertex_groups[vgroup_A_name]
        
        vgroup_B_name = cbn
        for id, vert in enumerate(ob.data.vertices):
            available_groups = [v_group_elem.group for v_group_elem in vert.groups]
            A = B = 0.0
            if ob.vertex_groups[vgroup_A_name].index in available_groups:
                A = ob.vertex_groups[vgroup_A_name].weight(id)
            if ob.vertex_groups[vgroup_B_name].index in available_groups:
                B = ob.vertex_groups[vgroup_B_name].weight(id)

            # only add to vertex group is weight is > 0
            sum = A + B
            vgroup.add([id], sum ,'REPLACE')
        
        ob.vertex_groups.remove(ob.vertex_groups[cbn])
        bpy.data.objects[actob_n].pose.bones[cbn].bone.use_deform = False


mb_addmiddle_stretch = {}

for obn in selob_n:
    for idx, mb in enumerate(middle_b):
        before_vg = [i.name for i in bpy.data.objects[obn].vertex_groups]
        bpy.data.objects[obn].vertex_groups[mb.name].name = add_middle_stretch_n
        after_vg = [i.name for i in bpy.data.objects[obn].vertex_groups]
        mb_addmiddle_stretch[mb.name] = f'{add_middle_stretch_n}_{idx}'
        mb_addmiddle_stretch[list(set(before_vg) - set(after_vg))[0]] = list(set(after_vg) - set(before_vg))[0]


n_scalar = {}

for cbn in scalar:
    n_scalar[cbn] = [mb_addmiddle_stretch[scalar[cbn][0]], scalar[cbn][1], scalar[cbn][2]]

print(n_scalar)


mbn_dic = {}

for cbn in scalar:
#    scalar[cbn][0] #mbn
#    scalar[cbn][1] #ht_bool
#    scalar[cbn][-1] #min_loc
    
    try:
        mbn_dic[scalar[cbn][0]] += np.array(bpy.data.objects[actob_n].pose.bones[cbn].head)
        mbn_dic[f'{scalar[cbn][0]}_tmp'] += 1
    except:
        mbn_dic[scalar[cbn][0]] = np.array(bpy.data.objects[actob_n].pose.bones[cbn].head)
        mbn_dic[f'{scalar[cbn][0]}_tmp'] = 1




for mbn in mbn_dic:
    if 'tmp' in mbn:
        continue
    add_middle_stretch_mean_head = mbn_dic[mbn] / mbn_dic[f'{mbn}_tmp']

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.bone_primitive_add(name = mb_addmiddle_stretch[mbn])
    bpy.ops.armature.select_linked()
    check_add_middle_stretch_n = bpy.context.selected_editable_bones[0].name
    bpy.data.objects[actob_n].data.edit_bones[check_add_middle_stretch_n].head = add_middle_stretch_mean_head
    bpy.data.objects[actob_n].data.edit_bones[check_add_middle_stretch_n].tail = bpy.data.objects[actob_n].data.edit_bones[mbn].head

    bpy.ops.object.mode_set(mode='POSE')
    cstrt = bpy.data.objects[actob_n].pose.bones[check_add_middle_stretch_n].constraints.new("STRETCH_TO")
    cstrt.target = bpy.data.objects[actob_n]
    cstrt.subtarget = mbn



bpy.ops.object.mode_set(mode='EDIT')
if delete_stretch_bone:
    for cbn in scalar:
        bpy.data.objects[actob_n].data.edit_bones.remove(bpy.data.objects[actob_n].data.edit_bones[cbn])

bpy.ops.object.mode_set(mode='POSE')
