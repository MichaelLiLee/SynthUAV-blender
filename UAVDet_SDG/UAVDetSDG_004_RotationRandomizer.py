""" RotationRandomizer
"""

import bpy
import random
import math
from mathutils import Euler

class RotationRandomizer:
    def __init__(self,
                x_rotation_range = {"min":-45, "max":45},
                y_rotation_range = {"min":-45, "max":45},
                z_rotation_range = {"min":0, "max":365}
                ):

        self.collections_for_rotation_randomize = [bpy.data.collections["DroneCollection"]]
        self.x_rotation_range = x_rotation_range
        self.y_rotation_range = y_rotation_range
        self.z_rotation_range = z_rotation_range


    def rotation_randomize(self):
        """ Applies a random rotation to an object in collections
        """ 
        for collection in self.collections_for_rotation_randomize:
            for obj_to_rotate in collection.objects:

                rotation_x_max = int(self.x_rotation_range["max"])
                rotation_x_min = int(self.x_rotation_range["min"])
                rotation_y_max = int(self.y_rotation_range["max"])
                rotation_y_min = int(self.y_rotation_range["min"])
                rotation_z_max = int(self.z_rotation_range["max"])
                rotation_z_min = int(self.z_rotation_range["min"])

                rotation_x =  random.randrange(rotation_x_min, rotation_x_max, 1)
                rotation_y =  random.randrange(rotation_y_min, rotation_y_max, 1)
                rotation_z =  random.randrange(rotation_z_min, rotation_z_max, 1)

                cam_rot = (math.pi * rotation_x / 180, 
                           math.pi * rotation_y / 180, 
                           math.pi * rotation_z / 180)
                obj_to_rotate.rotation_euler = Euler(cam_rot, 'XYZ')
             
        print("Rotation Randomize COMPLERED !!!")

if __name__ == '__main__':    
    randomizer = RotationRandomizer()
    randomizer.rotation_randomize()