import bpy
from bpy_extras import view3d_utils
import mathutils







class ViewOperatorRayCast(bpy.types.Operator):
    """Modal object selection with a ray cast"""
    bl_idname = "view3d.modal_operator_raycast"
    bl_label = "RayCast View Operator"

    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # allow navigation
            return {'PASS_THROUGH'}
        
        elif event.type == 'LEFTMOUSE':
            def main(context, event):
                """Run this function on left mouse, execute the ray cast"""
                # get the context arguments
                scene = context.scene
                region = context.region # [k for k in [i for i in bpy.context.screen.areas if i.type=='VIEW_3D'][0].regions if k.type == 'WINDOW'][0] 로 얻을 수 있음. 해당 객체는 VIEW_3D에 존재하는 ui rgion 중 WINDOW 타입을 출력한다
                rv3d = context.region_data # [i for i in bpy.context.screen.areas if i.type=='VIEW_3D'][0].spaces[0].region_3d 로 얻을 수 있음
                coord = event.mouse_region_x, event.mouse_region_y # region 내부에 상대적인 좌표를 찾는다고 하며, mouse_x와는 다른 결과를 도출해낸다 (mouse_x, mouse_y로 출력된 값을 사용할 경우, z축이 반전된다)
                # get the ray from the viewport and mouse
                view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)

                ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord) # viewport camera의 position vector


                ray_target = ray_origin + view_vector

                def visible_objects_and_duplis():
                    """Loop over (object, matrix) pairs (mesh only)"""

                    depsgraph = context.evaluated_depsgraph_get() # 모디파이어로 인해 변형된 mesh의 데이터를 가져올 수 있는 기능. 최종 상태의 object를 얻을 수 있다
                    print(depsgraph)
                    for dup in depsgraph.object_instances:
                        # print(dup)
                        print(dir(dup))
                        if dup.is_instance:  # Real dupli instance
                            obj = dup.instance_object
                            yield (obj, dup.matrix_world.copy())
                        else:  # Usual object
                            obj = dup.object
                            yield (obj, obj.matrix_world.copy())

                def obj_ray_cast(obj, matrix):
                    """Wrapper for ray casting that moves the ray into object space"""

                    # get the ray relative to the object
                    matrix_inv = matrix.inverted()
                    ray_origin_obj = matrix_inv @ ray_origin
                    ray_target_obj = matrix_inv @ ray_target
                    ray_direction_obj = ray_target_obj - ray_origin_obj

                    # cast the ray
                    success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

                    if success:
                        return location, normal, face_index
                    else:
                        return None, None, None

                # cast rays and find the closest object
                best_length_squared = -1.0
                best_obj = None

                for obj, matrix in visible_objects_and_duplis():
                    if obj.type == 'MESH':
                        hit, normal, face_index = obj_ray_cast(obj, matrix)
                        if hit is not None:
                            hit_world = matrix @ hit
                            scene.cursor.location = hit_world
                            length_squared = (hit_world - ray_origin).length_squared
                            if best_obj is None or length_squared < best_length_squared:
                                best_length_squared = length_squared
                                best_obj = obj

                # now we have the object under the mouse cursor,
                # we could do lots of stuff but for the example just select.
                if best_obj is not None:
                    # for selection etc. we need the original object,
                    # evaluated objects are not in viewlayer
                    best_original = best_obj.original
                    best_original.select_set(True)
                    context.view_layer.objects.active = best_original
            
            # out of view3d area
            view3d_areas = [[i.x, i.y, i.width, i.height, i.type] for i in context.screen.areas if i.type=='VIEW_3D']
            for x,y,w,h,t in view3d_areas:
                if event.mouse_x < x or event.mouse_x > (x+w) or event.mouse_y < y or event.mouse_y > (y+h):
                    return {'PASS_THROUGH'}
            
            main(context, event)
            return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ViewOperatorRayCast.bl_idname, text="Raycast View Modal Operator")


# Register and add to the "view" menu (required to also use F3 search "Raycast View Modal Operator" for quick access).
def register():
    bpy.utils.register_class(ViewOperatorRayCast)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ViewOperatorRayCast)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()