"""
해당 파일은 작성자가 짠 코드가 아니며 핸드폰으로 코드를 읽기 위해 업로드했을 뿐이다
출처는 아래와 같다
https://blenderartists.org/t/revised-mesh-tension-add-on/1239091
"""

bl_info = {
    "name": "Mesh Tension",
    "author": "Steve Miller",
    "version": (1, 3, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Mesh Data",
    "description": "Stores mesh tension in vertex colours and vertex groups",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}

import bpy
import bmesh
from mathutils import Vector
from bpy.app.handlers import persistent

skip = skip_dg_pre = skip_dg_post = False
rendering = False

generative_modifiers = ['ARRAY','BEVEL','BOOLEAN', 'BUILD', 'DECIMATE','EDGE_SPLIT','MASK','MIRROR','MULTIRES','REMESH','SCREW','SKIN','SOLIDIFY','SUBSURF','TRIANGULATE','WELD','WIREFRAME']
bmeshes = []

#maintains list of objects to calculate tension
#only uses the first object instance of a mesh it encounters
def call_list_refresh(self,context):
    list_refresh()
    
def list_refresh():
    global bmeshes
    for bm in bmeshes:
        bm.free()
    bmeshes.clear()
    
    tp = bpy.context.scene.tension_props
    tp.objects.clear()
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH' and ob.data.tension_props.enable:
            dup = False
            for o2 in tp.objects:
                ob2 = context.scene.objects[o2.name]
                if ob2.data.name == ob.data.name:
                    dup=True
            if dup: continue
        
            o = tp.objects.add()
            o.name = ob.name
            bm = bmesh.new()
            bm.from_mesh(ob.data)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bmeshes.append(bm)
                       
def get_vcol(ob,name):
    vcol = ob.data.vertex_colors.get(name)
    if not vcol:
        vcol = ob.data.vertex_colors.new(name=name)
    return vcol

def get_vgroup(ob,name):
    vgroup = ob.vertex_groups.get(name)
    if not vgroup:
        vgroup = ob.vertex_groups.new(name=name)
    return vgroup
            
def call_mask_refresh(self,context):
    mask_refresh(context.object)

def mask_refresh(ob):
    mask_index = ob.vertex_groups.find(ob.data.tension_props.vgroup)
    if mask_index == -1:
        ob.data['tension_mask'] = [v.index for v in ob.data.vertices]
    else:
        ob.data['tension_mask'] = [v.index for v in ob.data.vertices if mask_index in [vg.group for vg in v.groups]]
    
    #refresh maps and groups   
    tm = get_vcol(ob,'tension_map')
    for index in tm.data:
        index.color = (0,0,0,0)
    s = ob.vertex_groups.get('tension_stretch')
    if s: ob.vertex_groups.remove(s)
    c = ob.vertex_groups.get('tension_compress')
    if c: ob.vertex_groups.remove(c)
    

#validate that we should be always updating
def valid_always_update(scene):
    if not scene.render.use_lock_interface: return False #safety measure
    if not scene.tension_props.enable: return False #effect globally disabled
    if rendering: return False #rendering
    if bpy.context.screen.is_animation_playing: return False #already frame change updating
    return True #always update tagged object

@persistent
def render_pre(scene):
    global rendering
    rendering = True

def tension_pre(ob):
    global generative_modifiers, skip_dg_pre
            
    #disable modifiers that are generative or dependant on tension vertex groups
    #store their state for restoring
    delayed_modifiers = ob.data.tension_props.delayed_modifiers
    delayed_modifiers.clear()
    
    def delay_modifier(m,delayed_modifiers):
        dm = delayed_modifiers.add()
        dm.name = m.name
        dm.viewport = m.show_viewport
        dm.render = m.show_render
        m.show_viewport = False
        m.show_render = False
        
    for m in ob.modifiers:
        if hasattr(m,'vertex_group'):
            if m.vertex_group in ['tension_compress', 'tension_stretch']:
                delay_modifier(m, delayed_modifiers)
                continue
        if m.type in generative_modifiers:
            delay_modifier(m, delayed_modifiers)
            continue
        if m.name[-11:].upper() == 'SKIPTENSION':
            delay_modifier(m, delayed_modifiers)
            continue

@persistent
def dg_update_pre(scene):
    global skip_dg_pre, skip_dg_post
    if skip_dg_pre or skip_dg_post: return

    if not valid_always_update(scene):
        #print('no ' + str(scene.frame_current))
        return
    #print('yes ' + str(scene.frame_current))
    
    #otherwise we have a tension mesh that we can update
    skip_dg_pre = True #prevent recursion
    
    for o in scene.tension_props.objects:
        ob = scene.objects.get(o.name)
        if not ob:
            list_refresh()
            return
        if ob.data.tension_props.always_update and ob.mode == 'OBJECT': tension_pre(ob)
        
    skip_dg_pre = False

@persistent    
def frame_pre(scene):
    global skip
    if skip: return

    if not scene.tension_props.enable: return
    if not scene.render.use_lock_interface: return
    
    for o in scene.tension_props.objects:
        ob = scene.objects.get(o.name)
        if not ob:
            list_refresh()
            return
        if ob.mode == 'OBJECT': tension_pre(ob)

def tension_post(i,scene,dg):
    global bmeshes
    spread_mask = []
    spread_tension = []
    
    ob = scene.objects.get(scene.tension_props.objects[i].name)
    ob_eval = ob.evaluated_get(dg)
    
    bm = ob_eval.data 

    #generate tension mask if it doesn't exist
    if ob.data.get('tension_mask') is None: mask_refresh(ob)
    if len(bmeshes) <= i: list_refresh()
    bm_orig = bmeshes[i]
    bias = ob.data.tension_props.bias
    
    tension_map = get_vcol(ob, 'tension_map')
    stretch_group = get_vgroup(ob, 'tension_stretch')
    compress_group = get_vgroup(ob, 'tension_compress')
    
    #iterate through verts in mask
    for v_index in ob.data['tension_mask']:
        v = bm_orig.verts[v_index]
        t = 0
        for e in v.link_edges:
            e_def = bm.edges[e.index]
            e_def_length=(bm.vertices[e_def.vertices[0]].co - bm.vertices[e_def.vertices[1]].co).length
            e_stretch = e_def_length/e.calc_length()
            t += e_stretch
        t = t/len(v.link_edges)
        t = (1-t)
        
        #store tighter list of verts with tension, and corresponding list of tensions
        if abs(t)>.001:
            spread_mask.append(v_index)
            spread_tension.append(t)
      
    flip = (ob.data.tension_props.spread < 0)
    for iter in range(abs(ob.data.tension_props.spread)):
        spread_tension_last = spread_tension.copy()
        count = len(spread_mask)
        for i1 in range(count):
            v_index = spread_mask[i1]
            v = bm_orig.verts[v_index]
            v_tension = spread_tension_last[spread_mask.index(v_index)]
            for e in v.link_edges:
                v2 = e.other_vert(v)
                if not v2.index in ob.data['tension_mask']: continue
                if not v2.index in spread_mask:
                    spread_mask.append(v2.index)
                    spread_tension.append(0)
                i2 = spread_mask.index(v2.index)
                if flip:
                    spread_tension[i2] = max(v_tension, spread_tension[i2])
                else:
                    spread_tension[i2] = min(v_tension, spread_tension[i2])
        del spread_tension_last
            
    for v_index in ob.data['tension_mask']:
        v = bm_orig.verts[v_index]
        t = 0
        if v.index in spread_mask:
            t = spread_tension[spread_mask.index(v.index)]*ob.data.tension_props.strength
            
        stretch_group.add([v.index], sorted((0,-t+bias,1))[1], 'REPLACE')
        compress_group.add([v.index], sorted((0,t-bias,1))[1], 'REPLACE')    
        for l in v.link_loops:
            if t < 0:
                tension_map.data[l.index].color = (0, -t+bias, 0, 1.0)
            else:
                tension_map.data[l.index].color = (t-bias,0,0,1.0)
            
   
    delayed_modifiers = ob.data.tension_props.delayed_modifiers
    for m in delayed_modifiers:
        if m.name in ob.modifiers:
            ob.modifiers[m.name].show_viewport = m.viewport
            ob.modifiers[m.name].show_render = m.render

@persistent
def dg_update_post(scene,dg):
    global skip_dg_post, skip_dg_pre

    if skip_dg_pre or skip_dg_post: return
    if not valid_always_update(scene): return
    
    #otherwise we have a tension mesh that we can update
    skip_dg_post = True
    for i,o in enumerate(scene.tension_props.objects):
        ob = scene.objects.get(o.name)
        if ob.data.tension_props.always_update and ob.mode == 'OBJECT': tension_post(i,scene,dg)
    skip_dg_post = False

@persistent
def frame_post(scene,dg):
    global skip, rendering
    if skip: return
    
    if not scene.tension_props.enable: return
    if not scene.render.use_lock_interface: return

    for i,o in enumerate(scene.tension_props.objects):
        ob = scene.objects.get(o.name)
        if ob.mode == 'OBJECT': tension_post(i,scene,dg)
                 
    if not rendering: return
    #render needs this update
    skip = True       
    scene.frame_set(scene.frame_current)
    skip = False
        
@persistent
def render_post(scene):
    global rendering
    rendering = False
    
@persistent
def load_post(scene):
    list_refresh()

class MaskRefreshOperator(bpy.types.Operator):
    """Refresh Mask"""
    bl_idname="id.mask_refresh"
    bl_label="Refresh Mask"
    @classmethod
    def poll(cls,context):
        return True
    def execute(self,context):
        mask_refresh(context.object)
        return{'FINISHED'}

class TensionMeshPanel(bpy.types.Panel):
    bl_label = 'Tension Maps'
    bl_idname = 'MESH_PT_tension'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'
    
    def draw_header(self,context):
        if not context.scene.render.use_lock_interface:
            self.layout.enabled = False
        self.layout.prop(context.object.data.tension_props, 'enable', text='')
    def draw(self,context):
        global generative_modifiers
        if context.scene.render.use_lock_interface:
            self.layout.use_property_split = True
            ob = context.object
            self.layout.prop(ob.data.tension_props, 'strength')
            self.layout.prop(ob.data.tension_props, 'bias')
            self.layout.prop(ob.data.tension_props, 'spread')
            row = self.layout.row()
            row.prop_search(ob.data.tension_props, 'vgroup', ob, 'vertex_groups')
            row.operator('id.mask_refresh',text='',icon='FILE_REFRESH')
            self.layout.prop(ob.data.tension_props, 'always_update')
        else:
            self.layout.label(text="Enable 'Render > Lock Interface' to use")
        
class TensionScenePanel(bpy.types.Panel):
    bl_label = 'Tension Maps'
    bl_idname = 'SCENE_PT_tension'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    
    def draw_header(self,context):
        if not context.scene.render.use_lock_interface:
            self.layout.enabled = False
        self.layout.prop(context.scene.tension_props, 'enable', text='')
    def draw(self,context):
        if not context.scene.render.use_lock_interface:
            self.layout.label(text="Enable 'Render > Lock Interface' to use")

class TensionItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name')
    viewport: bpy.props.BoolProperty(name='Show Viewport')
    render: bpy.props.BoolProperty(name='Show Render')
    
class TensionMeshProps(bpy.types.PropertyGroup):
    enable: bpy.props.BoolProperty(name = 'Enable', default=False,update=call_list_refresh)
    strength: bpy.props.FloatProperty(name = 'Strength', default=1.0)
    bias: bpy.props.FloatProperty(name = 'Bias', default=0.0)
    spread: bpy.props.IntProperty(name = 'Spread Iterations', default = 0, soft_min=-4, soft_max=4)
    vgroup: bpy.props.StringProperty(name = 'Vertex Mask',update=call_mask_refresh)
    vlist: bpy.props.IntVectorProperty()
    delayed_modifiers: bpy.props.CollectionProperty(type=TensionItem)
    always_update: bpy.props.BoolProperty(name = 'Always Update', description='Update even when animation not playing (may impact general viewport performance).', default = False)

class TensionSceneProps(bpy.types.PropertyGroup):
    enable: bpy.props.BoolProperty(name = 'Enable', default=True,update=call_list_refresh)
    objects: bpy.props.CollectionProperty(type=TensionItem)

# register classes and properties
def register():

    bpy.utils.register_class(TensionItem)
    bpy.utils.register_class(TensionMeshProps)
    bpy.utils.register_class(TensionSceneProps)
    
    bpy.types.Mesh.tension_props = bpy.props.PointerProperty(type=TensionMeshProps)
    bpy.types.Scene.tension_props = bpy.props.PointerProperty(type=TensionSceneProps)
    
    bpy.utils.register_class(MaskRefreshOperator)
    bpy.utils.register_class(TensionMeshPanel)
    bpy.utils.register_class(TensionScenePanel)

#    bpy.app.handlers.frame_change_post.clear()
#    bpy.app.handlers.frame_change_pre.clear()
#    bpy.app.handlers.render_pre.clear()
#    bpy.app.handlers.render_post.clear()
#    bpy.app.handlers.depsgraph_update_pre.clear()
#    bpy.app.handlers.depsgraph_update_post.clear()
    
    bpy.app.handlers.load_post.append(load_post)
    bpy.app.handlers.frame_change_post.append(frame_post)
    bpy.app.handlers.frame_change_pre.append(frame_pre)
    bpy.app.handlers.render_pre.append(render_pre)
    bpy.app.handlers.render_post.append(render_post)
    bpy.app.handlers.depsgraph_update_pre.append(dg_update_pre)
    bpy.app.handlers.depsgraph_update_post.append(dg_update_post)

def unregister():
    bpy.utils.unregister_class(TensionItem)
    bpy.utils.unregister_class(TensionMeshProps)
    bpy.utils.unregister_class(TensionSceneProps)
    
    del bpy.types.Mesh.tension_props
    del bpy.types.Scene.tension_props
    
    bpy.utils.unregister_class(MaskRefreshOperator)
    bpy.utils.unregister_class(TensionMeshPanel)
    bpy.utils.unregister_class(TensionScenePanel)
    
    bpy.app.handlers.load_post.remove(load_post)
    bpy.app.handlers.frame_change_post.remove(frame_post)
    bpy.app.handlers.frame_change_pre.remove(frame_pre)
    bpy.app.handlers.render_pre.remove(render_pre)
    bpy.app.handlers.render_post.remove(render_post)
    bpy.app.handlers.depsgraph_update_pre.remove(dg_update_pre)
    bpy.app.handlers.depsgraph_update_post.remove(dg_update_post)
    
if __name__ == "__main__":
    register()
