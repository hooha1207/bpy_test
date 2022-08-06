import bpy


bpy.ops.object.make_single_user(object=True, obdata=True, material=True, animation=False, obdata_animation=False)


select = bpy.context.selected_objects
select_n = []

for i in select:
    select_n.append(i.name)


for idx, i in enumerate(select_n):
    bpy.ops.object.select_all(action='DESELECT')
    
    if bpy.data.objects.get(i) == None:
        continue

    bpy.context.view_layer.objects.active = bpy.data.objects[i]
    bobj = bpy.data.objects[i]

    nselect = select_n[:idx] + select_n[idx+1:]



    for k in nselect:
        
        if bpy.data.objects.get(k) == None or bpy.data.objects.get(i) == None:
            continue
        
        bpy.context.view_layer.objects.active = bpy.data.objects[i]
        bobj = bpy.data.objects[i]
        bobj.select_set(True)
        
        
        bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')
        


        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.view_layer.objects.active.modifiers['Boolean'].object = bpy.data.objects[k]
        bpy.context.view_layer.objects.active.modifiers['Boolean'].operation = 'INTERSECT'

        bpy.ops.object.modifier_apply(modifier='Boolean')



        if bpy.context.view_layer.objects.active.dimensions.x > 0 or bpy.context.view_layer.objects.active.dimensions.y > 0 or bpy.context.view_layer.objects.active.dimensions.z > 0:
            bpy.ops.object.delete()
            bpy.context.view_layer.objects.active = bpy.data.objects[i]
            bpy.data.objects[i].select_set(True)
            bpy.ops.object.delete()
        else:
            bpy.ops.object.delete()
