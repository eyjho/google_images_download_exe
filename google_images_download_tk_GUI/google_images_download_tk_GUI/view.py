#!/usr/bin/env python
# coding: utf-8

'''
View class creates interactive Tkinter widget showing images
'''
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk
import os

class View():
    
    def __init__(self, canvas, root, img_dir, scrollbar, grid_dimensions = [7, 5]):
        self.canvas = canvas
        self.root = root
        self.image_gallery = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0,0), window = self.image_gallery, anchor='nw')

        self.image_gallery.bind("<Configure>", 
            lambda _: self.canvas.configure(scrollregion = canvas.bbox("all")))
        canvas.bind('<Configure>', self.FrameWidth)
        

        self.image_library = {}
        self.input_dict = {}
        self.display_images(self.image_gallery, img_dir, grid_dimensions)
        canvas['yscrollcommand'] = scrollbar.set
        canvas.configure(scrollregion=(0,0,3000,3000))

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        
    def import_images(self, directory, files, quantity = 9):
        output = {}
        for filename in files:
#             print('\n' + directory + "\\" + filename)
            try: thumbnail = PIL.Image.open(directory + "\\" + filename)
            except: continue
            scale = 150/max(thumbnail.size)
            new_size = tuple([round(scale*dimension-1) for dimension in thumbnail.size])
            output[filename] = dict({'thumbnail': ImageTk.PhotoImage(thumbnail.resize(new_size)), 'size': new_size})
        return output

    # in-place method toiteratively add image labels to buttons
    def display_images(self, mainframe, img_dir, grid_dimensions = [5, 4]):
        
        # clear frame
        try: directory, subfolders, files = next(os.walk(img_dir))
        except: return False
        # saved_images must be global variable otherwise all image data is lost when function ends
        self.image_library = self.import_images(directory, files)
        sorted_keys = sorted(self.image_library, key = lambda key: self.image_library[key]['size'][1])
        x, y = 1, 1

        for key in sorted_keys:
            self.image_library[key]['widget'] = ttk.Button(mainframe, text = f"{y}_{x}", 
                       image = self.image_library[key]['thumbnail'], compound = "bottom")
            self.image_library[key]['widget'].grid(column = x, row = y, sticky=N)
#             if y > grid_dimensions[1]: 
#                 return False # limited by grid
#                 break
            self.root.update_idletasks() 
            # print(self.canvas.winfo_width())
            # if x >= grid_dimensions[0]: x, y = 1, y + 1
            # elif x <= grid_dimensions[0]: x += 1
            if x*150+130 >= self.canvas.winfo_width(): x, y = 1, y + 1
            elif x*150+130 < self.canvas.winfo_width(): x += 1
            else:
                print("Index error")
                break
        else:
#             self.image_canvas['scrollregion'] = self.image_canvas.bbox("all")
            return True # shown all images
