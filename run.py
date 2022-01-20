#!/usr/bin/env python
"""
general idea: two folders - /Visualisation
                            /JsonExtraction

The Visualisation folder shows the generated baselines etc. with streamlit
The JsonExtraction uses the shared-file-format to create json's based on those images
"""

import streamlit
from mmdet.apis import init_detector, inference_detector, show_result_pyplot

SCRIPTS_LOCATION: str = "/home/makn/workspace-uni/CascadeTabNetTests"
CURRENT_LOCATION: str = SCRIPTS_LOCATION
FILE_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet/Demo"
CASCADE_TAB_NET_REPO_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet"

# Test a single image
img: str = FILE_LOCATION + "/demo.png"

# Load model
config_file = CASCADE_TAB_NET_REPO_LOCATION + "/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
checkpoint_file = CURRENT_LOCATION + "/epoch_36.pth"
model = init_detector(config_file, checkpoint_file, device="cuda:0")

# Run Inference
print("Run Inference")
result = inference_detector(model, img)

# Visualization results
print("Visualization results")
# show_result_pyplot(img, result, ("Bordered", "cell", "Borderless"), score_thr=0.85)
# image = show_result_pyplot(img=img, result=result, class_names=("Bordered", "cell", "Borderless"), score_thr=0.85)
# streamlit.pyplot(image)
streamlit.pyplot(
    show_result_pyplot(img=img, result=result, class_names=("Bordered", "cell", "Borderless"), score_thr=0.85))
