import bpy
from math import pi
from mathutils import Vector, Matrix, Quaternion, Euler


rig_ob_n = bpy.context.active_object.name
actob = bpy.data.objects[rig_ob_n]



actob.data.layers[-2] = True

for side in ['L', 'R']:
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.armature.select_all(action='DESELECT')
    actob.data.edit_bones.active = actob.data.edit_bones[f'MCH-forearm_ik.{side}']
    actob.data.edit_bones[f'MCH-forearm_ik.{side}'].select_head = True
    actob.data.edit_bones[f'MCH-forearm_ik.{side}'].select_tail = True
    bpy.ops.armature.duplicate_move()
    dup_forearm_n = actob.data.edit_bones.active.name
    dup_forearm_ed = actob.data.edit_bones[dup_forearm_n]
    
    bpy.ops.armature.select_all(action='DESELECT')
    actob.data.edit_bones.active = actob.data.edit_bones[f'upper_arm_ik.{side}']
    actob.data.edit_bones[f'upper_arm_ik.{side}'].select_head = True
    actob.data.edit_bones[f'upper_arm_ik.{side}'].select_tail = True
    bpy.ops.armature.duplicate_move()
    dup_upperarm_n = actob.data.edit_bones.active.name
    dup_upperarm_ed = actob.data.edit_bones[dup_upperarm_n]
    
    bpy.ops.armature.select_all(action='DESELECT')
    
    stretch_locTarget_bn = actob.data.edit_bones[f'upper_arm_ik.{side}'].parent.name
    
    if side =='L':
        dup_forearm_ed.layers[7]=True
        dup_upperarm_ed.layers[7]=True
    elif side =='R':
        dup_forearm_ed.layers[10]=True
        dup_upperarm_ed.layers[10]=True
    
    actob.data.edit_bones.active.layers[-2]=False
    
    actob.data.edit_bones[f'upper_arm_ik.{side}'].layers[-2]=True
    actob.data.edit_bones[f'upper_arm_ik.{side}'].layers[7]=False
    actob.data.edit_bones[f'upper_arm_ik.{side}'].layers[10]=False
    
    
    stretch_eb = actob.data.edit_bones.new(f'ik_armt_stretch.{side}')
    stretch_eb.head = actob.data.edit_bones[f'upper_arm_ik.{side}'].head
    stretch_eb.tail = actob.data.edit_bones[f'MCH-forearm_ik.{side}'].tail
    stretch_eb.roll = actob.data.edit_bones[f'upper_arm_ik.{side}'].roll
    stretch_n = stretch_eb.name
#    stretch_eb.parent = actob.data.edit_bones[f'upper_arm_ik.{side}'].parent
    
    distance_v = stretch_eb.tail - stretch_eb.head
    distance = distance_v.length
    
    stretch_target_eb = actob.data.edit_bones.new(f'ik_armt_stretch_target.{side}')
    stretch_target_eb.head = actob.data.edit_bones[f'MCH-forearm_ik.{side}'].tail
    stretch_target_eb.tail = stretch_target_eb.head + Vector((0,0,0.5))
    stretch_target_eb.parent = actob.data.edit_bones[f'MCH-upper_arm_ik_target.{side}']
    stretch_target_n = stretch_target_eb.name
    
    stretch_sc_transfer_eb = actob.data.edit_bones.new(f'stretch_sc_transfer.{side}')
    stretch_sc_transfer_eb.head = actob.data.edit_bones[f'upper_arm_ik.{side}'].head
    stretch_sc_transfer_eb.tail = actob.data.edit_bones[f'MCH-forearm_ik.{side}'].tail
    stretch_sc_transfer_eb.roll = actob.data.edit_bones[f'upper_arm_ik.{side}'].roll
    stretch_sc_transfer_eb.length = stretch_sc_transfer_eb.length / 2
    stretch_sc_transfer_n = stretch_sc_transfer_eb.name

    dup_upperarm_ed.parent = stretch_sc_transfer_eb
    dup_forearm_ed.parent = dup_upperarm_ed
    
    
    
    use_layers = [30]
    for eb in [stretch_eb, stretch_target_eb, stretch_sc_transfer_eb]:
        for uselayer in use_layers:
            eb.layers[uselayer] = True
        for i in range(len(eb.layers)):
            if not i in use_layers:
                eb.layers[i] = False
    
    
    
    bpy.ops.object.mode_set(mode='POSE')
    
    fcurve = actob.pose.bones[stretch_sc_transfer_n].driver_add('scale')
    for fc in fcurve:
        driver = fc.driver
        driver.type = 'SCRIPTED'
        var_1 = driver.variables.new()
        var_1.name = 'var_1'
        var_1.type = 'TRANSFORMS'
        var_1.targets[0].id = bpy.context.active_object
        var_1.targets[0].bone_target = stretch_n
        var_1.targets[0].transform_space = 'LOCAL_SPACE'
        var_1.targets[0].transform_type = 'SCALE_Y'
        driver.expression = 'var_1'
    
    cstrt = actob.pose.bones[stretch_n].constraints.new('ARMATURE')
    cstrt.targets.new()
    cstrt.targets[0].target = actob
    cstrt.targets[0].subtarget = stretch_locTarget_bn
    
    cstrt = actob.pose.bones[stretch_n].constraints.new('STRETCH_TO')
    cstrt.target = actob
    cstrt.subtarget = stretch_target_n
    cstrt.volume = 'NO_VOLUME'
    
    
    cstrt = actob.pose.bones[stretch_target_n].constraints.new('LIMIT_DISTANCE')
    cstrt.target = actob
    cstrt.subtarget = stretch_locTarget_bn
    cstrt.limit_mode = 'LIMITDIST_OUTSIDE'
    cstrt.target_space = 'CUSTOM'
    cstrt.owner_space = 'CUSTOM'
    cstrt.space_object = actob
    cstrt.space_subtarget = stretch_locTarget_bn
    
    
    cstrt = actob.pose.bones[stretch_sc_transfer_n].constraints.new('COPY_LOCATION')
    cstrt.target = actob
    cstrt.subtarget = stretch_locTarget_bn
    
    cstrt = actob.pose.bones[stretch_sc_transfer_n].constraints.new('DAMPED_TRACK')
    cstrt.target = actob
    cstrt.subtarget = stretch_target_n
    
    
    
    actob.pose.bones[f'upper_arm_ik.{side}'].custom_shape = None
    actob.pose.bones[f'MCH-forearm_ik.{side}'].bone_group = actob.pose.bone_groups[1]
    actob.pose.bones[dup_forearm_n].custom_shape = bpy.data.objects[f'WGT-rig_upper_arm_ik.{side}']
    actob.pose.bones[dup_forearm_n].bone_group = actob.pose.bone_groups[1]
    
    for cstrt in actob.pose.bones[f'MCH-forearm_ik.{side}'].constraints:
        actob.pose.bones[f'MCH-forearm_ik.{side}'].constraints.remove(cstrt)
    
    cstrt = actob.pose.bones[f'MCH-forearm_ik.{side}'].constraints.new('COPY_TRANSFORMS')
    cstrt.target = actob
    cstrt.subtarget = dup_forearm_n
