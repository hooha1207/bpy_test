#pose mode에서 merge 시키고자 하는 bone을 select로 설정한다
#merge 기준이 되는 bone의 경우 active select로 설정한다
#해당 스크립트를 실행한다

import bpy
import numpy as np



delete_stretch_bone = True


add_middle_stretch_n = 'process_middle_bone'





actob_n = bpy.context.object.name
selob_n = [i.name for i in bpy.context.selected_objects if not i.name == actob_n]

middle_bn = bpy.context.active_bone.name
circle_bn = [i.name for i in bpy.context.selected_pose_bones if middle_bn != i.name]


add_middle_stretch_head = np.array([0.0,0.0,0.0])
add_middle_stretch_num = 0
for cbn in circle_bn:
    add_middle_stretch_head += np.array(bpy.data.objects[actob_n].pose.bones[cbn].head)
    add_middle_stretch_num += 1

add_middle_stretch_mean_head = add_middle_stretch_head / add_middle_stretch_num


for ob in selob_n:
    vgroup_A_name = middle_bn
    ob = bpy.data.objects[ob]
    vgroup = ob.vertex_groups[vgroup_A_name]
    
    for cbn in circle_bn:
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
        
        if delete_stretch_bone:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.data.objects[actob_n].data.edit_bones.remove(bpy.data.objects[actob_n].data.edit_bones[cbn])
            bpy.ops.object.mode_set(mode='POSE')

#    ob.vertex_groups[middle_bn].name = add_middle_stretch_n

#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.armature.bone_primitive_add(name = add_middle_stretch_n)
#bpy.ops.armature.select_linked()
#check_add_middle_stretch_n = bpy.context.selected_editable_bones[0].name
#bpy.data.objects[actob_n].data.edit_bones[check_add_middle_stretch_n].head = add_middle_stretch_mean_head
#bpy.data.objects[actob_n].data.edit_bones[check_add_middle_stretch_n].tail = bpy.data.objects[actob_n].data.edit_bones[middle_bn].head

#bpy.ops.object.mode_set(mode='POSE')
#cstrt = bpy.data.objects[actob_n].pose.bones[check_add_middle_stretch_n].constraints.new("STRETCH_TO")
#cstrt.target = bpy.data.objects[actob_n]
#cstrt.subtarget = middle_bn
