from tkinter import *
from PIL import ImageTk,Image  
import os
import json
import math
import exifread
from pyproj import Proj

# cd to Current Directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# User Input Variables
obj_size = 100 # Approximate Size of Objects (in Pixels)
img_types = (".jpg", ".png") # Allowed Image Types (Raw)

# List of Acceptable Entries (Update From Interop)
obj_orient_list = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
obj_shape_list = sorted(("RECTANGLE", "SQUARE", "CROSS", "STAR", "CIRCLE", "SEMI-CIRCLE", "PENTAGON", "HEXAGON", "OCTAGON", "TRAPEZOID", "TRIANGLE"))
obj_color_list = sorted(("RED", "GREEN", "BLUE", "BROWN", "BLACK", "YELLOW", "ORANGE", "GRAY", "PURPLE", "WHITE"))
obj_alpha_color_list = obj_color_list

# Ask for Misison ID
mission_id = int(input("What is the Mission ID: "))

# ------------------------------------------------------------------------------------------------------------------

def next_img(): # Next Image (UI)
    global img_idx, img_ui, img_comp_ui
    
    img_idx += 1
    
    # Display New Image and Compass
    img_ui = ImageTk.PhotoImage(imgs_scale[img_idx])
    label_img.config(image=img_ui)
    
    img_comp_ui = ImageTk.PhotoImage(imgs_comp[img_idx])
    label_comp.config(image=img_comp_ui)
    
    # Allocate Button State Based on Current Image
    if img_idx == len(imgs)-1:
        next_btn["state"] = DISABLED
    else:
        next_btn["state"] = NORMAL
        
    prev_btn["state"] = NORMAL
        
def prev_img(): # Previous Image (UI)
    global img_idx, img_ui, img_comp_ui
    
    img_idx -= 1
    
    # DIsplay New Image and Compass
    img_ui = ImageTk.PhotoImage(imgs_scale[img_idx])
    label_img.config(image=img_ui)
    
    img_comp_ui = ImageTk.PhotoImage(imgs_comp[img_idx])
    label_comp.config(image=img_comp_ui)
    
    # Allocate Button State Based on Current Image
    if img_idx == 0:
        prev_btn["state"] = DISABLED    
    else:
        prev_btn["state"] = NORMAL
    
    next_btn["state"] = NORMAL

def dropdown(dropdown_list, frame, desc): # Create Dropdown Box
    dropdown_var = StringVar(ui)
    dropdown_var.set(dropdown_list[0]) # Default Value
    
    dropdown = OptionMenu(frame, dropdown_var, *dropdown_list)
    dropdown.config(width=10)
    
    dropdown_label = Label(frame, text = desc)
    
    obj_dict = {"list": dropdown_list, "var": dropdown_var, "dropdown": dropdown, "label": dropdown_label}

    return obj_dict

def double_click(click):
    global click_x, click_y

    click_x, click_y = click.x, click.y
    
    zoom_img(True) # Required for Zoom Method

def load_imgs(): # Load All Images

    # Load and Scale Compass Image
    img_comp = Image.open(path_comp)
    comp_size = int(display_height/5)
    img_comp_scale = img_comp.resize((comp_size, comp_size))
    
    # Load Raw Images and Metadata
    for file in os.listdir(path_raw):
        file_path = os.path.join(path_raw, file) 
        file_name, file_ext = os.path.splitext(file_path)
                
        # Ignore Non-Image Files
        if file_ext in img_types:
            img = Image.open(file_path)
            imgs.append(img)
   
        # Read Image Metadata
        craft_heading = 43

        # Rotate and Pair Compass Image to Each Raw Image
        img_comp_rot = img_comp_scale.rotate(-craft_heading, expand = True)
        imgs_comp.append(img_comp_rot)
           
    return imgs, imgs_comp

def save_data(): # Save JSON and Cropped Images
    global crop_idx
    
    # Set File Name and Save Cropped Image as PNG
    img_ext = "png"
    img_name = str(path_crops) + str(crop_idx) + "." + img_ext
    img_zoom.save(img_name, img_ext)

    # Localize Object
    obj_lat, obj_long = obj_loc(img_cent_x, img_cent_y)
    
    # Create JSON for Classifier
    json_name = str(path_crops) + str(crop_idx) + ".json"
    file = open(json_name,'w+')
        
    # Format JSON Data into Dictionary
    json_new = {
            "mission": mission_id,
            "type": "STANDARD", 
            "latitude": obj_lat, 
            "longitude": obj_long, 
            "orientation": obj_orient["var"].get(),
            "shape": obj_shape["var"].get(), 
            "shapeColor": obj_color["var"].get(), 
            "alphanumeric": (obj_alpha["entry"].get()).upper(), 
            "alphanumericColor": obj_alpha_color["var"].get()}
    
    # Convert to and Save as JSON
    json_new = json.dumps(json_new)
    file.write(json_new)
    file.close()
    
    crop_idx += 1 # Iterate Crop Count
    
    reset() # Reset Image View

