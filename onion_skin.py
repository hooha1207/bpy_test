import bpy


actsel_ani = False
if bpy.context.active_object.animation_data != None:
    actsel_ani = True

if actsel_ani:
    """
    이 코드는 active select object에 animation이 존재할 때 실행된다
    일반적으로 내가 statue를 만들 때 애니메이션이 존재하는 bone을 선택하기 때문에
    대게 이 코드가 동작할 거 같다
            
    또 onione statue로 만들고자 하는 객체가 armature가 아니더라도,
    해당 위치에 statue를 만들도록 제작함
    """

    kfs = {'FINISHED'}
    first_select = bpy.context.selected_objects
    first_active_select = bpy.context.active_object
    onion_statues = []
        
    duplicate_l = [i for i in bpy.context.selected_objects if not i == bpy.context.active_object]
    anim = bpy.context.active_object
            
    while kfs == {'FINISHED'}:
        kfs = bpy.ops.screen.keyframe_jump()
        
        bpy.ops.object.select_all(action='DESELECT')
        for duplicate in duplicate_l:
            duplicate.select_set(True)
        
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        for duplicate in duplicate_l:
            bpy.context.view_layer.objects.active = duplicate
            try:
                bpy.ops.object.modifier_apply(modifier="Armature")
                print('armature')
            except:
                print('no armature')
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        for i in bpy.context.selected_objects:
            onion_statues.append(i)
        
        anim.select_set(True)
        bpy.context.view_layer.objects.active = anim

    bpy.ops.object.select_all(action='DESELECT')
    for i in onion_statues:
        i.select_set(True)
    bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="onion")
    
    bpy.ops.object.select_all(action='DESELECT')
    for i in first_select:
        i.select_set(True)
    bpy.context.view_layer.objects.active = first_active_select
    bpy.context.scene.frame_set(1)
    
else:
    print('Please, active select an object with animation')
