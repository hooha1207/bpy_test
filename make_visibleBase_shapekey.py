import bpy
from mathutils import Vector, Matrix, Euler, Quaternion



shapeKey_n = 'sign_shapekey'
from_mix = False


learning_rate = 1e-1

threshold = 0.01




base_ob = bpy.context.active_object
target_ob = [i for i in bpy.context.selected_objects if i!=base_ob][0]

if base_ob.data.shape_keys == None:
    base_ob.shape_key_add(name='Basis', from_mix=True)
    

depsgraph = bpy.context.evaluated_depsgraph_get()
vis_ob = depsgraph.objects[base_ob.name]


sk = base_ob.shape_key_add(name=shapeKey_n, from_mix=from_mix)
skn = sk.name
base_ob.data.shape_keys.key_blocks[skn].value = 1.0



for vid in range(len(vis_ob.data.vertices)):
    print('vid  :  ', vid)
    
    incorrect = True
    direct = (target_ob.data.vertices[vid].co - vis_ob.data.vertices[vid].co)*learning_rate
    print(direct)
    while incorrect:
        
        before_v = target_ob.data.vertices[vid].co - depsgraph.objects[base_ob.name].data.vertices[vid].co
        
        sk.data[vid].co += direct
        depsgraph.update()
        
        after_v = target_ob.data.vertices[vid].co - depsgraph.objects[base_ob.name].data.vertices[vid].co
        
        diff_loss = after_v - before_v
#        print(diff_loss)
#        print(direct)
        if diff_loss.length < threshold:
            incorrect = False
        
        if abs(diff_loss.x)>abs(before_v.x):
            direct.x = direct.x + (diff_loss.x * -1)
        if abs(diff_loss.y)>abs(before_v.y):
            direct.y = direct.y + (diff_loss.y * -1)
        if abs(diff_loss.z)>abs(before_v.z):
            direct.z = direct.z + (diff_loss.z * -1)
        
#        sk.data[vid].co
#        vis_ob.data.vertices[vid].co

print('\n')
