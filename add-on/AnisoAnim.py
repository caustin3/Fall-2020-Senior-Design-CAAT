bl_info = {
    "name": "Anisotropic Animation",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class aniso_anim(bpy.types.Operator):
    """Open the Anisotropic Animation Dialog Box"""
    bl_label = "Anisotropic Animation"
    bl_idname = "wm.myop"
    mat = bpy.props.StringProperty(name= "Material Type", default= "")
    mesh = bpy.props.StringProperty(name= "Mesh File Name", default= "")
    frames = bpy.props.IntProperty(name= "Frames", default=60)
    fps = bpy.props.IntProperty(name= "FPS", default=60)
    gravity = bpy.props.FloatProperty(name = "Gravity", default = -9.8)
    def execute(self, context):
        t = self.mat
        m = self.mesh
        fr = self.frames
        fp = self.fps
        g = self.gravity
        #Run animation script here
        
        return{'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
    
def menu_func(self, context):
    self.layout.operator(aniso_anim.bl_idname)
    
def register():
    bpy.utils.register_class(aniso_anim)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(aniso_anim)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()
    
    bpy.ops.wm.myop('INVOKE_DEFAULT')