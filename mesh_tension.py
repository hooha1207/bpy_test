bl_info = {
    "name": "Mesh Tension",
    "author": "Steve Miller",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Mesh Data",
    "description": "Stores mesh tension in vertex colours and vertex groups",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}

import bpy
import bmesh
from bpy.app.handlers import persistent

skip = skip_dg_pre = skip_dg_post = False
rendering = False

generative_modifiers = ['ARRAY','BEVEL','BOOLEAN', 'BUILD', 'DECIMATE','EDGE_SPLIT','MASK','MIRROR','MULTIRES','REMESH','SCREW','SKIN','SOLIDIFY','SUBSURF','TRIANGULATE','WELD','WIREFRAME']

#maintains list of objects to calculate tension
#only uses the first object instance of a mesh it encounters
def call_list_refresh(self,context):
    list_refresh()
    
def list_refresh():
    objects = bpy.context.scene.tension_props.objects
    objects.clear()
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH' and ob.data.tension_props.enable and ob.data.name not in objects:
            o = objects.add()
            o.name = ob.name

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

@persistent
def dg_update_pre(scene):
    global skip_dg_pre, skip_dg_post
    if skip_dg_pre or skip_dg_post: return

    if not valid_always_update(scene):
        print('no ' + str(scene.frame_current))
        return
    print('yes ' + str(scene.frame_current))
    
    #otherwise we have a tension mesh that we can update
    skip_dg_pre = True #prevent recursion
    
    for o in scene.tension_props.objects:
        ob = scene.objects.get(o.name)
        if not ob:
            list_refresh()
            return
        if ob.data.tension_props.always_update: tension_pre(ob)
        
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
        tension_pre(ob)
        
def tension_post(ob,scene,dg):
    ob_eval = ob.evaluated_get(dg)
    
    #evaluated mesh deformed
    bm = bmesh.new()
    bm.from_mesh(ob_eval.data)
    
    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    #original mesh undeformed
    bm_orig = bmesh.new()
    bm_orig.from_mesh(ob.data)
    #bm_orig.from_object(ob, dg, deform=False)
    bm_orig.edges.ensure_lookup_table()  
    
    #calculate edge stretch:
    edges_stretch = [edge.calc_length() / bm_orig.edges[edge.index].calc_length() for edge in bm.edges]
    
    #calculate vertex tension as average of connected edge tensions
    vert_tension = []
    for v in bm.verts:
        t = 0
        for e in v.link_edges:
            t += edges_stretch[e.index]
        vert_tension.append(t/len(v.link_edges))

    #convert to vertex colours (green for stretch, red for compress) and groups
    tension_map = ob.data.vertex_colors.get('tension_map')
    if not tension_map: tension_map = ob.data.vertex_colors.new(name='tension_map')
    stretch = ob.vertex_groups.get('tension_stretch')
    if not stretch: stretch = ob.vertex_groups.new(name='tension_stretch')
    compress = ob.vertex_groups.get('tension_compress')
    if not compress: compress = ob.vertex_groups.new(name='tension_compress')

    i = 0
    for f in bm.faces:
        for v in f.verts:
            t = (1-vert_tension[v.index])*ob.data.tension_props.strength
            stretch.add([v.index], sorted((0,-t,1))[1], 'REPLACE')
            compress.add([v.index], sorted((0,t,1))[1], 'REPLACE')
            if t < 0: #stretch
                tension_map.data[i].color = (0,-t,0,1.0)
            else: #compresss
                tension_map.data[i].color = (t,0,0,1.0)
            i+= 1

    bm.free()
    bm_orig.free()
    
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
    for o in scene.tension_props.objects:
        ob = scene.objects.get(o.name)
        if ob.data.tension_props.always_update: tension_post(ob,scene,dg)
    skip_dg_post = False

@persistent
def frame_post(scene,dg):
    global skip, rendering
    if skip: return

    if not scene.tension_props.enable: return
    if not scene.render.use_lock_interface: return

    for o in scene.tension_props.objects:
        ob = scene.objects.get(o.name)
        tension_post(ob,scene,dg)
                 
    if not rendering: return
    #render needs this update
    skip = True       
    scene.frame_set(scene.frame_current)
    skip = False
        
@persistent
def render_post(scene):
    global rendering
    rendering = False


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
            self.layout.prop(context.object.data.tension_props, 'strength')
            self.layout.prop(context.object.data.tension_props, 'always_update')
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
    
    bpy.utils.register_class(TensionMeshPanel)
    bpy.utils.register_class(TensionScenePanel)

#    bpy.app.handlers.frame_change_post.clear()
#    bpy.app.handlers.frame_change_pre.clear()
#    bpy.app.handlers.render_pre.clear()
#    bpy.app.handlers.render_post.clear()
#    bpy.app.handlers.depsgraph_update_pre.clear()
#    bpy.app.handlers.depsgraph_update_post.clear()
    
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
    
    bpy.utils.unregister_class(TensionMeshPanel)
    bpy.utils.unregister_class(TensionScenePanel)
    
    bpy.app.handlers.frame_change_post.remove(frame_post)
    bpy.app.handlers.frame_change_pre.remove(frame_pre)
    bpy.app.handlers.render_pre.remove(render_pre)
    bpy.app.handlers.render_post.remove(render_post)
    bpy.app.handlers.depsgraph_update_pre.remove(dg_update_pre)
    bpy.app.handlers.depsgraph_update_post.remove(dg_update_post)
    
if __name__ == "__main__":
    register()