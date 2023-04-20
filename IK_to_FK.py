import bpy


actob = bpy.context.object


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='POSE')


constraints_name = "IK_to_FK_COPY_TRANSFORMS"

for bone in bpy.context.selected_pose_bones:
    if 'poletarget' in bone.name:
        continue
    elif bone.name[-2:] in [".L",".R"]:
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
    if 'poletarget' in bone.name:
        continue
#    bone.constraints[constraints_name].enabled = False
    bone.constraints.remove(bone.constraints.get(constraints_name))
    
bpy.ops.object.mode_set(mode='OBJECT')
