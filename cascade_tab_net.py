# #!/usr/bin/env python
# """
# general idea: two folders - /Visualisation
#                             /JsonExtraction
#
# The Visualisation folder shows the generated baselines etc. with streamlit
# The JsonExtraction uses the shared-file-format to create json's based on those images
# """
# import os.path
# import time
#
# import streamlit
# from mmdet.apis import init_detector, inference_detector, show_result_pyplot
# from watchdog.events import FileSystemEventHandler, FileSystemEvent
# from watchdog.observers import Observer
#
# # todo extract these constants with argparse
# SCRIPTS_LOCATION: str = "/home/makn/workspace-uni/CascadeTabNetTests"
# FILE_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet/Demo"
# CASCADE_TAB_NET_REPO_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet"
#
# VISUALISATION_LOCATION: str = FILE_LOCATION + "/Visualisation"
# JSON_EXTRACTION_LOCATION: str = FILE_LOCATION + "/JsonExtraction"
#
# VISUALISATION_LOCATION_DETECTED = FILE_LOCATION + "/VisualisationDetected"
# JSON_EXTRACTION_LOCATION_DETECTED = FILE_LOCATION + "/JsonExtractionDetected"
#
#
# def create_extracted_dir():
#     if not os.path.exists(VISUALISATION_LOCATION_DETECTED):
#         os.makedirs(VISUALISATION_LOCATION_DETECTED)
#
#
# def move_to_extracted(event: FileSystemEvent):
#     if not os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(event.src_path))):
#         os.rename(event.src_path, os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(event.src_path)))
#     else:
#         handle_duplicate_files(event)
#
#
# def handle_duplicate_files(event: FileSystemEvent):
#     counter: int = 1
#     filename, file_extension = os.path.splitext(os.path.basename(event.src_path))
#     while os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED,
#                                       filename + " (" + str(counter) + ")" + file_extension)):
#         counter += 1
#     os.rename(event.src_path,
#               os.path.join(VISUALISATION_LOCATION_DETECTED, filename + " (" + str(counter) + ")" + file_extension))
#
#
# class DownloadedFileHandler(FileSystemEventHandler):
#     def on_created(self, event: FileSystemEvent):
#         absolute_path_from_event: str = os.path.abspath(event.src_path)
#         run_detection(absolute_path_from_event)
#         create_extracted_dir()
#
#         move_to_extracted(event)
#         # if any(event.src_path.endswith(x) for x in FILE_FOLDER_MAPPING):
#         #
#         #     # absolute path for the new folder
#         #     absolute_path_from_event = os.path.abspath(event.src_path)
#         #     # mapping for this file
#         #     file_folder_mapping_get = FILE_FOLDER_MAPPING.get(f".{event.src_path.split('.')[-1]}")
#         #     parent = os.path.join(os.path.dirname(absolute_path_from_event), file_folder_mapping_get)
#         #     if not os.path.exists(parent):
#         #         os.makedirs(parent)
#         #         sleep(_SLEEP_CHANGES)
#         #     os.rename(event.src_path, os.path.join(parent, os.path.basename(event.src_path)))
#         #     logger.info('moved ' + event.src_path + ' to ' + os.path.join(parent, os.path.basename(event.src_path)))
#         """
#         todo start detection
#         move to /VisualisationDetected
#         """
#
#
# def run_detection(image_path: str):
#     # Load model
#     config_file = CASCADE_TAB_NET_REPO_LOCATION + "/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
#     checkpoint_file = SCRIPTS_LOCATION + "/epoch_36.pth"
#     model = init_detector(config_file, checkpoint_file, device="cuda:0")
#
#     # Run Inference
#     result = inference_detector(model, image_path)
#
#     # Visualization results
#     image = show_result_pyplot(img=image_path, result=result, class_names=("Bordered", "cell", "Borderless"),
#                                score_thr=0.85)
#     streamlit.pyplot(image)
#
#
# def main():
#     try:
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         observer.stop()
#         observer.join()
#
#
# event_handler = DownloadedFileHandler()
# observer = Observer()
# observer.schedule(event_handler, VISUALISATION_LOCATION, recursive=True)
# observer.start()
#
# if __name__ == "__main__":
#     main()
