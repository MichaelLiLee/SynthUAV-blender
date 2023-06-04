""" DataGenerator
""" 
## add UAVDet related python files path to system path
import sys
import os
module_path = os.path.dirname(os.path.abspath(__file__))
sys_path_list = []
for p in sys.path:
    sys_path_list.append(p)
if module_path not in sys_path_list:
    sys.path.append(module_path)
## prevent create __pycache__ file
sys.dont_write_bytecode = True

import bpy
from UAVDetSDG_000_Initializer import Initializer
from UAVDetSDG_001_EnvironmentBackgroundRandomizer import EnvironmentBackgroundRandomizer
from UAVDetSDG_002_CameraRandomizer import CameraRandomizer
from UAVDetSDG_003_DronePlacementRandomizer import DronePlacementRandomizer
from UAVDetSDG_004_RotationRandomizer import RotationRandomizer
from UAVDetSDG_010_AutoLabeler import AutoLabeler
from UAVDetSDG_020_UAVDetParameter import UAVdetParameter
import subprocess

class DataGenerator:

     def gen_one_data(self):
        """
        """
        ## component_initialize
        initializer = Initializer()
        uavdet_parameter = UAVdetParameter()
        initializer.max_samples = uavdet_parameter.max_samples
        initializer.init()
        environment_background_randomizer = EnvironmentBackgroundRandomizer()
        camera_randomizer = CameraRandomizer()
        drone_placement_randomizer = DronePlacementRandomizer()
        rotation_randomizer = RotationRandomizer()
        auto_labeler = AutoLabeler()

        ## passing params
        environment_background_randomizer.asset_hdri_env_bg_folder_path = uavdet_parameter.asset_hdri_env_bg_folder_path 
        environment_background_randomizer.hdri_env_bg_strength_range = uavdet_parameter.hdri_env_bg_strength_range
        camera_randomizer.clip_end = uavdet_parameter.clip_end
        camera_randomizer.camera_pose_x_range = uavdet_parameter.camera_pose_x_range
        camera_randomizer.camera_pose_y_range = uavdet_parameter.camera_pose_y_range
        camera_randomizer.camera_pose_z_range = uavdet_parameter.camera_pose_z_range
        camera_randomizer.img_resolution_x = uavdet_parameter.img_resolution_x
        camera_randomizer.img_resolution_y = uavdet_parameter.img_resolution_y
        drone_placement_randomizer.drone_asset_folder_path = uavdet_parameter.drone_asset_folder_path
        drone_placement_randomizer.drone_num_in_scene = uavdet_parameter.drone_num_in_scene
        drone_placement_randomizer.fibonacci_sphere_radius_range = uavdet_parameter.fibonacci_sphere_radius_range
        rotation_randomizer.x_rotation_range = uavdet_parameter.x_rotation_range
        rotation_randomizer.y_rotation_range = uavdet_parameter.y_rotation_range
        rotation_randomizer.z_rotation_range = uavdet_parameter.z_rotation_range
        auto_labeler.output_img_path = uavdet_parameter.output_img_path
        auto_labeler.output_label_path = uavdet_parameter.output_label_path
        auto_labeler.obj_name_and_class_id_mapping = uavdet_parameter.obj_name_and_class_id_mapping
        auto_labeler.minimum_obj_pixel = uavdet_parameter.minimum_obj_pixel
  
        ## main UAVDetSDG process
        environment_background_randomizer.env_bg_randomize()
        camera_randomizer.camera_randomize()
        drone_placement_randomizer.drone_placement_randomize()
        rotation_randomizer.rotation_randomize()
        bpy.context.view_layer.update()## Update view layer
        auto_labeler.auto_labeling()

        print("Gen One Data COMPLERED!!!")
        sys.exit()

if __name__ == '__main__':
    datagen = DataGenerator()
    datagen.gen_one_data()
