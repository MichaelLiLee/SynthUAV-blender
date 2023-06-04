""" EnvironmentBackgroundRandomizer

""" 

import bpy
import os
import sys
from glob import glob
import random
import math
from mathutils import Euler

class EnvironmentBackgroundRandomizer:
    def __init__(self):
        self.asset_hdri_env_bg_folder_path = "C:/Users/user/Documents/project/UAVDet/Asset/hdri_env_bg"
        self.hdri_env_bg_strength_range = {"min": 0.5 , "max": 1.5}

    def __error_check(self,img_path_list):
        """
        """
        num_img_in_folder = len(img_path_list)
        if num_img_in_folder < 1:
            print(f'ERROR!!! can not find any image in {self.asset_hdri_env_bg_folder_path}')
            input("Press Enter to continue...")
            sys.exit()

    def __create_world_shader_nodes(self):
        """ Create world shader nodes
        """ 
        ## Use Nodes
        bpy.data.worlds['World'].use_nodes = True

        ## environment node tree reference
        nodes = bpy.data.worlds['World'].node_tree.nodes

        ## clear all nodes
        nodes.clear()

        ## add new nodes(Lighting)
        node_TextureCoordinate = nodes.new("ShaderNodeTexCoord")
        node_Mapping = nodes.new("ShaderNodeMapping")
        node_EnvironmentTexture = nodes.new("ShaderNodeTexEnvironment")
        node_Background = nodes.new("ShaderNodeBackground")
        node_WorldOutput = nodes.new("ShaderNodeOutputWorld")
        ## locate nodes
        node_WorldOutput.location = (100, 300)
        node_Background.location = (-100, 300)
        node_EnvironmentTexture.location = (-400, 300)
        node_Mapping.location = (-650, 300)
        node_TextureCoordinate.location = (-900, 300)

        ## link nodes
        links = bpy.data.worlds['World'].node_tree.links
        links.new(node_TextureCoordinate.outputs["Generated"], node_Mapping.inputs["Vector"])
        links.new(node_Mapping.outputs["Vector"], node_EnvironmentTexture.inputs["Vector"])
        links.new(node_EnvironmentTexture.outputs["Color"], node_Background.inputs["Color"])
        links.new(node_Background.outputs["Background"], node_WorldOutput.inputs["Surface"])

    def env_bg_randomize(self):
        """ 
        """ 
        self.__create_world_shader_nodes()
       ## Background node reference
        node_Background = bpy.data.worlds['World'].node_tree.nodes["Background"]
        ## EnvironmentTexture node reference
        node_EnvironmentTexture = bpy.data.worlds['World'].node_tree.nodes["Environment Texture"]
        ## Mapping node reference
        node_Mapping = bpy.data.worlds["World"].node_tree.nodes["Mapping"]

        ## get hdri environment background asset path
        hdri_env_bg_path_list = glob(os.path.join(self.asset_hdri_env_bg_folder_path, "*.jpg"))
        self.__error_check(img_path_list = hdri_env_bg_path_list)

        ## randomly select a hdri environment background, then add hdri_env_bg to node_EnvironmentTexture
        hdri_env_bg_selected = random.sample(hdri_env_bg_path_list, 1)
        hdri_env_bg = bpy.data.images.load(hdri_env_bg_selected[0])
        node_EnvironmentTexture.image = hdri_env_bg

        ## randomly set hdri_env_bg_strength
        hdri_env_bg_strength_max = int(self.hdri_env_bg_strength_range["max"] * 10)
        hdri_env_bg_strength_min = int(self.hdri_env_bg_strength_range["min"] * 10)
        hdri_env_bg_strength = random.randrange(hdri_env_bg_strength_min, hdri_env_bg_strength_max,1)/10
        node_Background.inputs["Strength"].default_value = hdri_env_bg_strength

        ## randomly rotate hdri_env_bg
        random_rot = random.random() * 2 * math.pi
        node_Mapping.inputs["Rotation"].default_value[2] =  random_rot

        print("Environment Background Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = EnvironmentBackgroundRandomizer()
    randomizer.env_bg_randomize()


