#armature를 선택한 다음, 원하는 bone layer를 코드에 입력하고 해당 코드를 실행하면
#현재 레이어에 존재하는 모든 bone을 원하는 bone layer로 복사하는데,
#이때 복사된 bone은 기존에 존재하던 bone의 transform을 before origin (full)로 mix하여 제어할 수 있다
#local space로 설정한 이유는 spline ik의 경우 hook로 회전값을 부여할 수 없기 때문에 back bone이 필요해서다


import bpy


spline_bone_layer = 25

select_bone_layer = [  ] + [spline_bone_layer]

constraints_name = "spline_IK_hook_constraints"
add_bone_name = "transfer_transform"



actob_n = bpy.context.object.name


Bbone_layer = []
for i in range(len(bpy.context.object.data.layers)):
    if i in select_bone_layer:
        Bbone_layer.append(True)
    else:
        Bbone_layer.append(False)



bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
#If you want only selected bones to be control bones,
#modified here

select_bone_name = [i.name for i in bpy.context.selected_pose_bones]



for bone in select_bone_name:
    bone_location = bpy.data.objects[actob_n].pose.bones[bone].head
    bpy.ops.pose.select_all(action='DESELECT')
    if type(bpy.data.objects[actob_n].pose.bones[bone].parent) == type(None):
        add_bone_parent_name = f'{add_bone_name}_{bone}'
        bpy.ops.object.mode_set(mode='EDIT')
#        bpy.data.objects[actob_n].data.edit_bones[bone].select = True
        bpy.data.objects[actob_n].data.edit_bones[bone].select_head = True
        for child in bpy.data.objects[actob_n].data.edit_bones[bone].children:
            child.select_head = True
        bpy.ops.armature.select_linked()
        
        child_list = [i.name for i in bpy.context.selected_editable_bones if i.name != bone]
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        child_count = 0
        
        bpy.ops.object.mode_set(mode='POSE')
        for sel_bone in bpy.context.selected_pose_bones:
            if type(sel_bone.parent) == type(None):
                sel_bone.name = f'{add_bone_name}_{bone}'
                check_sel_bone_name = sel_bone.name
                
                
                cstrt = bpy.data.objects[actob_n].pose.bones[check_sel_bone_name].constraints.new("COPY_TRANSFORMS")
                cstrt.name = constraints_name
                cstrt.target = bpy.data.objects[actob_n]
                cstrt.owner_space = 'LOCAL'
                cstrt.target_space = 'LOCAL'
                cstrt.subtarget = bpy.data.objects[actob_n].data.bones[bone].name
                cstrt.mix_mode = 'BEFORE_FULL'
                bpy.ops.pose.bone_layers(layers=Bbone_layer)
                
            elif type(sel_bone.parent) != type(None):
                sel_bone.name = f'{add_bone_name}_{bone}'
                check_sel_bone_name = sel_bone.name
                
                if len(bpy.data.objects[actob_n].pose.bones[check_sel_bone_name].constraints) != 0:
                    for constraints in bpy.data.objects[actob_n].pose.bones[check_sel_bone_name].constraints:
                        bpy.data.objects[actob_n].pose.bones[check_sel_bone_name].constraints.remove(constraints)
                
                cstrt = bpy.data.objects[actob_n].pose.bones[check_sel_bone_name].constraints.new("COPY_TRANSFORMS")
                cstrt.name = constraints_name
                cstrt.target = bpy.data.objects[actob_n]
                cstrt.owner_space = 'LOCAL'
                cstrt.target_space = 'LOCAL'
                cstrt.subtarget = bpy.data.objects[actob_n].data.bones[child_list[child_count]].name
                cstrt.mix_mode = 'BEFORE_FULL'
                
                child_count += 1






for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False
