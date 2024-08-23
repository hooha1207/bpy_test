import bpy
import bmesh

import numpy as np


# get vlf

actob = bpy.context.active_object
faces_arr = np.zeros(len(actob.data.edges)*2, dtype=np.int32)
actob.data.polygons.foreach_get('vertices', edges_arr)
edges_arr = (np.array(faces_arr)).reshape(-1,2)
print(edges_arr)

vert = [i.index for i in actob.data.vertices if i.select][0]
print(f'vert idx : {vert}')

mask = np.any(np.isin(edges_arr, vert), axis=1)

result = np.where(mask)
print(f'v result : {result}')
print(f'vle result : {faces_arr[result]}')
