#!/usr/bin/env python
"""
general idea: two folders - /Visualisation
                            /JsonExtraction

The Visualisation folder shows the generated baselines etc. with streamlit
The JsonExtraction uses the shared-file-format to create json's based on those images

I know that the folder watcher implemented with watchdog.event_handler would have been a better solutions.
Sadly streamlit together with the multiprocessing of watchdog events led to unexpected concurrency issues.
It's likely that there is a fix for this behaviour, but it didn't seem like worth the effort, because this approach
can still be used by the pure json encoding folder watcher :)
"""
import os
import time

import matplotlib
import streamlit
from mmdet.apis import init_detector, inference_detector, show_result_pyplot

SCRIPTS_LOCATION: str = "/home/makn/workspace-uni/CascadeTabNetTests"
FILE_LOCATION: str = SCRIPTS_LOCATION + "/files"
CASCADE_TAB_NET_REPO_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet"

VISUALISATION_LOCATION: str = FILE_LOCATION + "/Visualisation"

VISUALISATION_LOCATION_DETECTED = FILE_LOCATION + "/VisualisationDetected"


def move_to_extracted(filepath: str):
    if not os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(filepath))):
        os.rename(filepath, os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(filepath)))
    else:
        handle_duplicate_files(filepath)


def handle_duplicate_files(filepath: str):
    counter: int = 1
    filename, file_extension = os.path.splitext(os.path.basename(filepath))
    while os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED,
                                      filename + " (" + str(counter) + ")" + file_extension)):
        counter += 1
    os.rename(filepath,
              os.path.join(VISUALISATION_LOCATION_DETECTED, filename + " (" + str(counter) + ")" + file_extension))


def run_detection(image_path: str):
    # Load model
    config_file = CASCADE_TAB_NET_REPO_LOCATION + "/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
    checkpoint_file = SCRIPTS_LOCATION + "/epoch_36.pth"
    model = init_detector(config_file, checkpoint_file, device="cuda:0")

    # Run Inference
    result = inference_detector(model, image_path)

    # Visualization results
    image: matplotlib.pyplot = show_result_pyplot(img=image_path, result=result,
                                                  class_names=("Bordered", "cell", "Borderless"),
                                                  score_thr=0.85)
    streamlit.pyplot(image)


def main():
    try:
        while True:
            for file in os.listdir(VISUALISATION_LOCATION):
                run_detection(VISUALISATION_LOCATION + "/" + file)
                move_to_extracted(VISUALISATION_LOCATION + "/" + file)
            time.sleep(2)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
