#armature를 선택한 다음, 원하는 bone layer를 코드에 입력하고
# cloth curve가 존재하는 collection 을 코드에 입력하고 실행하면
#현재 레이어에 존재하는 모든 bone을 원하는 bone layer로 복사하는데,
#이때 복사된 bone을 움직이면, 원래 존재하던 bone도 움직인다
#local space로 설정한 이유는 spline ik의 경우 hook로 회전값을 부여할 수 없기 때문에 back bone이 필요해서다

#해당 스크립트는 back bone이 존재하고 controller bone이 필요할 때 사용할 수 있다

import bpy
import numpy as np



spline_stretch_bone_layer = 27

select_bone_layer = [  ] + [spline_stretch_bone_layer]

constraints_name = "hook_stretch"
add_bone_name = "hook_stretch"

curve_collections_name = 'cloth_curve_1'


bone_size = 0.01
parent_bone_size = 0.1


rebatch = -(0.5-bone_size/2)
parent_rebatch = -(0.5-parent_bone_size/2)

actob_n = bpy.context.object.name


Bbone_layer = []
for i in range(len(bpy.context.object.data.layers)):
    if i in select_bone_layer:
        Bbone_layer.append(True)
    else:
        Bbone_layer.append(False)



bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')


curve_name_list = [i.name for i in bpy.data.collections[curve_collections_name].all_objects]
select_bone_name = [i.name for i in bpy.context.selected_pose_bones]


#hook_bone_dic = {}
#for curve_n in curve_name_list:
#    hook_bone_name = []
#    for modifier in bpy.data.objects[curve_n].modifiers:
#        hook_bone_name.append(modifier.subtarget)
#    hook_bone_dic[curve_n] = hook_bone_name


spline_hook_local = 'spline_hook_local_bone'

control_hook_bone_dic = {}
for curve_n in curve_name_list:
    hook_bone_name = []
    for modifier in bpy.data.objects[curve_n].modifiers:
        for pbone in bpy.data.objects[actob_n].pose.bones:
            if len(pbone.constraints) != 0:
                if pbone.constraints[0].name == 'spline_IK_hook_constraints':
#                    print('spline_IK_hook_constraints == check')
                    if type(pbone.parent) == type(None):
#                        print('parent == check')
#                        print(f'modifier.subtarget  {modifier.subtarget}')
#                        print(f'pbone.constraints[0].subtarget  {pbone.constraints[0].subtarget}')
#                        if pbone.constraints[0].subtarget.split('.')[-1] == modifier.subtarget.split('.')[-1]:
#                        print(pbone.constraints[0].subtarget)
#                        print(f'{spline_hook_local}_{modifier.subtarget}')
                        if pbone.constraints[0].subtarget == f'{spline_hook_local}_{modifier.subtarget}':
#                            print('subtarget == check')
                            hook_bone_name.append(pbone.constraints[0].subtarget)
    control_hook_bone_dic[curve_n] = hook_bone_name

hook_bone_dic = control_hook_bone_dic

del curve_n

del modifier




top_parent = []

def find_top_parent(bone):
    if type(bpy.data.objects[actob_n].pose.bones[bone].parent) == type(None):
        top_parent.append(bone)
    else:
        find_top_parent(bpy.data.objects[actob_n].pose.bones[bone].parent.name)


spline_ik_bone = []

spline_ik_bone_dic = {}
# curve_name : [spline_IK, spline_top_parent, [bone hooked to the curve]]
for i in bpy.data.objects[actob_n].pose.bones:
    if len(i.constraints) != 0:
        if i.constraints[0].type == 'SPLINE_IK':
            find_top_parent(i.name)
            spline_ik_bone_dic[i.constraints[0].target.name] = [i.name, top_parent[0], hook_bone_dic[i.constraints[0].target.name]]

    top_parent = []

bpy.ops.pose.select_all(action='DESELECT')


bpy.ops.object.mode_set(mode='EDIT')
for curve_n in spline_ik_bone_dic:
    spline_ik_bone, spline_top_parent_bone, hook_bone_list = spline_ik_bone_dic[curve_n]
    
    
    bpy.ops.armature.bone_primitive_add(name=f'{add_bone_name}_target')
    bpy.ops.armature.select_linked()

    bpy.ops.transform.translate(value=bpy.data.objects[actob_n].pose.bones[spline_ik_bone].tail) #world_space_coordinate
    bpy.ops.transform.resize(value=(parent_bone_size, parent_bone_size, parent_bone_size))
    bpy.ops.transform.translate(value=(0.0,0.0,parent_rebatch))
    
    bpy.ops.object.mode_set(mode='POSE')
    check_target_bone_n = bpy.context.selected_pose_bones[0].name
    bpy.data.objects[actob_n].pose.bones[check_target_bone_n].bone.use_deform = False
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT')
    
    spline_ik_loc = bpy.data.objects[actob_n].pose.bones[spline_ik_bone].tail
    spline_top_parent_loc = bpy.data.objects[actob_n].pose.bones[spline_top_parent_bone].head

    min_spline_ik_hook = np.abs(np.array(spline_ik_loc))*10
    min_spline_ik_hook_bone_name = ''
    # Vector((0.0, 0.0, 0.0))
    for hook_bn in hook_bone_list:
