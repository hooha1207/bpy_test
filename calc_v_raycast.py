import bpy
import numpy as np

# Active select 오브젝트 (a)
obj_a = bpy.context.view_layer.objects.active.evaluated_get(bpy.context.evaluated_depsgraph_get())

# Select 상태 오브젝트 (b)
obj_b = [obj.evaluated_get(bpy.context.evaluated_depsgraph_get()) for obj in bpy.context.selected_objects if obj != obj_a.original][0]

mesh_a = obj_a.data
mesh_b = obj_b.data

# a 오브젝트의 vertex 위치와 normal 가져오기
vertex_positions_a = np.array([obj_a.matrix_world @ v.co for v in mesh_a.vertices])
vertex_normals_a = np.array([obj_a.matrix_world.to_3x3() @ v.normal for v in mesh_a.vertices])

def intersect_ray_triangle(origin, direction, triangle):
    v0, v1, v2 = triangle
    edge1 = v1 - v0
    edge2 = v2 - v0
    h = np.cross(direction, edge2)
    a = np.dot(edge1, h)
    if -1e-8 < a < 1e-8:
        return False, None
    f = 1.0 / a
    s = origin - v0
    u = f * np.dot(s, h)
    if u < 0.0 or u > 1.0:
        return False, None
    q = np.cross(s, edge1)
    v = f * np.dot(direction, q)
    if v < 0.0 or u + v > 1.0:
        return False, None
    t = f * np.dot(edge2, q)
    if t > 1e-8:
        return True, t
    else:
        return False, None

def ray_cast(origin, direction, vertices, faces):
    for face in faces:
        v0, v1, v2, v3 = vertices[face]
        # 삼각형 두 개로 나누기
        triangles = [(v0, v1, v2), (v2, v3, v0)]
        for tri in triangles:
            hit, t = intersect_ray_triangle(origin, direction, tri)
            if hit:
                return True, t
    return False, None

faces_b = [np.array([j for j in i.vertices]) for i in obj_b.data.polygons]

hit_vertex_ids = []

for i, vertex in enumerate(vertex_positions_a):
    origin = vertex
    direction = vertex_normals_a[i]
    hit, t = ray_cast(origin, direction, np.array([obj_b.matrix_world @ v.co for v in mesh_b.vertices]), faces_b)
    if hit:
        hit_vertex_ids.append(i)
        print(f"Hit at t={t} from vertex {i}")
    else:
        print(f"No hit from vertex {i}")

print("Hit vertex IDs:", hit_vertex_ids)
