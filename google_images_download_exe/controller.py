#!/usr/bin/env python
# coding: utf-8

'''
Controller class creates main Tkinter window, inputs, labels, and binds commands and buttons
'''
from model import Model 
from view import View 
from tkinter import *
from tkinter import ttk
import requests
import os
from google_images_download import google_images_download

class Controller():

    # substantiate Tk window with View class, and define all key frames
    def __init__(self):
        self.root = Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.search_frame = ttk.Frame(self.root, height = 10, padding="12 12 12 12")
        self.search_frame.pack(side = 'top', fill = 'x', expand=False)
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.pack(fill = 'both', expand=True)
        self.control_panel = ttk.Frame(self.mainframe, padding = 10, borderwidth = 2, relief = 'sunken')
        self.control_panel.pack(side = 'left', fill = 'y', expand=False)
        self.image_canvas = Canvas(self.mainframe, relief = 'sunken') # canvas required for scrolling
        self.gallery_scrollbar = ttk.Scrollbar(self.mainframe, orient=VERTICAL,
                                              command=self.image_canvas.yview)
        self.gallery_scrollbar.pack(side = 'right', fill = 'y', expand=False)
        self.image_canvas.pack(side = 'right', fill = 'both', expand=True)
        
        self.model = Model()
        self.model.args_list = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords", "limit", "format",
                                "color", "color_type", "usage_rights", "size", "exact_size", "aspect_ratio", "type", "time", "time_range", 
                                "delay", "url", "single_image", "output_directory", "image_directory", "no_directory", "proxy", 
                                "similar_images", "specific_site", "print_urls", "print_size", "print_paths", "metadata", "extract_metadata",
                                "socket_timeout", "thumbnail", "thumbnail_only", "language", "prefix", "chromedriver", "related_images", 
                                "safe_search", "no_numbering", "offset", "no_download", "save_source", "silent_mode", "ignore_urls"]
        self.model.initialise_arguments(self.model.arguments, self.model.args_list)
        self.model.set_defaults(self.model.arguments)
        self.view = View(self.image_canvas, self.root, self.model.arguments['output_directory'], self.gallery_scrollbar)
        self.keyword_list = []
        self.input_library = {} # keys matching arguments, include label and entry widgets
        self.colours = ['none', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown']
        self.colour_types = ['none', 'full-color', 'black-and-white', 'transparent']
        # for when multiple keywords accepted, currently disabled
#         self.keyword_list = [keyword.strip() for keyword in self.model.arguments["keywords"].split(",")]

    # generate labels and position
    def create_labels(self, mainframe, label_list = ['Unlabelled']):
        row_index = 1
#         self.labels = [None]*len(label_list)
        for key in label_list:
            self.input_library[key] = {}
            cleaned_label = key.replace('_', ' ')
            cleaned_label = cleaned_label[0].upper() + cleaned_label[1:]
            
            if 'keyword' in key: # position keyword label on self.search_frame
                self.input_library[key]['label_widget'] = ttk.Label(self.search_frame, text = cleaned_label)
                self.input_library[key]['label_widget'].pack(side = 'left', fill = 'x', expand=False)
            else:
                self.input_library[key]['label_widget'] = ttk.Label(mainframe, text = cleaned_label)
                self.input_library[key]['label_widget'].grid(column = 1, row = row_index, sticky=W)
                
            # create extra row for directory inputs
            if 'directory' in key:
                self.input_library[key]['label_widget'].grid(columnspan = 3)
                row_index += 2
            elif 'keyword' in key: pass
            else: row_index += 1

        # blank line before status
        row_index += 1
        ttk.Label(mainframe, text = '_____________________').grid(column = 1, row = row_index, sticky=W)

        # status
        row_index += 1
        self.input_library['readout'] = {}
        self.input_library['readout']['variable'] = StringVar(value = 'Ready')
        self.input_library['readout']['label_widget'] = ttk.Label(
            mainframe, textvariable = self.input_library['readout']['variable'])
        self.input_library['readout']['label_widget'].grid(column = 1, row = row_index, sticky=W)
        
    # generate entry widgets and position
    def create_inputs(self, mainframe, input_list = ['Inputs not defined']):
        row_index = 1
        for key in input_list:
            if 'keyword' in key: # special settings for input 0
                self.input_library[key]['variable'] = StringVar(value = str(self.model.arguments[key]))
                self.input_library[key]['widget'] = ttk.Entry(self.search_frame, width=7, # attach to search_frame
                                                          textvariable = self.input_library[key]['variable'])
                self.input_library[key]['widget'].pack(side = 'left', fill = 'x', expand=True)
                self.input_library[key]['widget'].bind('<Return>', self.search)
            else:
                self.input_library[key]['variable'] = StringVar(value = str(self.model.arguments[key]))
                self.input_library[key]['widget'] = ttk.Entry(mainframe, width=7,
                                                              textvariable = self.input_library[key]['variable'])
                self.input_library[key]['widget'].grid(column=2, row = row_index, sticky=(W, E))
          
            
            # special settings for columnspan
            if 'directory' in key: # create extra space for directory inputs
                row_index += 1
                self.input_library[key]['widget'].grid(column=1, columnspan=3, row = row_index, sticky=(W, E))
            elif 'keyword' in key: row_index -= 1
            else: self.input_library[key]['widget'].grid(columnspan=2)
        
            # add limit slider
            if 'limit' in key:
                row_index += 1 # put slider on new row
                self.input_library[key]['int_variable'] = IntVar(value = int(self.model.arguments[key]))
                self.input_library[key]['slider_widget'] = Scale(mainframe, variable = self.input_library[key]['variable'],
                                                                 orient=HORIZONTAL, length=20, from_=1, to=100)
                self.input_library[key]['slider_widget'].grid(column=1, columnspan=3, row = row_index, sticky=(W, E))
            
            if 'color' in key:
                if key == 'color': self.input_library[key]['variable'] = StringVar(value = self.colours)
                elif key == 'color_type': self.input_library[key]['variable'] = StringVar(value = self.colour_types)
                
                self.input_library[key]['widget'] = Listbox(mainframe, height=3, width=7, exportselection = False, listvariable = self.input_library[key]['variable'])
                self.input_library[key]['widget'].grid(column=2, row = row_index, sticky=(W, E))
                self.input_library[key]['scrollbar'] = ttk.Scrollbar(mainframe, orient=VERTICAL,
                                                                     command=self.input_library[key]['widget'].yview)
                self.input_library[key]['scrollbar'].grid(column=3, row = row_index, sticky=(N,S))
                self.input_library[key]['widget']['yscrollcommand'] = self.input_library[key]['scrollbar'].set
            
            row_index += 1
    
    def create_buttons(self, mainframe):
        buttons_commands = [("Download all", self.download_all), ("Search", self.search),
         ("Load thumbnails", self.existing_thumbnails), ("Read inputs", self.read_inputs)]
        self.buttons = []
        row_index = 30

        for text, function in buttons_commands:
            self.buttons.append(ttk.Button(mainframe, text = text))
            self.buttons[-1].bind('<1>', function) # using binding allows for event argument
            self.buttons[-1].grid(column=1, row = row_index, sticky=(W, E))
            row_index -= 1
        
    # Input list of widgets, bind each to events in place
    def bind_controls(self, image_library, command_list = []):
        for dictionary in image_library.values():
            if 'widget' in dictionary.keys(): dictionary['widget'].bind('<1>', self.download_image)
            else: pass
        else: return True

    # calling argument event allows configuration of associated widget and download from url
    # takes paths from model and image_library keys from view
    def download_image(self, event):
        search_string, filename, image_url, index = '', '', '', 8008
        
        # search image_library for widget to extract relevant key
        for key in self.view.image_library: 
            if event.widget in self.view.image_library[key].values():
                filename = key
                break
        else:
            self.input_library['readout']['variable'].set(value='Error: No widget found')
            return False

        # search for key inside paths. May be vulnerable to duplcicates
        for path_key, url in ((path_key, url) for path_key in self.model.paths for url in self.model.paths[path_key]):
            if filename in url:
                search_string, image_url, index = path_key, url, event.widget['text']
                self.input_library['readout']['variable'].set(value='Downloading...')
                if self.download_single_image(search_string, filename, image_url, index):
                    self.input_library['readout']['variable'].set(value='Downloaded :)')
                    return True
                else: 
                    self.input_library['readout']['variable'].set(value='Error: Download failed')
                    return False
        if not image_url:
            self.input_library['readout']['variable'].set(value='Error: No url found')
            return False
        
    # read all varaibles holder from entry widgets and return dictionary of arguments
    def read_inputs(self, event):
        arguments = {}
        for key in self.input_library:
            read_input = self.input_library[key]['variable'].get()
            if 'keywords' in key:
                arguments[key] = " ".join(read_input.translate(str.maketrans('', '', ".,")).split())
                self.input_library[key]['variable'].set(arguments[key])
            elif 'color' in key:
                list_indicies = self.input_library[key]['widget'].curselection()
                
                # capture multi-inputs
                if len(list_indicies) > 1:
                    self.input_library['readout']['variable'].set(value='Too many colour inputs')
                    continue

                if key == 'color': arguments[key] = self.colours[int(list_indicies[0])]
                elif key == 'color_type': arguments[key] = self.colour_types[int(list_indicies[0])]
            
            else: arguments[key] = read_input

            # capture none inputs
            if read_input.lower() == 'none' or arguments[key].lower() == 'none': arguments[key] = None
            
        print(arguments.items())
        return arguments

    # define search command
    def search(self, event):
        self.input_library['readout']['variable'].set(value='Searching...')
        self.root.update_idletasks()
        arguments = self.read_inputs(event)
        arguments['thumbnail_only'] = True
        try: self.model.download(arguments)
        except Exception as e:
            print(e)
            self.input_library['readout']['variable'].set(value='Search failed')
            return False
    
#           for multiple keyword - currently not implemented
#         self.keyword_list = [keyword.strip() for keyword in self.model.arguments["keywords"].split(",")]

        img_dir = self.find_image_subdirectory(arguments['output_directory'], arguments['keywords'], thumbnail = True)
        
        if img_dir:
            self.view.image_gallery.destroy()
            self.view = View(self.image_canvas, self.root, img_dir, self.gallery_scrollbar)
            self.input_library['readout']['variable'].set(value='Search complete :)')
        else: self.input_library['readout']['variable'].set(value='Search failed')
            
    def download_all(self, event):
        self.input_library['readout']['variable'].set(value='Downloading...')
        self.root.update_idletasks()
        arguments = self.read_inputs(event)
        try: self.model.download(arguments)
        except: 
            self.input_library['readout']['variable'].set(value='Download failed')
            return False
        
        if self.find_image_subdirectory(self.model.arguments['output_directory'], self.model.arguments['keywords']):
            self.input_library['readout']['variable'].set(value='Download complete :)')
        else: self.input_library['readout']['variable'].set(value='Download failed')

    def find_image_subdirectory(self, img_dir = None, keyword = None, thumbnail = False):
        if img_dir == None: img_dir = self.model.arguments['output_directory']
        if keyword == None: keyword = self.keyword_list[0]
        directory, subfolders, files = next(os.walk(img_dir))
        
        # add thumbnail constraint
        if thumbnail: thumbnail = 'thumbnail'
        else: thumbnail = ''
        for subfolder in subfolders:
#             print(directory+'\\'+subfolder)
            if keyword in subfolder and thumbnail in subfolder: return directory+'\\'+subfolder
        else: return False
    
    
    # load thumbnails from memory
    def existing_thumbnails(self, event):
        self.input_library['readout']['variable'].set(value='Loading...') # this isn't working
        arguments = self.read_inputs(event)
        arguments['thumbnail_only'] = True

        try: img_dir = self.find_image_subdirectory(arguments['output_directory'], arguments['keywords'], thumbnail = True)
        except: 
            return False
            self.input_library['readout']['variable'].set(value='Failed')

        if img_dir:
            self.view.image_gallery.destroy()
            self.view = View(self.image_canvas, self.root, img_dir, self.gallery_scrollbar)
            self.input_library['readout']['variable'].set(value='Loaded :)')
        else: self.input_library['readout']['variable'].set(value='Failed')

    
    # define function to download single image given key parameters
    def download_single_image(self, search_string, filename, image_url, index):
        try:
            r = requests.get(image_url, allow_redirects=True)
            image_type = r.headers['Content-Type'][6:]
            open(f'{search_string}_{index}.{image_type}', 'wb').write(r.content)
        except: return False
        else: return True

    def run(self):
        self.root.title("Semiotics engine")
        
         # inputs must match argument keywords
        input_list = ['keywords', 'specific_site', 'output_directory', 'limit']
        self.create_labels(self.control_panel, input_list)
        self.create_inputs(self.control_panel, input_list)
        self.create_buttons(self.control_panel)
        self.bind_controls(self.view.image_library)
        self.root.mainloop()

# # shortcut to add padding around all widgets, put focus on entry widget, and binds keyboard return key to search
# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
# keywords_entry.focus()
# root.bind('<Return>', search)


    