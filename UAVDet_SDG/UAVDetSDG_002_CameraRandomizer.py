""" CameraRandomizer

"""
import bpy
from mathutils import Euler
from math import pi
import random

class CameraRandomizer:
    def __init__(self,
                clip_end = 150,
                camera_pose_x_range = {"min":0, "max":80},
                camera_pose_y_range = {"min":-10, "max":10},
                camera_pose_z_range = {"min":0, "max":360},
                img_resolution_x = 1920,
                img_resolution_y = 1080
                ):
        self.camera_location = (0, 0, 0)
        self.camera_pose = (90, 0, 0)
        self.camera_pose_x_range = camera_pose_x_range
        self.camera_pose_y_range = camera_pose_y_range
        self.camera_pose_z_range = camera_pose_z_range
        self.clip_end = clip_end
        self.img_resolution_x = img_resolution_x
        self.img_resolution_y = img_resolution_y

    def __camera_default_setting(self):
        """ 
        """
        ## set camera location
        bpy.data.objects["Camera"].location = self.camera_location

        ## set camera pose
        cam_rot = (pi*self.camera_pose[0]/180, pi*self.camera_pose[1]/180, pi*self.camera_pose[2]/ 180)
        bpy.data.objects["Camera"].rotation_euler = Euler(cam_rot, 'XYZ')

        ## set camera clip end distance
        bpy.data.cameras["Camera"].clip_end = self.clip_end

        ## set camera resoulation
        bpy.data.scenes['Scene'].render.resolution_x = self.img_resolution_x
        bpy.data.scenes['Scene'].render.resolution_y = self.img_resolution_y

    def __camera_pose_randomize(self):
        """
        """
        ## camera pose randomize
        pose_x_max = int(self.camera_pose_x_range["max"]) + 90
        pose_x_min = int(self.camera_pose_x_range["min"]) + 90
        pose_y_max = int(self.camera_pose_y_range["max"])
        pose_y_min = int(self.camera_pose_y_range["min"])
        pose_z_max = int(self.camera_pose_z_range["max"])
        pose_z_min = int(self.camera_pose_z_range["min"])

        pose_x =  random.randrange(pose_x_min, pose_x_max, 1)
        pose_y =  random.randrange(pose_y_min, pose_y_max, 1)
        pose_z =  random.randrange(pose_z_min, pose_z_max, 1)

        cam_rot = (pi * pose_x / 180, 
                pi * pose_y / 180, 
                pi * pose_z / 180)
        bpy.data.objects["Camera"].rotation_euler = Euler(cam_rot, 'XYZ')

    def camera_randomize(self):
        """
        Camera Randomizer main function
        """
        self.__camera_default_setting()
        self.__camera_pose_randomize()
        
        print("Camera Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = CameraRandomizer()
    randomizer.camera_randomize()