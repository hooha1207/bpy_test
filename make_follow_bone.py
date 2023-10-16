import bpy
import bmesh
import mathutils



GeometryNodeTree_n = 'Transfer_position_use_index'
vgn_vid = 'vid'
follow_armature_n = 'follow_armature'
bone_length = 0.1


armtob = [i for i in bpy.context.selected_objects if i.type == "ARMATURE"][0]
meshob = [i for i in bpy.context.selected_objects if i.type == "MESH"][0]






### collection
collection = bpy.data.collections.new(f'{meshob.name}_FollowBone')
bpy.context.collection.children.link(collection)

# detect collection
loop = True
for coll in bpy.data.collections:
    for coll_ob in coll.objects:
        if coll_ob.name == meshob.name:
            current_collection_n = coll.name
            loop = False
            break
    if not loop:
        break




# duplicate mesh object
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = meshob
meshob.select_set(True)
bpy.ops.object.duplicate_move()
meshob_dup_n = bpy.context.active_object.name
meshob_dup = bpy.data.objects[meshob_dup_n]

bpy.data.collections[current_collection_n].objects.unlink(meshob_dup)
collection.objects.link(meshob_dup)


# clear vg
for vg in meshob_dup.vertex_groups:
    meshob_dup.vertex_groups.remove(vg)

# clear modifier
for mod in meshob_dup.modifiers:
    meshob_dup.modifiers.remove(mod)


### set geometry node
# add node
geon_mod = meshob_dup.modifiers.new(name=GeometryNodeTree_n, type='NODES')
geometry_ng = bpy.data.node_groups.new(name=GeometryNodeTree_n, type='GeometryNodeTree')
geometry_ng.use_fake_user = True
geon_mod.node_group = geometry_ng

n_input = geometry_ng.nodes.new(type="NodeGroupInput")
n_input.location = (0,0)
socket_in1 = geometry_ng.inputs.new('NodeSocketGeometry','Geometry')


n_obinfo = geometry_ng.nodes.new(type="GeometryNodeObjectInfo")
n_obinfo.location = (100,0)
geometry_ng.nodes["Object Info"].inputs[0].default_value = meshob

n_spid = geometry_ng.nodes.new(type="GeometryNodeSampleIndex")
n_spid.data_type = 'FLOAT_VECTOR'
n_spid.location = (200,0)

n_idx = geometry_ng.nodes.new(type="GeometryNodeInputIndex")
n_idx.location = (300,0)

n_post = geometry_ng.nodes.new(type="GeometryNodeInputPosition")
n_post.location = (400,0)

n_vectmath_scl = geometry_ng.nodes.new(type="ShaderNodeVectorMath")
n_vectmath_scl.operation = 'SCALE'
n_vectmath_scl.location = (500,0)

n_setpost = geometry_ng.nodes.new(type="GeometryNodeSetPosition")
n_setpost.location = (600,0)

n_output = geometry_ng.nodes.new(type="NodeGroupOutput")
socket_out1 = geometry_ng.outputs.new('NodeSocketGeometry','Geometry')
n_output.location = (700,0)



# geometry node connect
geometry_ng.links.new(n_input.outputs['Geometry'], n_setpost.inputs['Geometry'])

geometry_ng.links.new(n_obinfo.outputs['Geometry'], n_spid.inputs['Geometry'])

geometry_ng.links.new(n_post.outputs['Position'], [i for i in n_spid.inputs if i.type=='VECTOR'][0])
geometry_ng.links.new(n_idx.outputs['Index'], n_spid.inputs['Index'])

#geometry_ng.links.new(n_spid.outputs['Value'], [i for i in n_vectmath_scl.inputs if i.type =='VECTOR'][0])
#geometry_ng.links.new(n_spid.outputs['Value'], n_vectmath_scl.inputs[3])
#geometry_ng.links.new(n_spid.outputs['Value'], [i for i in n_vectmath_scl.inputs if i.type =='VALUE'][0])
#geometry_ng.links.new(n_spid.outputs[2], n_vectmath_scl.inputs[3])
geometry_ng.links.new([i for i in n_spid.outputs if i.type=='VECTOR'][0], [i for i in n_vectmath_scl.inputs if i.type =='VECTOR'][0])
geometry_ng.links.new([i for i in n_vectmath_scl.outputs if i.type =='VECTOR'][0], n_setpost.inputs['Position'])

geometry_ng.links.new(n_output.inputs['Geometry'], n_setpost.outputs['Geometry'])


# vertex index to vg
vid_norm = {}

for v in meshob_dup.data.vertices:
    vg = meshob_dup.vertex_groups.new(name=f'{vgn_vid}-{v.index}')
    vg.add([v.index], 1.0, 'REPLACE')
    vid_norm[v.index] = [v.normal, v.co]



# make damped track mesh
bpy.ops.object.duplicate_move()
meshob_duptrk_n = bpy.context.active_object.name
meshob_duptrk = bpy.data.objects[meshob_duptrk_n]
dismod = meshob_duptrk.modifiers.new('Displace','DISPLACE')




# set bone
fol_armt = bpy.data.armatures.new(follow_armature_n)
folarmt_ob = bpy.data.objects.new(name=follow_armature_n, object_data=fol_armt)
collection.objects.link(folarmt_ob)

bpy.context.view_layer.objects.active = folarmt_ob
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='EDIT')

for vid in vid_norm:
    eb = fol_armt.edit_bones.new(f'{vgn_vid}-{vid}')
    eb.head = vid_norm[vid][1]
    eb.tail = vid_norm[vid][1] + vid_norm[vid][0]
    eb.length = bone_length

bpy.ops.object.mode_set(mode='POSE')
for pb in folarmt_ob.pose.bones:
    cstrt = pb.constraints.new("COPY_LOCATION")
    cstrt.target = meshob_dup
    cstrt.subtarget = pb.name
    
    cstrt = pb.constraints.new("DAMPED_TRACK")
    cstrt.target = meshob_duptrk
    cstrt.subtarget = pb.name

bpy.ops.object.mode_set(mode='OBJECT')