def zoom_img(on_click): # Zoom on Images
    global img_zoom, img_zoom_ui, img_cent_x, img_cent_y
    
    # Load Images and Respective Sizes
    img_full = imgs_full[img_idx]
    img_scale = imgs_scale[img_idx]
    img_full_width, img_full_height = img_full.size
    img_scale_width, img_scale_height = img_scale.size
    img_zoom_width, img_zoom_height = img_zoom.size
    
    zoom_val = zoom_scl.get() # Get Zoom Slider Value
    
    img_marg = (obj_size)/zoom_val # Bounds (in Pixels) Adjusted for Zoom
        
    # Calculate Image Position from Mouse Click
    img_full_scale_ratio = img_full_height/img_scale_height

    if img_zoom_width != img_zoom_height and on_click == True:     
        img_cent_x, img_cent_y = click_x*img_full_scale_ratio, click_y*img_full_scale_ratio
    elif on_click == True:
        img_cent_x += (((click_x/img_zoom_width)-0.5)*2*img_marg)
        img_cent_y += (((click_y/img_zoom_height)-0.5)*2*img_marg)
        
    # Modify if Object Proximity to Boundary Causes Issues    
    img_cent_x = min((max(img_marg, img_cent_x)),(img_full_width-img_marg))
    img_cent_y = min((max(img_marg, img_cent_y)),(img_full_height-img_marg))
    
    # Set Bounds Around Center of Object
    img_left = img_cent_x - img_marg
    img_right = img_cent_x + img_marg
    img_upper = img_cent_y - img_marg
    img_lower = img_cent_y + img_marg
        
    # Create New Zoomed Image
    img_zoom = img_full.crop([img_left, img_upper, img_right, img_lower]) # Crop Based on Bounds
    img_zoom = img_zoom.resize((img_scale_height, img_scale_height)) # Resize to Square (UI)
    
    # Display Zoomed Image on GUI
    img_zoom_ui = ImageTk.PhotoImage(img_zoom)
    label_img.config(image=img_zoom_ui)
    
def reset(): # Reset Zoom on Image    
    global img_ui, img_zoom
    
    # Display Current Image (Zoomed Out)
    img_zoom = imgs_scale[img_idx]
    img_ui = ImageTk.PhotoImage(img_zoom)
    label_img.config(image=img_ui)

def obj_loc(img_cent_x, img_cent_y): # Localize Objects

    # Initialize Camera Variables (Manual)
    cam_fov_hor = 69.98 # Degrees
    cam_fov_hor = math.radians(cam_fov_hor) # Radians

    # Get Aircraft Data
    craft_lat = 37.1970694
    craft_lon = -80.5781355
    craft_alt = 70.3 # Meters
    craft_comp = (360-44.5)
    craft_comp = math.radians(-craft_comp) # Convert to Radians and Negate

    # Convert Craft UTM Position to XY Position
    utm_zone = math.floor((craft_lon + 180)/6) + 1
    utm_xy_conv = Proj(proj='utm',zone=utm_zone, ellps='WGS84')
    craft_x, craft_y = utm_xy_conv(craft_lon, craft_lat)

    # Calculate Ground Sampling Distance (m/pix)
    img_width_meter = craft_alt*2*math.tan(cam_fov_hor/2)

    img_full = imgs_full[img_idx]
    img_full_width, img_full_height = img_full.size

    img_gsd = img_width_meter/img_full_width

    # Calculate Distance Between Object and Image Center
    obj_dist_x = (img_cent_x - img_full_width/2)*img_gsd
    obj_dist_y = -(img_cent_y - img_full_height/2)*img_gsd

    obj_dist_E = math.cos(craft_comp)*obj_dist_x - math.sin(craft_comp)*obj_dist_y
    obj_dist_N = math.sin(craft_comp)*obj_dist_x + math.cos(craft_comp)*obj_dist_y

    # Calculate Position of Object
    obj_x, obj_y = (craft_x + obj_dist_E), (craft_y + obj_dist_N)
    obj_lon, obj_lat = utm_xy_conv(obj_x, obj_y, inverse=True)

    return obj_lat, obj_lon

# ------------------------------------------------------------------------------------------------------------------

# Initialize Variables
obj_alpha = {}
imgs = []
imgs_full = []
imgs_scale = []
imgs_comp = []
img_idx = 0
img_cent_x = img_cent_y = 0
crop_idx = 1

# Load Files and Setup Directories
path_raw = "/Raw_Images/"
path_crops = "/Cropped_Images/"
path_comp = "/compass.png"

path_raw = os.getcwd() + path_raw
path_crops = os.getcwd() + path_crops
path_comp = os.getcwd() + path_comp

# Get Number of Previous Crops or Create Folder if Non-Existent
if not os.path.isdir(path_crops):
    os.mkdir(path_crops)
