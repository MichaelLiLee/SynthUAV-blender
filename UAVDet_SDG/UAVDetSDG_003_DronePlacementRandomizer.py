""" DronePlacementRandomizer

reference:
[Evenly distributing n points on a sphere](https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere)
[Seanmatthews/fibonacci_sphere.py](https://gist.github.com/Seanmatthews/a51ac697db1a4f58a6bca7996d75f68c)  
[3D Scatter Plots in Python](https://plotly.com/python/3d-scatter-plots/)  
[Python: Check if vertex is on camera field of view [duplicate]](https://blender.stackexchange.com/questions/32975/python-check-if-vertex-is-on-camera-field-of-view)  
[bpy_extras.object_utils.world_to_camera_view](https://docs.blender.org/api/current/bpy_extras.object_utils.html#bpy_extras.object_utils.object_add_grid_scale_apply_operator)  
[Rendering in blender dont take rotation updates of camera and light directions](https://stackoverflow.com/questions/64628823/rendering-in-blender-dont-take-rotation-updates-of-camera-and-light-directions)  
[No updates after setting values](https://docs.blender.org/api/current/info_gotcha.html)  

""" 

import bpy
import random
import numpy as np
import os
import sys
import glob
import math
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

class DronePlacementRandomizer:
    def __init__(self,
                drone_asset_folder_path = "C:/Users/user/Documents/project/UAVDet/Asset/UAV/Edited",
                drone_num_in_scene = 1,
                fibonacci_sphere_radius_range = {"min":5, "max":50}
                ):

        self.drone_collection = bpy.data.collections["DroneCollection"]
        self.drone_asset_folder_path = drone_asset_folder_path
        self.drone_num_in_scene = drone_num_in_scene
        self.fibonacci_sphere_radius_range = fibonacci_sphere_radius_range
        self.fibonacci_sphere_radius = 5 #random change by __create_random_fibonacci_sphere
        self.fibonacci_sphere_sample_area = 1
        self.fibonacci_sphere_sample_num = 10 #random change by __create_random_fibonacci_sphere
        self.sphere_points = list()
        self.cam_view_visual_points = list()

    def __error_check(self,asset_path_list):
        """
        """
        num_asset_in_folder = len(asset_path_list)
        if num_asset_in_folder < 1:
            print(f'ERROR!!! can not find any drone asset in {self.drone_asset_folder_path}')
            input("Press Enter to continue...")
            sys.exit()

    def __fibonacci_sphere(self, r = 1, samples = 100):
        """
        """
        points = []
        phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

        for i in range(samples):
            y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
            radius = math.sqrt(1 - y * y)  # radius at y
            theta = phi * i  # golden angle increment
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius

            # just return upper sphere points
            if z < 0:
                continue

            x,y,z=r*x,r*y,r*z
            points.append((x, y, z))

        return points

    def __create_random_fibonacci_sphere(self):
        """
        1.random select fibonacci_sphere_radius
        2.caculate sphere_area
        3.caculate fibonacci_sphere_sample_num accroding to fibonacci_sphere_sample_area
        4.return fibonacci_sphere points coordinate
        """
        ## 1.random select fibonacci_sphere_radius
        fibonacci_sphere_radius_max = int(self.fibonacci_sphere_radius_range["max"])
        fibonacci_sphere_radius_min = int(self.fibonacci_sphere_radius_range["min"])
        self.fibonacci_sphere_radius = random.randrange(fibonacci_sphere_radius_min, fibonacci_sphere_radius_max, 1)

        ##2.caculate sphere_area
        sphere_area = 4 * math.pi * self.fibonacci_sphere_radius * self.fibonacci_sphere_radius

        ## 3.caculate fibonacci_sphere_sample_num accroding to fibonacci_sphere_sample_area
        self.fibonacci_sphere_sample_num = round(sphere_area/self.fibonacci_sphere_sample_area)

        ## 4.return fibonacci_sphere points coordinate
        self.sphere_points = self.__fibonacci_sphere(r = self.fibonacci_sphere_radius, samples = self.fibonacci_sphere_sample_num)

        print(f'fibonacci_sphere_radius : {self.fibonacci_sphere_radius}')
        print(f'fibonacci_sphere_sample_num : {self.fibonacci_sphere_sample_num}')
        print(f'sphere_points_num : {len(self.sphere_points)}')

    def __load_obj_from_blend_file(self,filepath,collection):
        """
        """ 
        ## append object from .blend file
        with bpy.data.libraries.load(filepath, link = False,assets_only = True) as (data_from, data_to):
            data_to.objects = data_from.objects
        ## link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                collection.objects.link(obj)

    def __import_drone_asset(self):
        """ 
        """ 
        ## get vehicle asset path
        drone_asset_path_list = glob.glob(os.path.join(self.drone_asset_folder_path, "*.blend"))
        self.__error_check(asset_path_list = drone_asset_path_list)
        num_drone_asset = len(drone_asset_path_list)
        print(f"num vehicle asset in {self.drone_asset_folder_path} folder: {num_drone_asset}")

        ##randomly select k(k = drone_num_in_scene) drone asset from drone_asset_path_list, then import to DroneCollection
        drone_asset_path_list_selected = random.choices(drone_asset_path_list, k = self.drone_num_in_scene)
        for drone_asset_path in drone_asset_path_list_selected:
            self.__load_obj_from_blend_file(filepath=drone_asset_path, collection=self.drone_collection)

    def __check_cam_view_visual_sphere_points(self):
        """ 
        """ 
        ## forced update view_layer
        bpy.context.view_layer.update()

        scene = bpy.context.scene
        cam = bpy.data.objects['Camera']
        cs, ce = cam.data.clip_start, cam.data.clip_end
        visual_points = list()
        ## check which sphere points in camera view
        for p in self.sphere_points:
            vector_p = Vector(p)
            co_ndc = world_to_camera_view(scene, cam, vector_p)
            #check wether point is inside frustum
            if (0.0 < co_ndc.x < 1.0 and 0.0 < co_ndc.y < 1.0 and cs < co_ndc.z <  ce):
                visual_points.append(p)
        print(f'num sphere points in cam view :{len(visual_points)}')

        ## return visual_points to self.cam_view_visual_points
        self.cam_view_visual_points = visual_points
        
    def drone_placement_randomize(self):
        """ 
        """ 
        ## create random fibonacci sphere
        self.__create_random_fibonacci_sphere()
        ##　check　cam　view　visual　sphere　points
        self.__check_cam_view_visual_sphere_points()
        ## import drone asset
        self.__import_drone_asset()

        ## move drone asset to random visual sphere points
        drone_asset_list = list()
        drone_locations_list =list()

        for drone_asset in self.drone_collection.objects:
           drone_asset_list.append(drone_asset)

        drone_locations_indices = np.random.choice(len(self.cam_view_visual_points), size = self.drone_num_in_scene, replace = False)
        for index in drone_locations_indices:
            drone_locations_list.append(self.cam_view_visual_points[index])

        for i in range(self.drone_num_in_scene):
            drone_location = (drone_locations_list[i][0],drone_locations_list[i][1], drone_locations_list[i][2])
            drone_asset_list[i].location = drone_location
            print(f'move {drone_asset_list[i].name} to {drone_location}')

        print("Drone Placement Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = DronePlacementRandomizer()
    randomizer.drone_placement_randomize()








    




    
    