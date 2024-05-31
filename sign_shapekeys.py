import bpy



from_mix = False



actob_n = bpy.context.active_object.name
actob = bpy.data.objects[actob_n]
target_ob = [i for i in bpy.context.selected_objects if i!=actob]


if actob.data.shape_keys == None:
    actob.shape_key_add(name='Basis', from_mix=from_mix)




depsgraph = bpy.context.evaluated_depsgraph_get()

for ob in target_ob:

    sk = actob.shape_key_add(name=ob.name, from_mix=from_mix)
    skn = sk.name
    
    idx = 0
    for v in ob.data.vertices:
        sk.data[idx].co = v.co
        idx +=1
