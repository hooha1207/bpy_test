import bpy
from mathutils import Vector
import mathutils
import math
from math import pi




clockwise = True

rot = mathutils.Euler((0,0,0))

class ModalTimerOperator(bpy.types.Operator):
    bl_idname = "custom_mode_test.rotate_y_viewport"
    bl_label = "Rotate_y viewport"

    r_press : bpy.props.BoolProperty(name='r_press')
    mc_x : bpy.props.IntProperty(name='middle_coord_x')
    mc_y : bpy.props.IntProperty(name='middle_coord_y')
    mp : bpy.props.FloatVectorProperty(name='mp')
    dv : bpy.props.FloatVectorProperty(name='dv')
    before_x : bpy.props.IntProperty(name='before_x')
    before_y : bpy.props.IntProperty(name='before_y')

    def modal(self, context, event):
        if event.type in {'ESC'}:
            return {'CANCELLED'}
        if event.type =='RIGHTMOUSE' and event.value == 'PRESS' and event.alt:
            print('success')
            self.r_press = True
            self.mc_x = int(context.area.width/2)
            self.mc_y = int(context.area.height/2)
            self.before_x = event.mouse_region_x-self.mc_x
            self.before_y = event.mouse_region_y-self.mc_y
            
        elif event.type == 'MOUSEMOVE' and self.r_press:
            
            
            self.mp = Vector((event.mouse_region_x-self.mc_x, event.mouse_region_y-self.mc_y, 0)).normalized()
            self.dv = (Vector(self.mp) - (Vector((self.before_x, self.before_y, 0)).normalized())).normalized()
            
            
            if Vector(self.mp).x>0 and Vector(self.mp).y>0 and Vector(self.dv).x<0 and Vector(self.dv).y>0:
#                clockwise = True
#                self.clockwise = 1
                clockwise = 1
#                print('0~90')
            elif Vector(self.mp).x<0 and Vector(self.mp).y>0 and Vector(self.dv).x<0 and Vector(self.dv).y<0:
#                clockwise = True
#                self.clockwise = 1
                clockwise = 1
#                print('90~180')
            elif Vector(self.mp).x<0 and Vector(self.mp).y<0 and Vector(self.dv).x>0 and Vector(self.dv).y<0:
#                clockwise = True
#                self.clockwise = 1
                clockwise = 1
#                print('180~270')
            elif Vector(self.mp).x>0 and Vector(self.mp).y<0 and Vector(self.dv).x>0 and Vector(self.dv).y>0:
#                clockwise = True
#                self.clockwise = 1
                clockwise = 1
#                print('270~360')
            else:
#                clockwise = False
#                self.clockwise = -1
                clockwise = -1
            
            self.before_x = event.mouse_region_x-self.mc_x
            self.before_y = event.mouse_region_y-self.mc_y
            
#            print(clockwise)
            
            
            rot = context.space_data.region_3d.view_rotation.to_euler()
            rot.rotate_axis('Z',(-1*clockwise)*pi/45)
            
            context.space_data.region_3d.view_rotation = rot.to_quaternion()

            
        elif event.type =='RIGHTMOUSE' and event.value == 'RELEASE' and self.r_press:
            print('done')
            self.r_press = False
#            return {'RUNNING_MODAL'}
        else:
            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    
    def invoke(self, context, event):

        if context.space_data.type == 'VIEW_3D':
            v3d = context.space_data
            rv3d = v3d.region_3d

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ModalTimerOperator.bl_idname, text=ModalTimerOperator.bl_label)


def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)


# Register and add to the "view" menu (required to also use F3 search "Modal Timer Operator" for quick access).
def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.custom_mode_test.rotate_y_viewport()
