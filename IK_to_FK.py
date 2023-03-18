import bpy

actob = bpy.context.object


constraints_name = "IK_to_FK_COPY_TRANSFORMS"

for bone in bpy.context.selected_pose_bones:
    if bone.name[-2:] in [".L",".R"]:
        cstrt = bone.constraints.new("COPY_TRANSFORMS")
        cstrt.name = constraints_name
        cstrt.target = actob
        cstrt.subtarget = actob.pose.bones[f"{bone.name[:-5]}.IK.{bone.name[-1:]}"].name
    else:
        cstrt = bone.constraints.new("COPY_TRANSFORMS")
        cstrt.name = constraints_name
        cstrt.target = actob
        cstrt.subtarget = actob.pose.bones[f"{bone.name[:-3]}.IK"].name
        
bpy.ops.pose.visual_transform_apply()

for bone in bpy.context.selected_pose_bones:
    bone.constraints[constraints_name].enabled = False
    

# 해당 코드는 2G anime anatomy 모델의 armature에 사용될 수 있는 코드다
# IK의 transforms을 FK bone에 visual_transform_apply를 하고 constraint를 enable한다
# 또 이 코드는 FK bone에 constraint를 추가하는 초기 세팅 코드이므로 세팅되어 있는 bone을 사용할 때는 아래 코드를 사용해야 된다



import bpy

actob = bpy.context.object


constraints_name = "IK_to_FK_COPY_TRANSFORMS"

for bone in bpy.context.selected_pose_bones:
    bone.constraints[constraints_name].enabled = True

bpy.ops.pose.visual_transform_apply()

for bone in bpy.context.selected_pose_bones:
    bone.constraints[constraints_name].enabled = False
