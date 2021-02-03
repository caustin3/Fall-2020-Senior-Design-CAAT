# Addison Dugal
# Team CAAT
# Blender Add-on Prototype
#
# To run in Blender:
# Edit -> Preferences -> Add-Ons -> Install -> select this file

bl_info = {
    "name": "CAAT Add-On",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class Test(bpy.types.Operator):
    """CAAT Blender Add-on"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.test"        # Unique identifier for buttons and menu items to reference.
    bl_label = "CAAT Test Add-on"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        scene = context.scene
        obj = context.active_object
        print("Add-on executing")
        # Insert tearing algorithms here

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def register(): # Called when add-on is enabled
    print("Add-on Enabled")
    bpy.utils.register_class(Test)

def unregister(): # Called when add-on is disabled; should un-load what is done in register
    print("Add-on Disabled")
    bpy.utils.unregister_class(Test)