#        print(f'np.sum(np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_ik_hook))   {np.sum(np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_ik_hook))}')
#        print(f'np.sum(np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < min_spline_ik_hook)   {np.sum(np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < min_spline_ik_hook)}')
#        print(f'np.sum(np.abs(spline_ik_loc - np.array(bpy.data.objects[actob_n].pose.bones[hook_bn].head)) < np.abs(min_spline_ik_hook))   {np.sum(np.abs(spline_ik_loc - np.array(bpy.data.objects[actob_n].pose.bones[hook_bn].head)) < np.abs(min_spline_ik_hook))}')
#        print(f'spline_ik_loc   {spline_ik_loc}')
#        print(f'bpy.data.objects[actob_n].pose.bones[hook_bn].head   {bpy.data.objects[actob_n].pose.bones[hook_bn].head}')
        if np.sum(np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_ik_hook)) >= 2:
            min_spline_ik_hook = np.abs(spline_ik_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head)
            min_spline_ik_hook_bone_name = hook_bn

    min_spline_top_parent_hook = np.abs(np.array(spline_top_parent_loc))*10
    min_spline_top_parent_hook_bone_name = ''
    # Vector((0.0, 0.0, 0.0))
    for hook_bn in hook_bone_list:
#        print(f'np.sum(np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_top_parent_hook))   {np.sum(np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_top_parent_hook))}')
#        print(f'np.sum(np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_top_parent_hook))   {np.sum(np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < min_spline_top_parent_hook)}')
#        print(f'np.sum(np.abs(spline_top_parent_loc - np.array(bpy.data.objects[actob_n].pose.bones[hook_bn].head)) < np.abs(min_spline_top_parent_hook))   {p.sum(np.abs(spline_top_parent_loc - np.array(bpy.data.objects[actob_n].pose.bones[hook_bn].head)) < np.abs(min_spline_top_parent_hook))}')
#        print(f'spline_top_parent_loc   {spline_top_parent_loc}')
#        print(f'bpy.data.objects[actob_n].pose.bones[hook_bn].head   {bpy.data.objects[actob_n].pose.bones[hook_bn].head}')
        if np.sum(np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head) < np.abs(min_spline_top_parent_hook)) >= 2:
            min_spline_top_parent_hook = np.abs(spline_top_parent_loc - bpy.data.objects[actob_n].pose.bones[hook_bn].head)
            min_spline_top_parent_hook_bone_name = hook_bn

#    bpy.data.objects[actob_n].pose.bones[min_spline_ik_hook_bone_name].head
#    bpy.data.objects[actob_n].pose.bones[min_spline_top_parent_hook_bone_name].head

    bpy.ops.armature.bone_primitive_add(name=f'{add_bone_name}')
    bpy.ops.armature.select_linked()

    bpy.ops.object.mode_set(mode='POSE')
    check_add_bone = bpy.context.selected_pose_bones[0].name
    bpy.data.objects[actob_n].pose.bones[check_add_bone].bone.use_deform = False
#    print(f'min_spline_top_parent_hook_bone_name = {min_spline_top_parent_hook_bone_name}')
#    print(f'min_spline_ik_hook_bone_name = {min_spline_ik_hook_bone_name}')
#    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.data.objects[actob_n].data.edit_bones[check_add_bone].head = np.array(bpy.data.objects[actob_n].pose.bones[min_spline_top_parent_hook_bone_name].head)
    bpy.data.objects[actob_n].data.edit_bones[check_add_bone].tail = np.array(bpy.data.objects[actob_n].pose.bones[min_spline_ik_hook_bone_name].head)
    
    bpy.ops.object.mode_set(mode='POSE')
    
    
#    해당 부분은 어째서인지 에러가 발생해서 try문으로 error가 발생하면 constraints를 추가하지 않도록 했는데,
#    이상하게 스크립트를 실행하면 정상적으로 bone이 생성되고 constraints도 추가된다
#    이는 추후 확인할 필요가 있어보임
#    원인은 알 수 없으나 constraints를 추가하는 코드를 없애면 에러가 발생하지 않는다
    
    for hbone_child in hook_bone_list:
        c_cstrt = bpy.data.objects[actob_n].pose.bones[hbone_child].constraints.new("CHILD_OF")
        c_cstrt.name = constraints_name
        c_cstrt.target = bpy.data.objects[actob_n]
        c_cstrt.subtarget = check_add_bone


    try:
        cstrt = bpy.data.objects[actob_n].pose.bones[check_add_bone].constraints.new("STRETCH_TO")
        cstrt.name = constraints_name
        cstrt.target = bpy.data.objects[actob_n]
        cstrt.subtarget = check_target_bone_n
        cstrt.volume = 'NO_VOLUME'
    except:
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')
        continue
    
    bpy.ops.pose.select_all(action='DESELECT')
    
    bpy.ops.object.mode_set(mode='EDIT')


bpy.ops.object.mode_set(mode='OBJECT')
