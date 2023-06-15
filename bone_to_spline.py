import bpy
# import bmesh
# import mathutils
# import math
# import numpy as np



add_name = 'bone_to_curve'
bone_size = 0.05 # curve_to_bone size
choose_layer_index = 1 # curve_to_bone layer





print('\n')
actob = bpy.context.active_object # armature
actob_n = actob.name

current_bone_layer = []
for idx, _ in enumerate(bpy.context.object.data.layers):
    if _:
        current_bone_layer.append(idx)


fcbn = []
# child -> parent short
def find_childs(ppb):
    if type(ppb.child) != type(None):
        find_childs(ppb.child)
        fcbn.append(ppb.name)
    else:
        fcbn.append(ppb.name)
        return

find_childs(bpy.context.selected_pose_bones[0])
#fcbn.append(bpy.context.selected_pose_bones[0].name)
end_child_bn = fcbn[0]

bpy.ops.object.mode_set(mode='EDIT')


co_list = []
tmp_count = len(fcbn) -1
for i in fcbn:
    if tmp_count > 0:
        tmp_count -= 1
        co_list.append(actob.data.edit_bones[i].tail)
        print(actob.data.edit_bones[i].tail)
    else:
        co_list.append(actob.data.edit_bones[i].tail)
        co_list.append(actob.data.edit_bones[i].head)
        print(actob.data.edit_bones[i].tail)
        print(actob.data.edit_bones[i].head)

#print(co_list)

n_curve = bpy.data.curves.new(add_name,'CURVE')
n_curve.dimensions = '3D'
n_c_object = bpy.data.objects.new(add_name, n_curve)
check_add_ob_n = n_c_object.name
bpy.context.scene.collection.objects.link(n_c_object)


nurb = n_curve.splines.new('NURBS')
bpy.context.view_layer.objects.active = n_c_object
bpy.context.view_layer.objects.active = actob
nurb.points.add(len(fcbn))
nurb.use_endpoint_u = True
nurb.order_u = 3

# len(co_list) - idx로 작성한 이유는, spline_IK를 적용했을 때 bone이 뒤집히는 현상을 방지하기 위해서다
for idx, i in enumerate(nurb.points):
    i.co = (co_list[len(co_list)-idx-1][0], co_list[len(co_list)-idx-1][1], co_list[len(co_list)-idx-1][2], 1)


bpy.ops.object.mode_set(mode='POSE')
cstrt = actob.pose.bones[end_child_bn].constraints.new('SPLINE_IK')
cstrt.target = n_c_object
cstrt.chain_count = len(fcbn)


bpy.ops.object.mode_set(mode='OBJECT')
n_c_object.select_set(True)



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index == choose_layer_index:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False


#armature를 activate_select로 설정한다
#curve를 select로 설정한다
#이때 curve는 apply_all_transform을 해줘야 된다
#스크립트를 실행하면, control point는 parent, handle point는 child로 이루어진 bone이 activate_select 된 armatrue에 추가된다



ob_armature = bpy.context.active_object
ob_select = [i for i in bpy.context.selected_objects if not i == ob_armature]



rebatch = -(0.5-bone_size/2)

parent_bone_size = 0.1
parent_rebatch = -(0.5-parent_bone_size/2)


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')


for ob in ob_select:
    curve_name = ob.name
    
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
                

bpy.context.view_layer.objects.active = ob_armature
n_c_object.select_set(False)



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in current_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False


bpy.ops.object.mode_set(mode='POSE')