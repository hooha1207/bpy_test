#선택된 bone 중에서 parent가 selected_pose_bones 리스트 내에 없고,
#child가 selected_pose_bones 리스트 내에 있다면
#parent bone의 vertex group에 child bone의 vertex group을 병합한다

import bpy
import numpy as np



bone_delete = True
bone_hide = True
bone_deform = True

add_middle_stretch_n = 'process_middle_bone'





actob_n = bpy.context.object.name
selob_n = [i.name for i in bpy.context.selected_objects if not i.name == actob_n]

middle_bn = []
for pb in bpy.context.selected_pose_bones:
    if not pb.parent in bpy.context.selected_pose_bones:
        middle_bn.append(pb.name)
    elif pb.parent in bpy.context.selected_pose_bones:
        continue


for ob in selob_n:
    for mbn in middle_bn:
        vgroup_A_name = mbn
        if type(ob) == type('str'):
            ob = bpy.data.objects[ob]
        vgroup = ob.vertex_groups[vgroup_A_name]
        
        for cbn in bpy.data.objects[actob_n].pose.bones[vgroup_A_name].children:
            if cbn in bpy.context.selected_pose_bones:
                vgroup_B_name = cbn.name
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
                
                ob.vertex_groups.remove(ob.vertex_groups[vgroup_B_name])
                
                if not bone_deform:
                    bpy.data.objects[actob_n].pose.bones[vgroup_B_name].bone.use_deform = False
                if bone_hide:
                    bpy.data.objects[actob_n].pose.bones[vgroup_B_name].bone.hide = True
                
                if bone_delete:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.data.objects[actob_n].data.edit_bones.remove(bpy.data.objects[actob_n].data.edit_bones[vgroup_B_name])
                    bpy.ops.object.mode_set(mode='POSE')
