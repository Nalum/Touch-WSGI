#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime_plugin
import os
import re


class TouchWSGI(sublime_plugin.EventListener):
    """
    Sublime Text Plugin to Touch WSGI Files.

    Scans any open folders in the current window when saving a file to see
    if there is a WSGI file in it. "WSGI file" == r"^.*[\.]wsgi(\.py)?$"
    """
    def on_post_save_async(self, view):
        #start_time = time.time()
        for folder in view.window().folders():
            # only check when saved file in project
            if view.file_name().startswith(folder):
                self.get_folders(folder)
        #print("* All checked")
        #print("--- %s seconds ---" % (time.time() - start_time))

    def get_folders(self, path):
        regex = re.compile(r"^.*\.wsgi(\.py)?$")
        for root, dirnames, filenames in os.walk(path):
            for file in filenames:
                if regex.match(file):
                    os.utime(os.path.join(root, file), None)