else:
    for file in os.listdir(path_crops):
        crop_num = int(file.partition('.')[0])
        if crop_num >= crop_idx: # Only Increases
            crop_idx = crop_num + 1

# Initialize UI   
ui = Tk()
ui.title("AAV Image Classifier")
ui.resizable(0, 0) # Lock UI Size

# Get Display Size Info (UI Scaling)
display_height = int(ui.winfo_screenheight())
display_width = int(ui.winfo_screenwidth())

# Load Images
imgs, imgs_comp = load_imgs()

# Create Frames (Image, Entry Elements, Buttons) and Open UI
frame_ui = Frame(ui) # Image Frame
frame_buttons = Frame(ui) # Button Frame
frame_zoom = Frame(ui) # Zoom Frame
frame_object = Frame(ui) # Object Frame

frame_ui.grid() # Open UI

# Create List of Images
for idx, img in enumerate(imgs):
    # Resize Image for UI Display (Controls Overall Window Size)
    img_width, img_height = img.size
    ui_img_height = int(display_height*.7)
    ui_img_width = int(ui_img_height*(img_width/img_height))
    
    img_scale = img.resize((ui_img_width, ui_img_height))
    img_zoom = img_scale # Zoom and Scale Image Equal on Initial Boot
    
    # Append to List of Running Images
    imgs_scale.append(img_scale)
    imgs_full.append(img)
 
# ------------------------------------------------------------------------------------------------------------------

# Create Buttons and Sliders
btn_width = int(display_width/100) # Button Width
zoom_scl = Scale(frame_zoom, from_ = 1, to = 10, orient = "vertical", digits = 3, resolution = 0.5, length = ui_img_height, command = zoom_img)
save_btn = Button(ui, text = "Save Data", width = btn_width, command = save_data)
next_btn = Button(frame_buttons, text = "Next", width = btn_width, command = next_img)
prev_btn = Button(frame_buttons, text = "Previous", width = btn_width, command = prev_img)
reset_btn = Button(ui, text = "Reset Zoom", width = btn_width, command = reset)
prev_btn["state"] = DISABLED # Previous Button Disabled On First Picture

# Create Entry Elements
obj_orient = dropdown(obj_orient_list, frame_object, "Orientation:")
obj_shape = dropdown(obj_shape_list, frame_object, "Shape:")
obj_color = dropdown(obj_color_list, frame_object, "Shape Color:")
obj_alpha_color = dropdown(obj_alpha_color_list, frame_object, "Alpha Color:")
obj_alpha["entry"] = Entry(frame_object, width = int(btn_width*1.1))
obj_alpha["label"] = Label(frame_object, text = "Alphanumeric:")

# ------------------------------------------------------------------------------------------------------------------

# Grid Alignment of Buttons
obj_spc_x = btn_width # Horizontal Spacing
prev_btn.grid(row=0, column=0, padx = obj_spc_x)
next_btn.grid(row=0, column=1, padx = obj_spc_x)
save_btn.grid(row=2, column=2)
zoom_scl.grid(row=0, column=0, padx = obj_spc_x)
reset_btn.grid(row=2, column=0, padx = obj_spc_x)

# Grid Allignment of Characteristic Entries and Labels
obj_spc_y = obj_spc_x # Vertical Spacing

obj_orient["label"].grid(row=1, column=0)
obj_shape["label"].grid(row=2, column=0)
obj_color["label"].grid(row=3, column=0)
obj_alpha_color["label"].grid(row=4, column=0)
obj_alpha["label"].grid(row=5, column=0)

obj_orient["dropdown"].grid(row=1, column=1, pady = obj_spc_y)
obj_shape["dropdown"].grid(row=2, column=1, pady = obj_spc_y)
obj_color["dropdown"].grid(row=3, column=1, pady = obj_spc_y)
obj_alpha_color["dropdown"].grid(row=4, column=1, pady = obj_spc_y)
obj_alpha["entry"].grid(row=5, column=1, pady = obj_spc_y)

# Display Image and Frames
img_ui = ImageTk.PhotoImage(imgs_scale[img_idx])
label_img = Label(ui, image=img_ui)
label_img.grid(row=0, column=1, rowspan=2)

img_comp_ui = ImageTk.PhotoImage(imgs_comp[img_idx])   
label_comp = Label(ui, image=img_comp_ui)
label_comp.grid(row = 0, column = 2)

frame_zoom.grid(row=0, column=0, rowspan=2, padx = obj_spc_x, sticky = "n") # Display Zoom Frame
frame_object.grid(row=1, column=2, padx = 2*obj_spc_x, sticky = "s") # Publish Object Frame
frame_buttons.grid(row=2, column=1, pady = obj_spc_y, sticky = "n") # Display Buttons Frame

# Get Position of Double Click on Image Only
label_img.bind('<Double-1>', double_click)

# ------------------------------------------------------------------------------------------------------------------

ui.mainloop() # Run UI in Loop (Updates on Butotn Presses, Text Entries, etc.)
