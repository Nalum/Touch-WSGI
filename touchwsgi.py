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
    def on_post_save(self, view):
        window = view.window()
        for folder in window.folders():
            self.get_folders(folder)

    def check_files(self, path, files):
        regex = re.compile(r"^.*[\.]wsgi(\.py)?$")
        files = [filename for filename in files if regex.match(filename) is not None]

        if len(files) > 0:
            for filename in files:
                os.utime(path + '/' + filename, None)

    def get_folders(self, path):
        for root, dirnames, filenames in os.walk(path):
            if len(dirnames) > 0:
                for dirname in dirnames:
                    self.check_files(root, filenames)
                    filenames = []
                    new_path = os.path.join(root, dirname)
                    self.get_folders(new_path)
