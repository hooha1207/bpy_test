import bpy


filter_bone_layer = 17

constraints_name = 'FK_constraints'

constraints_type = 'COPY_TRANSFORMS'

clear = True




select_bone_layer = [  ] + [filter_bone_layer]
Bbone_layer = []
for i in range(len(bpy.context.object.data.layers)):
    if i in select_bone_layer:
        Bbone_layer.append(True)
    else:
        Bbone_layer.append(False)


actob_n = bpy.context.active_object.name

bpy.ops.object.mode_set(mode='POSE')
selb_n = [pb.name for pb in bpy.context.selected_pose_bones]


for bn in selb_n:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[actob_n].data.bones[bn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    if bpy.context.object.data.use_mirror_x:
        bpy.context.object.data.use_mirror_x = False
    bpy.ops.armature.duplicate_move()
    check_add_bone_n = bpy.context.selected_editable_bones[0].name
    bpy.ops.object.mode_set(mode='POSE')
    if clear:
        for rcs in bpy.data.objects[actob_n].pose.bones[check_add_bone_n].constraints.values():
            bpy.data.objects[actob_n].pose.bones[check_add_bone_n].constraints.remove(rcs)
    
    cstrt = bpy.data.objects[actob_n].pose.bones[bn].constraints.new(constraints_type)
    cstrt.target = bpy.data.objects[actob_n]
    cstrt.subtarget = check_add_bone_n
    cstrt.name = constraints_name
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.data.objects[actob_n].data.edit_bones[check_add_bone_n].parent = bpy.data.objects[actob_n].data.edit_bones[bn].parent
    bpy.ops.armature.bone_layers(layers=Bbone_layer)
    ob_ab_dic[bn] = check_add_bone_n

for ob in ob_ab_dic:
    ab = ob_ab_dic[ob]
    if type(bpy.data.objects[actob_n].data.edit_bones[ob].parent) != type(None):
        ob_parent = bpy.data.objects[actob_n].data.edit_bones[ob].parent.name
        bpy.data.objects[actob_n].data.edit_bones[ab].parent = bpy.data.objects[actob_n].data.edit_bones[ob_ab_dic[ob_parent]]



bpy.ops.object.mode_set(mode='POSE')
bpy.context.object.data.use_mirror_x = True



for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index in select_bone_layer:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False
