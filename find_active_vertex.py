# reference = https://blenderartists.org/t/i-want-to-get-active-vertex-in-blender-3d-python-api/597206

import bpy


bpy.ops.object.mode_set(mode='EDIT')
actob_n = bpy.context.active_object.name

# infut object_name == active_vertex_instance
def vertex_active(obn):
    bpy.data.objects[obn]
    bm = bmesh.from_edit_mesh(me)
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
            return elem
    else:
        return None
