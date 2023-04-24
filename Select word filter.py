# 원하는 filter word와 filter word로 선택된 bone을 옮길 bone layer를 입력해준다
# filtering 하고자 하는 bone이 있는 bone layer를 활성화하고 해당 스크립트를 실행한다
# 만약 선택된 bone만 filtering 하고자 한다면, 아래 select all 을 삭제하면 된다

import bpy


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
