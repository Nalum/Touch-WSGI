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
        for folder in view.window().folders():
            filename = view.file_name()

            if filename is not None and filename.startswith(folder):
                self.get_folders(folder)

    def get_folders(self, path):
        regex = re.compile(r"^.*[\.]wsgi(\.py)?$")

        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if regex.match(filename):
                    os.utime(os.path.join(root, filename), None)
