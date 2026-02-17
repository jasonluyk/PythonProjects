from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import tkinter as tk
from tkinter import ttk
from os.path import join


def change_image(_):
    global image_tk
    #blur
    blur_image = image.filter(ImageFilter.BoxBlur(radius = blur_int.get()))
    #vibrance
    color_enhancer = ImageEnhance.Color(blur_image)
    new_image = color_enhancer.enhance(color_int.get())

    image_tk = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, image = image_tk, anchor = 'nw')

#create the window
window = tk.Tk()
window.geometry('640x400')
window.title('Image Editor')

#image import
image = Image.open(join('resources', 'images', 'raccoon.jpg'))
image_width, image_height = image.size
image = image.resize((image_width // 3, image_height // 3))
image_tk = ImageTk.PhotoImage(image)

#canvas
canvas = tk.Canvas(window, background = 'black', bd = 0, highlightthickness = 0, relief = 'ridge')
canvas.create_image(0, 0, image = image_tk, anchor = 'nw')
canvas.pack(expand = True, fill = 'both')

#sliders
blur_int = tk.IntVar(value = 0)
color_int = tk.IntVar(value = 0)
blur_slider = ttk.Scale(window, variable = blur_int, from_ = 0, to = 100, orient = 'horizontal', length = 400, command = change_image)
blur_slider.pack()

color_slider = ttk.Scale(window, variable = color_int, from_ = 0, to = 100, orient = 'horizontal', length = 400, command = change_image)
color_slider.pack()



window.mainloop()
