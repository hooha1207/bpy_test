#armature를 activate_select로 설정한다
#curve를 select로 설정한다
#이때 curve는 spline type이 nurbs 가 아니어야 되며, apply_all_transform을 해줘야 된다
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



def set_bone(curve_name):
    
    for spline_i in range(len(bpy.data.curves[f'{curve_name}'].splines)):
        for bezier_point_i in range(len(bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points)):
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
            select_bone_name = bpy.context.selected_pose_bones.__str__().split('[')[-1][1:-3]
            parent_bone_name = select_bone_name
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
            bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            #set place
            bpy.ops.transform.translate(value=bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].co) #world_space_coordinate
            
            #set bone size
            bpy.ops.transform.resize(value=(parent_bone_size, parent_bone_size, parent_bone_size))
            bpy.ops.transform.translate(value=(0.0,0.0,parent_rebatch))
            bpy.ops.object.mode_set(mode='OBJECT')
            
            #set hook
            ob_armature.select_set(True)
            bpy.data.objects[curve_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].select_control_point = True
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
            select_bone_name = bpy.context.selected_pose_bones.__str__().split('[')[-1][1:-3]
            child_bone_name_L = select_bone_name
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
            bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            #set place
            bpy.ops.transform.translate(value=bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].handle_left) #world_space_coordinate
            
            #set bone size
            bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
            bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
            bpy.ops.object.mode_set(mode='OBJECT')
            
            #set hook
            ob_armature.select_set(True)
            bpy.data.objects[curve_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].select_left_handle = True
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
            select_bone_name = bpy.context.selected_pose_bones.__str__().split('[')[-1][1:-3]
            child_bone_name_R = select_bone_name
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[select_bone_name]
            bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            #set place
            bpy.ops.transform.translate(value=bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].handle_right) #world_space_coordinate
            
            #set bone size
            bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
            bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
            bpy.ops.object.mode_set(mode='OBJECT')
            
            #set hook
            ob_armature.select_set(True)
            bpy.data.objects[curve_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[curve_name]
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.data.curves[f'{curve_name}'].splines[spline_i].bezier_points[bezier_point_i].select_right_handle = True
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
            
            

for i in ob_select:
    set_bone(i.name)
    


bpy.context.view_layer.objects.active = ob_armature
