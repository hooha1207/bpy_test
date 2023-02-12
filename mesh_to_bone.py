import bpy
import bmesh


index = 5 # here the index you want select please change 

obj = bpy.context.object
me = obj.data
bm = bmesh.from_edit_mesh(me)

vertices= [e for e in bm.verts]
oa = bpy.context.active_object

for vert in vertices:
    if vert.index == index:
        vert.select = True
    else:
        vert.select = False

bmesh.update_edit_mesh(me)
