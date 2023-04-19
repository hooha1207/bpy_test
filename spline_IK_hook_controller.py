#armature를 선택한 다음, 원하는 bone layer를 코드에 입력하고 해당 코드를 실행하면
#현재 레이어에 존재하는 모든 bone을 원하는 bone layer로 복사하는데,
#이때 복사된 bone을 움직이면, 원래 존재하던 bone도 움직인다
#local space로 설정한 이유는 spline ik의 경우 hook로 회전값을 부여할 수 없기 때문에 back bone이 필요해서다


import bpy


spline_bone_layer = 1

select_bone_layer = [  ] + [spline_bone_layer]

bone_size = 0.1

constraints_name = "spline_IK_hook_constraints"
add_bone_name = "spline_hook_control_bone"


rebatch = -(0.5-bone_size/2)

actob_n = bpy.context.object.name


Bbone_layer = []
for i in range(len(bpy.context.object.data.layers)):
    if i in select_bone_layer:
        Bbone_layer.append(True)
    else:
        Bbone_layer.append(False)



bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')

select_bone_name = [i.name for i in bpy.context.selected_pose_bones]

#bpy.ops.armature.select_all(action='DESELECT')



#for bone_n in select_bone_name:
#    bpy.ops.object.mode_set(mode='EDIT')
#    bpy.ops.armature.select_all(action='DESELECT')
#    actob.data.bones[bone_n].select_head
#    actob.data.bones[bone_n].select_tail
#    bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#    bpy.ops.object.mode_set(mode='POSE')
#    add_bone = bpy.context.selected_pose_bones[0]
#    add_bone_name = bone.name
#    
#    cstrt = add_bone.constraints.new("COPY_TRANSFORMS")
#    cstrt.name = constraints_name
#    cstrt.target = actob
#    cstrt.subtarget = actob.pose.bones[bone_n].name
#    cstrt.owner_space = 'LOCAL'
#    cstrt.target_space = 'LOCAL'



for bone in bpy.context.selected_pose_bones:
    
    bone_location = bone.head
    
    cstrt = bone.constraints.new("COPY_TRANSFORMS")
    cstrt.name = constraints_name
    cstrt.target = bpy.data.objects[actob_n]
    cstrt.owner_space = 'LOCAL'
    cstrt.target_space = 'LOCAL'
    

    
#    bpy.ops.object.mode_set(mode='EDIT')
#    bpy.ops.armature.select_all(action='DESELECT')
#    bpy.ops.object.mode_set(mode='OBJECT')
#    bpy.data.objects[actob_n].data.bones[bone.name].select=True
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.armature.bone_primitive_add(name=add_bone_name)
    bpy.ops.armature.select_linked()
    
    bpy.ops.transform.translate(value=bone_location) #world_space_coordinate
    bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
    bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
    
    bpy.ops.object.mode_set(mode='POSE')
    add_bone = bpy.context.selected_pose_bones[0]
    add_bone_name = add_bone.name
    
    
    
    cstrt.subtarget = bpy.data.objects[actob_n].data.bones[add_bone_name].name

    
    bpy.ops.pose.bone_layers(layers=Bbone_layer)




for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False





