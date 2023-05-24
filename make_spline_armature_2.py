#curve_to_bone, make_spline_IK, make_front_bone, make_control_bone 스크립트를 전부 합쳤다
#그냥 armature를 active select로 설정하고, curve를 select로 설정한 뒤 실행하면 bone이 생성된다

#armature를 activate_select로 설정한다
#curve를 select로 설정한다
#이때 curve는 apply_all_transform을 해줘야 된다
#스크립트를 실행하면, control point는 parent, handle point는 child로 이루어진 bone이 activate_select 된 armatrue에 추가된다


import bpy


ob_armature = bpy.context.active_object
ob_select = [i for i in bpy.context.selected_objects if not i == ob_armature]


bone_size = 0.05
rebatch = -(0.5-bone_size/2)

parent_bone_size = 0.1
parent_rebatch = -(0.5-parent_bone_size/2)


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')


curve_bone_dic = {}

for ob in ob_select:
    curve_name = ob.name
    
    parent_bone_name_l = []
    
    for spline_i in range(len(ob.data.splines)):
        if ob.data.splines[spline_i].type == 'BEZIER':
            
            for bezier_point_i in range(len(ob.data.splines[spline_i].bezier_points)):
                bpy.ops.object.select_all(action='DESELECT')

                #control_point
                #[
                bpy.context.view_layer.objects.active = ob_armature
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')
                
                #add bone
                add_bone_name = "bezier_curve_to_bone_control"
                bpy.ops.armature.bone_primitive_add(name=add_bone_name)
                bpy.ops.armature.select_linked()
                
                #set bone active
                bpy.ops.object.mode_set(mode='POSE')
                select_bone_name = bpy.context.selected_pose_bones[0].name
                parent_bone_name = select_bone_name
                bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
                bpy.context.object.pose.bones[select_bone_name].bone.use_deform = False
                bpy.ops.object.mode_set(mode='OBJECT')
                
                bpy.ops.object.mode_set(mode='EDIT')
                
                #set place
                bpy.ops.transform.translate(value=ob.data.splines[spline_i].bezier_points[bezier_point_i].co) #world_space_coordinate
                
                #set bone size
                bpy.ops.transform.resize(value=(parent_bone_size, parent_bone_size, parent_bone_size))
                bpy.ops.transform.translate(value=(0.0,0.0,parent_rebatch))
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #set hook
                ob_armature.select_set(True)
                bpy.data.objects[curve_name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')
                ob.data.splines[spline_i].bezier_points[bezier_point_i].select_control_point = True
                bpy.ops.object.hook_add_selob(use_bone=True)
                bpy.ops.curve.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                #]
                #control_point
                
                parent_bone_name_l.append(parent_bone_name)
                
                
                #handle_left
                #[
                bpy.context.view_layer.objects.active = ob_armature
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')
                
                #add bone
                add_bone_name = "bezier_curve_to_bone_left"
                bpy.ops.armature.bone_primitive_add(name=add_bone_name)
                bpy.ops.armature.select_linked()
                
                #set bone active
                bpy.ops.object.mode_set(mode='POSE')
                select_bone_name = bpy.context.selected_pose_bones[0].name
                child_bone_name_L = select_bone_name
                bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
                bpy.context.object.pose.bones[select_bone_name].bone.use_deform = False
                bpy.ops.object.mode_set(mode='OBJECT')
                
                bpy.ops.object.mode_set(mode='EDIT')
                
                #set place
                bpy.ops.transform.translate(value=ob.data.splines[spline_i].bezier_points[bezier_point_i].handle_left) #world_space_coordinate
                
                #set bone size
                bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
                bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #set hook
                ob_armature.select_set(True)
                bpy.data.objects[curve_name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')
                ob.data.splines[spline_i].bezier_points[bezier_point_i].select_left_handle = True
                bpy.ops.object.hook_add_selob(use_bone=True)
                bpy.ops.curve.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                #]
                #handle_right
                
                
                
                #handle_right
                #[
                bpy.context.view_layer.objects.active = ob_armature
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')
                
                #add bone
                add_bone_name = "bezier_curve_to_bone_right"
                bpy.ops.armature.bone_primitive_add(name=add_bone_name)
                bpy.ops.armature.select_linked()
                
                #set bone active
                bpy.ops.object.mode_set(mode='POSE')
                select_bone_name = bpy.context.selected_pose_bones[0].name
                child_bone_name_R = select_bone_name
                bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
                bpy.context.object.pose.bones[select_bone_name].bone.use_deform = False
                bpy.ops.object.mode_set(mode='OBJECT')
                
                bpy.ops.object.mode_set(mode='EDIT')
                
                #set place
                bpy.ops.transform.translate(value=ob.data.splines[spline_i].bezier_points[bezier_point_i].handle_right) #world_space_coordinate
                
                #set bone size
                bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
                bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #set hook
                ob_armature.select_set(True)
                bpy.data.objects[curve_name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')
                ob.data.splines[spline_i].bezier_points[bezier_point_i].select_right_handle = True
                bpy.ops.object.hook_add_selob(use_bone=True)
                bpy.ops.curve.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                #]
                #handle_right
                
                
                bpy.context.view_layer.objects.active = ob_armature
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.data.objects[ob_armature.name].data.edit_bones[child_bone_name_R].parent = bpy.data.objects[ob_armature.name].data.edit_bones[parent_bone_name]
                bpy.data.objects[ob_armature.name].data.edit_bones[child_bone_name_L].parent = bpy.data.objects[ob_armature.name].data.edit_bones[parent_bone_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                    



        elif ob.data.splines[spline_i].type == 'NURBS':
            for nurbs_point_i in range(len(ob.data.splines[spline_i].points)):
                bpy.ops.object.select_all(action='DESELECT')

                #control_point
                #[
                bpy.context.view_layer.objects.active = ob_armature
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')
                
                #add bone
                add_bone_name = "nurbs_curve_to_bone_control"
                bpy.ops.armature.bone_primitive_add(name=add_bone_name)
                bpy.ops.armature.select_linked()
                
                #set bone active
                bpy.ops.object.mode_set(mode='POSE')
                select_bone_name = bpy.context.selected_pose_bones[0].name
                parent_bone_name = select_bone_name
                bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
                bpy.context.object.pose.bones[select_bone_name].bone.use_deform = False
                bpy.ops.object.mode_set(mode='OBJECT')
                
                bpy.ops.object.mode_set(mode='EDIT')
                
                #set place
                bpy.ops.transform.translate(value=ob.data.splines[spline_i].points[nurbs_point_i].co[:-1]) #world_space_coordinate
                
                #set bone size
                bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
                bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #set hook
                ob_armature.select_set(True)
                bpy.data.objects[curve_name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')
                ob.data.splines[spline_i].points[nurbs_point_i].select = True
                bpy.ops.object.hook_add_selob(use_bone=True)
                bpy.ops.curve.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                #]
                #control_point
                
                parent_bone_name_l.append(parent_bone_name)

                
    curve_bone_dic[ob.name] = parent_bone_name_l


bpy.context.view_layer.objects.active = ob_armature



#armature를 선택한 다음, 원하는 bone layer를 코드에 입력하고 해당 코드를 실행하면
#현재 레이어에 존재하는 모든 bone을 원하는 bone layer로 복사하는데,
#이때 복사된 bone을 움직이면, 원래 존재하던 bone도 움직인다
#local space로 설정한 이유는 spline ik의 경우 hook로 회전값을 부여할 수 없기 때문에 back bone이 필요해서다

#해당 스크립트는 back bone이 존재하고 controller bone이 필요할 때 사용할 수 있다


spline_bone_layer = 9

select_bone_layer = [  ] + [spline_bone_layer]

constraints_name = "spline_IK_hook_constraints"
add_bone_name = "spline_hook_local_bone"

bone_size = 0.05
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
#If you want only selected bones to be control bones,
#modified here

select_bone_name = [i.name for i in bpy.context.selected_pose_bones]


reparent_bone = []
reparent_bone_parent = []

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='POSE')

add_bone_tree = {}


for bone in select_bone_name:
    
    bone_location = bpy.data.objects[actob_n].pose.bones[bone].head

    cstrt = bpy.data.objects[actob_n].pose.bones[bone].constraints.new("COPY_TRANSFORMS")
    cstrt.name = constraints_name
    cstrt.target = bpy.data.objects[actob_n]
    cstrt.owner_space = 'LOCAL'
    cstrt.target_space = 'LOCAL'
    
    if type(bpy.data.objects[actob_n].pose.bones[bone].parent) == type(None):
        add_bone_parent_name = f'{add_bone_name}_{bone}'
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.bone_primitive_add(name=add_bone_parent_name)
        bpy.ops.armature.select_linked()
        
        bpy.ops.transform.translate(value=bone_location) #world_space_coordinate
        bpy.ops.transform.resize(value=(parent_bone_size, parent_bone_size, parent_bone_size))
        bpy.ops.transform.translate(value=(0.0,0.0,parent_rebatch))
        
        bpy.ops.object.mode_set(mode='POSE')
        check_add_bone_name = bpy.context.selected_pose_bones[0].name
        bpy.context.object.pose.bones[check_add_bone_name].bone.use_deform = False
        bpy.ops.object.mode_set(mode='EDIT')
        
        add_bone_tree[bone] = [check_add_bone_name, [i.name for i in bpy.data.objects[actob_n].pose.bones[bone].children]]
        

    elif type(bpy.data.objects[actob_n].pose.bones[bone].parent) != type(None):
        parent_bone_name = bpy.data.objects[actob_n].pose.bones[bone].parent.name
        bpy.ops.object.mode_set(mode='EDIT')

        
        bpy.ops.armature.bone_primitive_add(name=f'{add_bone_name}_{bone}')
        bpy.ops.armature.select_linked()
        
        bpy.ops.transform.translate(value=bone_location) #world_space_coordinate
        bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
        bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
        
        bpy.ops.object.mode_set(mode='POSE')
        check_add_bone_name = bpy.context.selected_pose_bones[0].name
        bpy.context.object.pose.bones[check_add_bone_name].bone.use_deform = False
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            add_parent_bone_name = add_bone_tree[parent_bone_name][0]
            bpy.data.objects[actob_n].data.edit_bones[check_add_bone_name].parent = bpy.data.objects[actob_n].data.edit_bones[add_parent_bone_name]
        except:
            reparent_bone.append(check_add_bone_name)
            reparent_bone_parent.append(parent_bone_name)
        


    bpy.ops.object.mode_set(mode='POSE')
    cstrt.subtarget = bpy.data.objects[actob_n].data.bones[check_add_bone_name].name


    bpy.ops.pose.bone_layers(layers=Bbone_layer)
    


bpy.ops.object.mode_set(mode='EDIT')

for i in range(len(reparent_bone)):
    bpy.data.objects[actob_n].data.edit_bones[reparent_bone[i]].parent = bpy.data.objects[actob_n].data.edit_bones[reparent_bone_parent[i]]

bpy.ops.object.mode_set(mode='POSE')



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False




# 원하는 filter word와 filter word로 선택된 bone을 옮길 bone layer를 입력해준다
# filtering 하고자 하는 bone이 있는 bone layer를 활성화하고 해당 스크립트를 실행한다
# 만약 선택된 bone만 filtering 하고자 한다면, 아래 select all 을 삭제하면 된다



filter_bone_layer = 10

filter_word_list = ['control']



select_bone_layer = [  ] + [filter_bone_layer]

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



bpy.ops.pose.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
for bone_n in select_bone_name:
    for filter_word in filter_word_list:
        if filter_word in bone_n:
            bpy.data.objects[actob_n].data.bones[bone_n].select = True


bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.bone_layers(layers=Bbone_layer)



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False




choose_layer_index = 16
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index == choose_layer_index:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False
#bone layer의 경우, 무조건 하나 이상 활성화되어야만 된다
#때문에 원하는 bone layer를 선택하려면, 전체를 활성화한 다음,
#원하는 bone layer 외에는 전부 비활성화하는 과정이 필요하다
#위 코드는 해당 과정을 수행한다

#armature는 active select, 커브는 select로 설정하고 
#spline IK bone이 만들어질 bone layer를 선택하고 해당 스크립트를 실행한다


import math


unit_size = 0.3

add_bone_name = 'spline_ik_connect_bone'




curve_length_calc_unit = 0.01

bpy.ops.object.mode_set(mode='OBJECT')

actob_n = bpy.context.object.name
#Armature
selob_n = [i.name for i in ob_select]
#curve

bpy.ops.object.select_all(action='DESELECT')

for selob in selob_n:
    if bpy.data.objects[selob].data.splines[0].type == "NURBS":
        curve_point_density = len(bpy.data.objects[selob].data.splines[0].points)
        unit_batch_loc = bpy.data.objects[selob].data.splines[0].points[0].co[:-1]
    elif bpy.data.objects[selob].data.splines[0].type == "BEZIER":
        curve_point_density = 3*len(bpy.data.objects[selob].data.splines[0].bezier_points)
        unit_batch_loc = bpy.data.objects[selob].data.splines[0].bezier_points[0].co
    elif bpy.data.objects[selob].data.splines[0].type == "POLY":
        curve_point_density = len(bpy.data.objects[selob].data.splines[0].points)
        unit_batch_loc = bpy.data.objects[selob].data.splines[0].points[0].co[:-1]

    bpy.ops.mesh.primitive_plane_add(size=curve_length_calc_unit, enter_editmode=False, align='WORLD', location=unit_batch_loc, scale=(1, 1, 1))
    check_add_unit_n = bpy.context.selected_objects[0].name
    
    add_unit_mesh_n = bpy.data.objects[check_add_unit_n].to_mesh().name
    bpy.data.objects[check_add_unit_n].modifiers.new('unit_array', 'ARRAY')
    bpy.data.objects[check_add_unit_n].modifiers['unit_array'].fit_type = 'FIT_CURVE'
    bpy.data.objects[check_add_unit_n].modifiers['unit_array'].curve = bpy.data.objects[selob]

    bpy.ops.object.modifier_apply(modifier="unit_array")
    bpy.ops.object.mode_set(mode='EDIT')
    curve_length = bpy.data.objects[check_add_unit_n].data.total_face_sel * curve_length_calc_unit
    bpy.ops.object.mode_set(mode='OBJECT')
    minimum_cbone_density = curve_length / curve_point_density
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[actob_n]
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.bone_primitive_add(name=add_bone_name)
    bpy.ops.armature.select_linked()
#    print(f'curve_length   {curve_length}')
#    print(f'curve_point_density   {curve_point_density}')
#    print(f'math.floor(minimum_cbone_density)   {math.floor(minimum_cbone_density)}')
#    print(f'minimum_cbone_density   {minimum_cbone_density}')
#    bpy.ops.armature.subdivide(number_cuts=math.floor(minimum_cbone_density)-1)
    bpy.ops.armature.subdivide(number_cuts=curve_point_density-1)
    bpy.ops.object.mode_set(mode='POSE')
    for pbone in bpy.context.selected_pose_bones:
        bpy.data.objects[actob_n].pose.bones[pbone.name].bone.use_deform = False
    spline_ik_cstrt = bpy.context.selected_pose_bones[-1].constraints.new("SPLINE_IK")
    spline_ik_cstrt.target = bpy.data.objects[selob]
#    spline_ik_cstrt.chain_count = math.floor(minimum_cbone_density)
    spline_ik_cstrt.chain_count = math.floor(curve_point_density)
    bpy.ops.pose.select_all(action='DESELECT')
    
    bpy.data.objects.remove(bpy.data.objects[check_add_unit_n])
    bpy.data.meshes.remove(bpy.data.meshes[add_unit_mesh_n])


    bpy.ops.object.mode_set(mode='OBJECT')
    



#bezier_point[0] == spline IK head
#bezier_point[-1] == spline IK tail


bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.visual_transform_apply()
bpy.ops.pose.armature_apply(selected=True)
bpy.ops.pose.select_all(action='DESELECT')





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


back2cont = {}

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
        
        bpy.ops.object.mode_set(mode='POSE')
        for endbone in bpy.context.selected_pose_bones:
            endbone.bone.use_deform = True
        
        child_count = 0
        
        bpy.ops.object.mode_set(mode='POSE')
        for sel_bone in bpy.context.selected_pose_bones:
            if type(sel_bone.parent) == type(None):
                sel_bone.name = f'{add_bone_name}_{bone}'
                check_sel_bone_name = sel_bone.name
                
                back2cont[bone] = check_sel_bone_name
                
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






import numpy as np


def find_top_parent(cbone):
    bchild = False
    return_value = None
    while not bchild:
        if type(cbone.parent) != type(None):
            cbone = cbone.parent
        elif type(cbone.parent) == type(None):
            return_value = cbone.name
            bchild = True
    return return_value

tmp_dic = {}
#curve : top_bone

spikcb_l = [i for i in bpy.data.objects[actob_n].pose.bones if 'spline_ik_connect_bone' in i.name]
spikcb_l = [i for i in spikcb_l if not 'transform' in i.name]
spikcb_l = [i for i in spikcb_l if len(i.children) == 0]


for i in spikcb_l:
    curve_n = bpy.data.objects[actob_n].pose.bones[i.name].constraints['Spline IK'].target.name
    top_pb = find_top_parent(bpy.data.objects[actob_n].data.bones[i.name])
    tmp_dic[curve_n] = top_pb



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False

all_control_p_n = 'all_control_p'


bpy.ops.object.mode_set(mode='EDIT')
for cn in curve_bone_dic:
    bone_l_x = [bpy.data.objects[actob_n].data.bones[bone_n].head_local.x for bone_n in curve_bone_dic[cn]]
    bone_l_y = [bpy.data.objects[actob_n].data.bones[bone_n].head_local.y for bone_n in curve_bone_dic[cn]]
    bone_l_z = [bpy.data.objects[actob_n].data.bones[bone_n].head_local.z for bone_n in curve_bone_dic[cn]]
    
    center_head = (np.sum(bone_l_x) / len(bone_l_x), np.sum(bone_l_y) / len(bone_l_x), np.sum(bone_l_z) / len(bone_l_x))
    bpy.ops.armature.select_all(action='DESELECT')
    
    bpy.ops.armature.bone_primitive_add(name=f'{all_control_p_n}_{cn}')
    bpy.ops.armature.select_linked()
    bpy.ops.object.mode_set(mode='POSE')
    check_all_control_p_n = bpy.context.selected_pose_bones[0].name
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.object.data.bones.active = bpy.context.object.data.bones[check_all_control_p_n]
    bpy.context.object.data.bones[check_all_control_p_n].use_deform = False
    bpy.ops.transform.translate(value=center_head) #world_space_coordinate
    
    for bone_n in curve_bone_dic[cn]:
        bpy.ops.object.mode_set(mode='POSE')
        control_bone_name = bpy.data.objects[actob_n].pose.bones[bone_n].constraints["spline_IK_hook_constraints"].subtarget
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.data.objects[actob_n].data.edit_bones[control_bone_name].parent = bpy.data.objects[actob_n].data.edit_bones[check_all_control_p_n]
    bpy.data.objects[actob_n].data.edit_bones[back2cont[tmp_dic[cn]]].parent = bpy.data.objects[actob_n].data.edit_bones[check_all_control_p_n]




bpy.ops.object.mode_set(mode='POSE')
