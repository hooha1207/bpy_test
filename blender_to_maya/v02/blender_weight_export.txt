bl_info = {
    "name": "Export Weight to maya",
    "author": "hooha",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "location": "File > Export > Weight (.txt)",
    "description": "Export Weight (.txt)",
    "warning": "",
    "wiki_url": "",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}



import os
import bpy
import json

from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty
from bpy_extras.io_utils import ExportHelper


filename = 'weight_test'
path = 'C:'+ os.environ['HOMEPATH'] +'/Desktop'
filepath = f'{path}/{filename}'

weight_threshold = 0.0001







class nameError(Exception):
    def __init__(self):
        super().__init__('Check name bones what i using "." or other special signs')



def write_json(context, filepath, weight_threshold, weight_round):
    f = open(filepath, 'w+')
    fw = f.write
    
    depsgraph = bpy.context.evaluated_depsgraph_get()

    total_json = []

    for ob in bpy.context.selected_objects:
        armt_obs = []
        for modf in ob.modifiers:
            if modf.type =='ARMATURE':
               armt_obs.append(modf.object)
        
        jnt_ns = []
        for armt in armt_obs:
            for b in armt.data.bones:
                jnt_ns.append(b.name)
        
        vis_ob = depsgraph.objects[ob.name]
        
        if not len(vis_ob.data.vertices) == len(ob.data.vertices):
            vis_ob = ob
        
        ob_w = []
        for v in vis_ob.data.vertices:
            dict = {'vid':v.index}
            for vg in v.groups:
                if vis_ob.vertex_groups[vg.group].name in jnt_ns:
                    if round(vg.weight, 3) > weight_threshold:
                        dict[vis_ob.vertex_groups[vg.group].name] = round(vg.weight, weight_round)
            ob_w.append(dict)
        total_json.append(json.dumps({vis_ob.name:ob_w}))

    fw(json.dumps(total_json))
    f.close()




class WeightsExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "export_weight.objects"
    bl_label = "Export"

    filename_ext = ".txt"
    filepath: StringProperty(default=filepath, options={'HIDDEN'})

    weight_threshold: FloatProperty(name="Weight Threshold",
            description="Weight threshold for export",
            default=0.0001, max=1.0)
    
    weight_round: IntProperty(name="Weight Threshold",
            description="Weight threshold for export",
            default=4, max=6)

    
    def execute(self, context):
        write_json(context, self.filepath, self.weight_threshold, self.weight_round)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}




def menu_export(self, context):
    default_path = path
    self.layout.operator(WeightsExporter.bl_idname, text="Weights (.txt)")

def register():
    bpy.utils.register_class(WeightsExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_export)

def unregister():
    bpy.utils.unregister_class(WeightsExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export)

if __name__ == "__main__":
    register()
