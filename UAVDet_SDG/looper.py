""" looper
"""

## prevent create __pycache__ file
import sys
sys.dont_write_bytecode = True

import subprocess
import os
from UAVDetSDG_020_UAVDetParameter import UAVdetParameter


for i in range(99999):

    ## get blender exe path
    uavdet_parameter = UAVdetParameter()
    blender_exe_path = uavdet_parameter.blender_exe_path

    ## get UAVDetSDG_090_DataGenerator.py path
    module_path = os.path.dirname(os.path.abspath(__file__))
    data_generator_path = os.path.join(module_path,"UAVDetSDG_090_DataGenerator.py")

    ## set args
    args = [
        blender_exe_path,
        "--python",
        data_generator_path
        ]

    ## create new process
    subprocess.run(args)

    print("ok") 
