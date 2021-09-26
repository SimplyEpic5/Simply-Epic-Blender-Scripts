# AutoDynamics.py - A script that automatically switches rigid body objects from animated 
# to dynamic based on proximity to an object

import bpy

# Modify these variables to configure the script:
dynamicsCollectionName = "AutoDynamics"     # Name of the collection containing the objects you want dynamics auto set for
triggerObjName = "Sphere"                   # Name of the object you want to use to trigger dynamics by distance
resetFrame = 1                              # Frame dynamics should be reset before (set to a frame before any objects become dynamic)
triggerDistance = 2.8                       # Set to the minimum disatnce from the trigger object an object should be before dynamics are set

# ===== Script Begins =====

collection = bpy.data.collections[dynamicsCollectionName]
triggerObj = bpy.data.objects[triggerObjName]

for obj in collection.all_objects:
    obj["isDynamic"] = 0
    obj.rigid_body.enabled = False
    obj.rigid_body.kinematic = True

def autoDynamics(scene):
    frame_num = bpy.context.scene.frame_current
    
    if frame_num <= resetFrame:
        for obj in collection.all_objects:
            obj["isDynamic"] = 0
            obj.rigid_body.enabled = False
            obj.rigid_body.kinematic = True
    else:
        for obj in collection.all_objects:
            if not obj["isDynamic"]:
                # If the object is not dynamic, check if it should be set
                loc0 = triggerObj.location
                loc1 = obj.location
                dist = (loc0 - loc1).length
                
                if (dist < triggerDistance):
                    # Object is close enough, trigger dynamics
                    obj["isDynamic"] = 1
                    obj.rigid_body.enabled = True
                    obj.rigid_body.kinematic = False

bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(autoDynamics)