# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
from glob import glob


class TouchWSGI(sublime_plugin.EventListener):
    """
    Sublime Text Plugin to Touch WSGI Files.

    Scans any open folders in the current window when saving a file to see
    if there is a WSGI file in it. "WSGI file" == *.wsgi or *wsgi.py
    """
    def on_post_save(self, view):
        print "Looking for WSGI Files."
        window = view.window()
        for folder in window.folders():
            self.check_folder(folder)
            # self.get_folders(folder)
        print "Done."

    def check_folder(self, path):
        wsgi_files = filter(os.path.isfile, glob(path + "/*.wsgi"))
        if len(wsgi_files) == 0:
            wsgi_files = filter(os.path.isfile, glob(path + "/*wsgi.py"))
        if len(wsgi_files) > 0:
            print "Found WSGI File(s) in " + path
            for wsgi_file in wsgi_files:
                os.utime(wsgi_file, None)

    def get_folders(self, path):
        for root, dirnames, filenames in os.walk(path):
            if len(dirnames) > 0:
                for dirname in dirnames:
                    new_path = os.path.join(root, dirname)
                    self.check_folder(new_path)
                    self.get_folders(new_path)
