#!/usr/bin/env python
"""
general idea: two folders - /Visualisation
                            /JsonExtraction

The Visualisation folder shows the generated baselines etc. with streamlit
The JsonExtraction uses the shared-file-format to create json's based on those images
"""
import logging
import os.path
import time

import streamlit
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

# todo extract these constants with argparse
SCRIPTS_LOCATION: str = "/home/makn/workspace-uni/CascadeTabNetTests"
FILE_LOCATION: str = SCRIPTS_LOCATION + "/CascadeTabNet/Demo"

VISUALISATION_LOCATION: str = FILE_LOCATION + "/Visualisation"

VISUALISATION_LOCATION_DETECTED = FILE_LOCATION + "/VisualisationExtracted"

text_to_display = "initial text to display"
changed: bool = False


def move_to_extracted(event: FileSystemEvent):
    if not os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(event.src_path))):
        os.rename(event.src_path, os.path.join(VISUALISATION_LOCATION_DETECTED, os.path.basename(event.src_path)))
    else:
        handle_duplicate_files(event)


def handle_duplicate_files(event: FileSystemEvent):
    counter: int = 1
    filename, file_extension = os.path.splitext(os.path.basename(event.src_path))
    while os.path.isfile(os.path.join(VISUALISATION_LOCATION_DETECTED,
                                      filename + " (" + str(counter) + ")" + file_extension)):
        counter += 1
    os.rename(event.src_path,
              os.path.join(VISUALISATION_LOCATION_DETECTED, filename + " (" + str(counter) + ")" + file_extension))


class DownloadedFileHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent):
        move_to_extracted(event)
        global changed, text_to_display
        changed = True
        text_to_display = "reached on created"


def main():
    logging.debug("reached main()")
    streamlit.text("first message")
    global changed, text_to_display
    try:
        while True:
            logging.debug(text_to_display)
            logging.debug("asdf")
            if changed:
                streamlit.text(text_to_display)
                changed = False
            time.sleep(2)
    except KeyboardInterrupt:
        observer.join()
        observer.stop()


# @streamlit.cache
# def install_monitor():
event_handler = DownloadedFileHandler()
observer = Observer()
observer.schedule(event_handler, VISUALISATION_LOCATION, recursive=True)
observer.start()

if __name__ == "__main__":
    main()
