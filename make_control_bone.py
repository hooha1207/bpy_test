#armature를 선택한 다음, 원하는 bone layer를 코드에 입력하고 해당 코드를 실행하면
#현재 레이어에 존재하는 모든 bone을 원하는 bone layer로 복사하는데,
#이때 복사된 bone을 움직이면, 원래 존재하던 bone도 움직인다
#local space로 설정한 이유는 spline ik의 경우 hook로 회전값을 부여할 수 없기 때문에 back bone이 필요해서다

#해당 스크립트는 back bone이 존재하고 controller bone이 필요할 때 사용할 수 있다

import bpy


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
