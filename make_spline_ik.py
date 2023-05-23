#armature는 active select, 커브는 select로 설정하고 
#spline IK bone이 만들어질 bone layer를 선택하고 해당 스크립트를 실행한다


import bpy
import math


unit_size = 0.3

add_bone_name = 'spline_ik_connect_bone'




curve_length_calc_unit = 0.01

bpy.ops.object.mode_set(mode='OBJECT')

actob_n = bpy.context.object.name
#Armature
selob_n = [i.name for i in bpy.context.selected_objects if not i.name == actob_n]
#curve

bpy.ops.object.select_all(action='DESELECT')

for selob in selob_n:
    if bpy.data.objects[selob].data.splines[0].type == "NURBS":
        curve_point_density = len(bpy.data.objects[selob].data.splines[0].points)
        unit_batch_loc = bpy.data.objects[selob].data.splines[0].points[0].co[-1]
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
    print(f'curve_length   {curve_length}')
    print(f'curve_point_density   {curve_point_density}')
    print(f'math.floor(minimum_cbone_density)   {math.floor(minimum_cbone_density)}')
    print(f'minimum_cbone_density   {minimum_cbone_density}')
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
