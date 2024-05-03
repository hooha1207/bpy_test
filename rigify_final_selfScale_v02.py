import bpy
from math import pi
from mathutils import Vector, Matrix, Quaternion, Euler
#from timeit import default_timer as timer




def preprocess_self_scale_ik(actob, bn_mch, bn_ikc, bn_ikp, bn_ikt, bn_mch2ikc, bn_bbstr, bn_bbstrt, bn_bbtrf, side):
    
    actob.data.layers[-2] = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    
    current_bl_mch = []
    for idx, b in enumerate(actob.data.edit_bones[f'{bn_mch}.{side}'].layers):
        if b:
            current_bl_mch.append(idx)
    
    current_bl_ikc = []
    for idx, b in enumerate(actob.data.edit_bones[f'{bn_ikc}.{side}'].layers):
        if b:
            current_bl_ikc.append(idx)
    
    
    bpy.ops.armature.select_all(action='DESELECT')
    actob.data.edit_bones.active = actob.data.edit_bones[f'{bn_mch}.{side}']
    actob.data.edit_bones[f'{bn_mch}.{side}'].select_head = True
    actob.data.edit_bones[f'{bn_mch}.{side}'].select_tail = True
    bpy.ops.armature.duplicate_move()
    dup_mch_n = actob.data.edit_bones.active.name
    dup_mch_ed = actob.data.edit_bones[dup_mch_n]
    
    bpy.ops.armature.select_all(action='DESELECT')
    actob.data.edit_bones.active = actob.data.edit_bones[f'{bn_ikc}.{side}']
    actob.data.edit_bones[f'{bn_ikc}.{side}'].select_head = True
    actob.data.edit_bones[f'{bn_ikc}.{side}'].select_tail = True
    bpy.ops.armature.duplicate_move()
    dup_ikc_n = actob.data.edit_bones.active.name
    dup_ikc_ed = actob.data.edit_bones[dup_ikc_n]
    
    bpy.ops.armature.select_all(action='DESELECT')
    
    stretch_locTarget_bn = actob.data.edit_bones[f'{bn_ikc}.{side}'].parent.name
    
    
    
    actob.data.edit_bones[f'{bn_ikc}.{side}'].layers[-2]=True
    
    for bl_ikc in current_bl_ikc:
        dup_mch_ed.layers[bl_ikc]=True
        dup_ikc_ed.layers[bl_ikc]=True
        actob.data.edit_bones[f'{bn_ikc}.{side}'].layers[bl_ikc]=False
        print(bl_ikc)
    
    
    
    stretch_eb = actob.data.edit_bones.new(f'{bn_bbstr}.{side}')
    stretch_eb.head = actob.data.edit_bones[f'{bn_ikc}.{side}'].head
    stretch_eb.tail = actob.data.edit_bones[f'{bn_mch}.{side}'].tail
    stretch_eb.roll = actob.data.edit_bones[f'{bn_ikc}.{side}'].roll
    stretch_n = stretch_eb.name
    
    distance_v = stretch_eb.tail - stretch_eb.head
    distance = distance_v.length
    
    stretch_target_eb = actob.data.edit_bones.new(f'{bn_bbstrt}.{side}')
    stretch_target_eb.head = actob.data.edit_bones[f'{bn_mch}.{side}'].tail
    stretch_target_eb.tail = stretch_target_eb.head + Vector((0,0,0.5))
    stretch_target_eb.parent = actob.data.edit_bones[f'{bn_ikt}.{side}']
    stretch_target_n = stretch_target_eb.name
    
    stretch_sc_transfer_eb = actob.data.edit_bones.new(f'{bn_bbtrf}.{side}')
    stretch_sc_transfer_eb.head = actob.data.edit_bones[f'{bn_ikc}.{side}'].head
    stretch_sc_transfer_eb.tail = actob.data.edit_bones[f'{bn_mch}.{side}'].tail
    stretch_sc_transfer_eb.roll = actob.data.edit_bones[f'{bn_ikc}.{side}'].roll
    stretch_sc_transfer_eb.length = stretch_sc_transfer_eb.length / 2
    stretch_sc_transfer_n = stretch_sc_transfer_eb.name

    dup_ikc_ed.parent = stretch_sc_transfer_eb
    dup_mch_ed.parent = dup_ikc_ed
    
    
    
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
    
    

    actob.pose.bones[dup_mch_n].custom_shape = actob.pose.bones[f'{bn_ikc}.{side}'].custom_shape
    actob.pose.bones[f'{bn_ikc}.{side}'].custom_shape = None
    actob.pose.bones[f'{bn_mch}.{side}'].bone_group = actob.pose.bone_groups[1]
    actob.pose.bones[dup_mch_n].bone_group = actob.pose.bone_groups[1]

    for cstrt in actob.pose.bones[f'{bn_mch}.{side}'].constraints:
        actob.pose.bones[f'{bn_mch}.{side}'].constraints.remove(cstrt)
    
    cstrt = actob.pose.bones[f'{bn_mch}.{side}'].constraints.new('COPY_TRANSFORMS')
    cstrt.target = actob
    cstrt.subtarget = dup_mch_n
    
    cstrt = actob.pose.bones[f'{bn_ikc}.{side}'].constraints.new('COPY_TRANSFORMS')
    cstrt.target = actob
    cstrt.subtarget = dup_ikc_n
    
    cstrt = actob.pose.bones[dup_mch_n].constraints.new('COPY_SCALE')
    cstrt.target = actob
    cstrt.subtarget = dup_ikc_n
    cstrt.use_offset = True
    cstrt.power = -1
    cstrt.target_space = 'LOCAL'
    cstrt.owner_space = 'LOCAL'
    
    actob.pose.bones[dup_mch_n].constraints.move(2,0)
    
    
    for cstrt in actob.pose.bones[dup_mch_n].constraints:
        if cstrt.name == 'IK':
            cstrt.use_stretch = False
            fcurve = cstrt.driver_add('enabled')
            driver = fcurve.driver
            driver.type = 'SCRIPTED'
            var_1 = driver.variables.new()
            var_1.name = 'var_1'
            var_1.type = 'SINGLE_PROP'
            var_1.targets[0].id = bpy.context.active_object
            var_1.targets[0].data_path = f'pose.bones["{bn_ikp}.{side}"]["pole_vector"]'
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
            var_1.targets[0].data_path = f'pose.bones["{bn_ikp}.{side}"]["pole_vector"]'
            driver.expression = 'var_1'
    
    
    actob.pose.bones[dup_mch_n].lock_scale[0],\
    actob.pose.bones[dup_mch_n].lock_scale[1],\
    actob.pose.bones[dup_mch_n].lock_scale[2] = [False,False,False]
    
    
    
    actob.data.bones[f'{bn_ikc}.{side}'].name = 'tmp'
    actob.data.bones[dup_ikc_n].name = f'{bn_ikc}.{side}'
    actob.data.bones['tmp'].name = f'{bn_ikc}.001.{side}'
    
    actob.data.bones[dup_mch_n].name = f'{bn_mch2ikc}.{side}'
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    actob.data.edit_bones[stretch_sc_transfer_n].parent = actob.data.edit_bones[stretch_locTarget_bn]
    
    actob.data.layers[-2] = False
    bpy.ops.object.mode_set(mode='OBJECT')
    







