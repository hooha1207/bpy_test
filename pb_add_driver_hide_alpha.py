import bpy


actob = bpy.context.active_object
pbnl = [i.name for i in bpy.context.selected_pose_bones]


for bn in pbnl:
    fcurve = actob.pose.bones[bn].bone.driver_add('hide')
    driver = fcurve.driver
    driver.type = "SCRIPTED"
    var_1 = driver.variables.new()
    var_1.name = 'var_1'
    var_1.type = "SINGLE_PROP"
    var_1.targets[0].id = actob
    var_1.targets[0].data_path = 'pose.bones["root"]["FK_Mode_muffler"]'

    var_2 = driver.variables.new()
    var_2.name = 'var_2'
    var_2.type = "SINGLE_PROP"
    var_2.targets[0].id = actob
    var_2.targets[0].data_path = 'pose.bones["root"]["IK_Mode_muffler"]'
    
    driver.expression = '(0<((var_1==1) + (var_2==1)))'
#    driver.expression = '1-(var_1==0)'

for bn in pbnl:
    fcurves = actob.pose.bones[f'LSTts_upper_fore.{lr}'].driver_add('scale')
    driver = fcurves[0].driver
    driver.type = 'SCRIPTED'
    var = driver.variables.new()
    var.type = 'TRANSFORMS'
    var.name = 'var'
    var.targets[0].id = actob
    var.targets[0].bone_target = f'LST_upper_fore.{lr}'
    var.targets[0].transform_space = 'LOCAL_SPACE'
    var.targets[0].transform_type = 'SCALE_Y'
    driver.expression = 'var'
    driver = fcurves[1].driver
    driver.type = 'SCRIPTED'
    var = driver.variables.new()
    var.type = 'TRANSFORMS'
    var.name = 'var'
    var.targets[0].id = actob
    var.targets[0].bone_target = f'LST_upper_fore.{lr}'
    var.targets[0].transform_space = 'LOCAL_SPACE'
    var.targets[0].transform_type = 'SCALE_Y'
    driver.expression = 'var'
    driver = fcurves[2].driver
    driver.type = 'SCRIPTED'
    var = driver.variables.new()
    var.type = 'TRANSFORMS'
    var.name = 'var'
    var.targets[0].id = actob
    var.targets[0].bone_target = f'LST_upper_fore.{lr}'
    var.targets[0].transform_space = 'LOCAL_SPACE'
    var.targets[0].transform_type = 'SCALE_Y'
    driver.expression = 'var'
