#!/usr/bin/env python
# coding: utf-8

'''
Created 28/07/2020 to create MVC style interface
'''
from google_images_download import google_images_download
import os

# Model calls google image downloader and stores image urls and paths to downloaded files
class Model():
    def __init__(self):
        self.arguments = {}
        self.args_list = []
        self.paths = {}
        
    def __str__(self):
        return f"{self.arguments}"
    
    def display(self):
        pass
    
    def initialise_arguments(self, arguments, args_list):
        # Add dictionary keys into Gallery
        for argument_name in args_list:
            arguments[argument_name] = None
        else: return True

    def check_corruption(self):
        # Clean out corrupted images - requires additional permissions / user install
        img_dir = self.arguments['output_directory']
        for directory, subfolders, files in os.walk(img_dir):
            if directory == '.': continue # skip main directory
            for filename in files:
                print(directory + "\\" + filename + " is ", end = '')
                try :
                    with Image.open(directory + "\\" + filename) as im: print('ok  \n')
                except :
                    print("corrupt \n")
#                     os.remove(directory + "\\" + filename) # delete corrupt files
        
    # set defaults for panda search and image download, output directory
    def set_defaults(self, arguments):
        
        # key user inputs
        arguments['keywords'] = 'panda'
        arguments['output_directory'] = os.path.join(os.path.dirname(os.getcwd()), 'Pictures')
        print(os.getcwd())
        print(arguments['output_directory'])
        arguments['limit'] = 5

        # functional inputs
        arguments['thumbnail_only'] = False
        
        # always off
        arguments['no_download'] = False
        arguments['print_paths'] = False
        arguments['print_size'] = False
        arguments['print_urls'] = False
        arguments['metadata'] = False
        # gallery_0.arguments['type'] = '' # Possible values: face, photo, clip-art, line-drawing, animated
        # gallery_0.arguments[''] = None
    
    # Take download with temporary parameters, saved to directory, return paths
    def download(self, temp_settings = {'thumbnail_only':True}):
        # extract arguments from defaults
        self.set_defaults(self.arguments)
        arguments = self.arguments
        # overwrite specific arguments from input settings
        for key, value in temp_settings.items(): 
            print(key, value)
            arguments[key] = value
        response = google_images_download.googleimagesdownload()   #class instantiation
        paths, errors = response.download(arguments)   # passing the arguments to the function
        return paths