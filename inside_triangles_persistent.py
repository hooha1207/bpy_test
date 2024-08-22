import bpy
import numpy as np
from bpy.app.handlers import persistent

def inside_triangles(tris, points, margin=0.0):
    origins = tris[:, 0]
    cross_vecs = tris[:, 1:] - origins[:, None]
    v2 = points - origins

    v0 = cross_vecs[:, 0]
    v1 = cross_vecs[:, 1]

    d00_d11 = np.einsum('ijk,ijk->ij', cross_vecs, cross_vecs)
    d00 = d00_d11[:, 0]
    d11 = d00_d11[:, 1]
    d01 = np.einsum('ij,ij->i', v0, v1)
    d02 = np.einsum('ij,ij->i', v0, v2)
    d12 = np.einsum('ij,ij->i', v1, v2)

    denominator = d00 * d11 - d01 * d01
    if np.any(denominator == 0):
        raise ValueError("삼각형의 면적이 0입니다. 유효한 삼각형을 입력하세요.")
    div = 1 / denominator
    u = (d11 * d02 - d01 * d12) * div
    v = (d00 * d12 - d01 * d02) * div

    w = 1 - (u + v)
    weights = np.array([w, u, v]).T
    check = (u >= margin) & (v >= margin) & (w >= margin)
    return check, weights

@persistent
def load_handler(dummy=None):
    tris = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh = obj.data
            for poly in mesh.polygons:
                if len(poly.vertices) == 3:
                    tris.append([mesh.vertices[poly.vertices[0]].co,
                                 mesh.vertices[poly.vertices[1]].co,
                                 mesh.vertices[poly.vertices[2]].co])
    tris = np.array(tris)

    points = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'EMPTY':
            points.append(obj.location)
    points = np.array(points)

    if len(tris) == 0 or len(points) == 0:
        print("삼각형 데이터 또는 포인트 데이터가 없습니다.")
        return 0.0

    check, weights = inside_triangles(tris, points)
    print("Check:", check)
    print("Weights:", weights)
    
    return 0.0


bpy.app.timers.register(load_handler, persistent=True)
