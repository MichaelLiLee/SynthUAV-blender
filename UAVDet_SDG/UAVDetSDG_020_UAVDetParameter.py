""" UAVDetParameter
"""
from dataclasses import dataclass

@dataclass
class UAVdetParameter:
    def __init__(self):
        self.blender_exe_path = "C:/Program Files/Blender Foundation/Blender 3.2/blender" #blender執行檔路徑
        self.max_samples = 256 #採樣數
        self.asset_hdri_env_bg_folder_path = "C:/Users/user/Documents/project/UAVDet_v230301/Asset/hdri_env_bg" #全景圖資產路徑
        self.hdri_env_bg_strength_range = {"min": 0.5 , "max": 1.5} #環境照明強度
        self.clip_end = 150 #最大渲染範圍
        self.camera_pose_x_range = {"min":0, "max":80} #相機隨機姿態:俯仰(Pitch)
        self.camera_pose_y_range = {"min":-10, "max":10} #相機隨機姿態:翻滾(Roll)
        self.camera_pose_z_range = {"min":0, "max":360} #相機隨機姿態:偏航(Yaw)
        self.img_resolution_x = 1920 #影像解析度(寬)
        self.img_resolution_y = 1080 #影像解析度(高)
        self.drone_asset_folder_path = "C:/Users/user/Documents/project/UAVDet_v230301/Asset/UAV/Edited" #無人機資產路徑
        self.drone_num_in_scene = 1 #無人機入鏡數量
        self.fibonacci_sphere_radius_range = {"min":5, "max":50} #無人機距離鏡頭的遠近分佈
        self.x_rotation_range = {"min":-45, "max":45} #無人機隨機姿態:俯仰(Pitch)
        self.y_rotation_range = {"min":-45, "max":45} #無人機隨機姿態:翻滾(Roll)
        self.z_rotation_range = {"min":0, "max":360} #無人機隨機姿態:偏航(Yaw)
        self.output_img_path = "C:/Users/user/Documents/project/UAVDet_v230301/gen_data/images" #渲染照片儲存路徑
        self.output_label_path = "C:/Users/user/Documents/project/UAVDet_v230301/gen_data/labels" #物件標註儲存路徑
        self.obj_name_and_class_id_mapping = {"Drone" : 0} #目標物件與yolo class id 對照
        self.minimum_obj_pixel = 1 #目標物件最小像素