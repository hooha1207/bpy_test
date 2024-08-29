import bpy
import bmesh
import numpy as np



tmp_vvs_l = 99
l_attr_n = 'linkF_v.'
vvs_ls_attr_n = 'vvs_c'
link_level = 0




bpy.ops.object.mode_set(mode='OBJECT')

def get_linkF_v(vs, rvs, obm):
    for v in vs:
        v = obm.verts[v]
        for f in v.link_faces:
            for vv in f.verts:
                if not vv.index in rvs:
                    rvs.append(vv.index)



for ob in bpy.context.selected_objects:
    obm = bmesh.new()
    obm.from_mesh(ob.data)
    obm.verts.ensure_lookup_table()
    obm.faces.ensure_lookup_table()
    obm.edges.ensure_lookup_table()
    
    ob_vvs = []
    ob_vvs_l_total = 0
    ob_vvs_ls = []
    for v in obm.verts:
        vvs = []
        for vlf in v.link_faces:
            for vv in vlf.verts:
                if not vv.index in vvs:
                    vvs.append(vv.index)
        
        if link_level>0:
            for _ in range(link_level):
                get_linkF_v(vvs.copy(), vvs, obm)
        
        vvs.remove(v.index)
        
        vvs_arr = np.zeros(tmp_vvs_l, dtype=np.int32)
        ob_vvs.append(vvs_arr)
        
        
        tmp = 0
        for vid in vvs:
            vvs_arr[tmp] = vid
            tmp+=1
        if len(vvs) > ob_vvs_l_total:
            ob_vvs_l_total = len(vvs)
        
        ob_vvs_ls.append(len(vvs))
    
    ob_vvs_arr = np.array(ob_vvs)
    ob_vvs_arr = ob_vvs_arr[:,:ob_vvs_l_total]
    
    for i in range(ob_vvs_l_total):
        attr = ob.data.attributes.new(f'{l_attr_n}{i}', 'INT', 'POINT')
        for idx,v in enumerate(attr.data):
            v.value = ob_vvs_arr[idx][i]
        
    attr = ob.data.attributes.new(f'{vvs_ls_attr_n}', 'INT', 'POINT')
    for idx,v in enumerate(attr.data):
        v.value = ob_vvs_ls[idx]
