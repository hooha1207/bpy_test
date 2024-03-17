import bpy
import bmesh



actob = bpy.context.active_object
obm = bmesh.from_edit_mesh(actob.data)

obm.verts.ensure_lookup_table()


obm.verts[0].index = 1
obm.verts[1].index = 1
obm.verts.sort()
bmesh.update_edit_mesh(actob.data)