rig_ob_n = bpy.context.active_object.name
actob = bpy.data.objects[rig_ob_n]



category_n = 'arm'

bn_mch = 'MCH-forearm_ik'
bn_ikc = 'upper_arm_ik'
bn_ikp = 'upper_arm_parent'
bn_ikt = 'MCH-upper_arm_ik_target'

bn_mch2ikc = 'forearm_ik'

bn_bbstr = f'sc_stretch_{category_n}'
bn_bbstrt = f'sc_stretch_target_{category_n}'
bn_bbtrf = f'sc_stretch_transfer_{category_n}'



dicts = []

info = {}

category_n = 'arm'

info['actob'] = actob

info['bn_mch'] = 'MCH-forearm_ik'
info['bn_ikc'] = 'upper_arm_ik'
info['bn_ikp'] = 'upper_arm_parent'
info['bn_ikt'] = 'MCH-upper_arm_ik_target'

info['bn_mch2ikc'] = 'forearm_ik'

info['bn_bbstr'] = f'sc_stretch_{category_n}'
info['bn_bbstrt'] = f'sc_stretch_target_{category_n}'
info['bn_bbtrf'] = f'sc_stretch_transfer_{category_n}'

dicts.append(info)



info = {}

category_n = 'leg'

info['actob'] = actob

info['bn_mch'] = 'MCH-shin_ik'
info['bn_ikc'] = 'thigh_ik'
info['bn_ikp'] = 'thigh_parent'
info['bn_ikt'] = 'MCH-thigh_ik_target'

info['bn_mch2ikc'] = 'shin_ik'

info['bn_bbstr'] = f'sc_stretch_{category_n}'
info['bn_bbstrt'] = f'sc_stretch_target_{category_n}'
info['bn_bbtrf'] = f'sc_stretch_transfer_{category_n}'

dicts.append(info)




for info in dicts:
    for side in ['L', 'R']:
        info['side'] = side
        preprocess_self_scale_ik(**info)
