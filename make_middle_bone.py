#mesh의 out curve와 middle curve를 만든다
#curve to bone을 실행해준다
#middle bone에 대칭되어 생성된 bone의 경우 이름 중 bone을 middle로 바꿔준다
#이후 posemode에서 middle과 out에 대칭되는 bone을 선택해서 해당 코드를 실행한다


import bpy




actob_n = bpy.context.object.name

middle_b = [i for i in bpy.context.selected_pose_bones if 'middle' in i.name]
circle_b = [i for i in bpy.context.selected_pose_bones if not 'middle' in i.name]

bpy.ops.object.mode_set(mode='OBJECT')

scalar = {}

for cbone in circle_b:
    min = 10000
    mbn = ''
    min_loc = 0
    ht_bool = False
    for mbone in middle_b:
        if min >= abs(cbone.tail[0] - mbone.head[0]) + abs(cbone.tail[1] - mbone.head[1]) + abs(cbone.tail[2] - mbone.head[2]):
            min = abs(cbone.tail[0] - mbone.head[0]) + abs(cbone.tail[1] - mbone.head[1]) + abs(cbone.tail[2] - mbone.head[2])
            mbn = mbone.name
            min_loc = mbone.head
            ht_bool = False
        if min > abs(cbone.tail[0] - mbone.tail[0]) + abs(cbone.tail[1] - mbone.tail[1]) + abs(cbone.tail[2] - mbone.tail[2]):
            min = abs(cbone.tail[0] - mbone.tail[0]) + abs(cbone.tail[1] - mbone.tail[1]) + abs(cbone.tail[2] - mbone.tail[2])
            mbn = mbone.name
            min_loc = mbone.tail
            ht_bool = True
    
    scalar[f'{cbone.name}'] = [mbn, ht_bool, min_loc]



for cbone in scalar:
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.data.objects[actob_n].pose.bones[cbone].bone.select_tail = True
    ex_loc = scalar[cbone][-1]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0,0,0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'FACE'}, "use_snap_project":True, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.armature.select_more()
    bpy.context.selected_editable_bones[0].tail = ex_loc
    add_bone = bpy.context.selected_editable_bones[0].name
    
    bpy.ops.object.mode_set(mode='POSE')
    cstrt = bpy.data.objects[actob_n].pose.bones[add_bone].constraints.new("STRETCH_TO")
    cstrt.target = bpy.data.objects[actob_n]
    cstrt.subtarget = scalar[cbone][0]
    cstrt.volume = "NO_VOLUME"
    if scalar[cbone][1]:
        cstrt.head_tail = 1


