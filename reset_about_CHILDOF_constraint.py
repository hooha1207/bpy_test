import bpy





for pb in bpy.context.selected_pose_bones:
    
    bpy.context.active_object.data.bones.active = bpy.context.active_object.data.bones[pb.name]
    cstrt_l = [i for i in pb.constraints if i.type == 'CHILD_OF']
    
    for cstrt in cstrt_l:

        context_py = bpy.context.copy()
        context_py['constraint'] = cstrt
        
        

        bpy.ops.constraint.childof_clear_inverse(context_py, constraint=cstrt.name, owner='BONE')
        bpy.ops.constraint.childof_set_inverse(context_py, constraint=cstrt.name, owner='BONE')
