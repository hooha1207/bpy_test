# 해당 스크립트는 face가 vertex 4개로 이루어져있다는 가정 하에 작성되었다
# 선택한 edge의 link_faces를 bmesh를 사용하지 않고 구한다

import bpy
import bmesh

import numpy as np



actob = bpy.context.active_object
faces_arr = np.zeros(len(actob.data.polygons)*4, dtype=np.int32)
actob.data.polygons.foreach_get('vertices', faces_arr)
faces_arr = (np.array(faces_arr)).reshape(-1,4)
print(faces_arr)

edge = [[i.vertices[0], i.vertices[1]] for i in actob.data.edges if i.select][0]
print(edge)


mask1 = np.any(np.isin(faces_arr, edge[0]), axis=1)
mask2 = np.any(np.isin(faces_arr, edge[1]), axis=1)


mask = mask1*mask2
result = np.where(mask)
print(result)
print(faces_arr[result])



edge_idx = [i.index for i in actob.data.edges if i.select][0]
obm = bmesh.new()
obm.from_mesh(actob.data)
obm.verts.ensure_lookup_table()
obm.edges.ensure_lookup_table()
obm.faces.ensure_lookup_table()

print([i.index for i in obm.edges[edge_idx].link_faces])