#    cstrt.target_space = 'LOCAL'
#    cstrt.owner_space = 'LOCAL'
    
    cstrt = actob.pose.bones[f'upper_arm_ik.{side}'].constraints.new('COPY_TRANSFORMS')
    cstrt.target = actob
    cstrt.subtarget = dup_upperarm_n
#    cstrt.target_space = 'LOCAL'
#    cstrt.owner_space = 'LOCAL'
    
    cstrt = actob.pose.bones[dup_forearm_n].constraints.new('COPY_SCALE')
    cstrt.target = actob
    cstrt.subtarget = dup_upperarm_n
    cstrt.use_offset = True
    cstrt.power = -1
    cstrt.target_space = 'LOCAL'
    cstrt.owner_space = 'LOCAL'
    
    actob.pose.bones[dup_forearm_n].constraints.move(2,0)
    
    
    for cstrt in actob.pose.bones[dup_forearm_n].constraints:
        if cstrt.name == 'IK':
            cstrt.use_stretch = False
            fcurve = cstrt.driver_add('enabled')
            driver = fcurve.driver
            driver.type = 'SCRIPTED'
            var_1 = driver.variables.new()
            var_1.name = 'var_1'
            var_1.type = 'SINGLE_PROP'
            var_1.targets[0].id = bpy.context.active_object
            var_1.targets[0].data_path = f'pose.bones["upper_arm_parent.{side}"]["pole_vector"]'
            driver.expression = '1-var_1'
        elif cstrt.name == 'IK.001':
            cstrt.use_stretch = False
            fcurve = cstrt.driver_add('enabled')
            driver = fcurve.driver
            driver.type = 'SCRIPTED'
            var_1 = driver.variables.new()
            var_1.name = 'var_1'
            var_1.type = 'SINGLE_PROP'
            var_1.targets[0].id = bpy.context.active_object
            var_1.targets[0].data_path = f'pose.bones["upper_arm_parent.{side}"]["pole_vector"]'
            driver.expression = 'var_1'
    
    
    actob.pose.bones[dup_forearm_n].lock_scale[0],\
    actob.pose.bones[dup_forearm_n].lock_scale[1],\
    actob.pose.bones[dup_forearm_n].lock_scale[2] = [False,False,False]
    
    
    
    actob.data.bones[f'upper_arm_ik.{side}'].name = 'tmp'
    actob.data.bones[dup_upperarm_n].name = f'upper_arm_ik.{side}'
    actob.data.bones['tmp'].name = f'upper_arm_ik.001.{side}'
    
    actob.data.bones[dup_forearm_n].name = f'forearm_ik.{side}'

actob.data.layers[-2] = False
bpy.ops.object.mode_set(mode='OBJECT')
