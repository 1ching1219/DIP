from PIL import Image, ImageTk, ImageEnhance
import cv2
import tkinter as tk
import numpy as np
import imutils
from tkinter import filedialog
import matplotlib.pyplot as plt


def open_file():
	path_image = filedialog.askopenfilename(filetypes=[
			("image", ".jpg"), 
			("image", ".jpeg"), 
			("image", ".png"), 
			("image", ".tif"), ])
	if len(path_image) > 0:
		global image
		global gray_img
		global last
		global size_img
		image = cv2.imread(path_image)
		image = imutils.resize(image, height = 540)
		last = image
		size_img = last
		gray_img = last
		#show image
		imageToShow = imutils.resize(image, height=540)
		im = Image.fromarray(imageToShow)
		img = ImageTk.PhotoImage(image = im)
		image_place.configure(image=img)
		image_place.image = img

def save_as_jpg():
	im = Image.fromarray(last)
	im.save("saved.jpg", "jpeg")

def save_as_tif():
	im = Image.fromarray(last)
	im.save("saved.tiff", "tiff")

def get_current_brightness_value():
	return '{: .2f}'.format(brightness_value.get())

def get_current_contrast_value():
	return '{: 2f}'.format(contrast_value.get())

def get_current_size_value():
	return '{: 2f}'.format(size_value.get())

def brightness_change(event):
	global last
	global size_img
	global gray_img
	im = Image.fromarray(image)
	degree = float(get_current_brightness_value())/50
	adjust = ImageEnhance.Brightness(im).enhance(degree)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last


def contrast_change(event):
	global last
	global size_img
	global gray_img
	im = Image.fromarray(image)
	degree = float(get_current_contrast_value())/50
	adjust = ImageEnhance.Contrast(im).enhance(degree)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def size_change(event):
	global last
	global size_img
	global gray_img
	im = Image.fromarray(size_img)
	degree = float(get_current_size_value())/50
	adjust = im.resize((int(im.size[1]*degree), int(im.size[0]*degree)), Image.BILINEAR)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	gray_img = last
	
def rotate_change():
	global last
	global size_img
	global gray_img
	im = Image.fromarray(last)
	value = rotate_entry.get()
	adjust = im.rotate(float(value), Image.BILINEAR)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def showImage(title, img):
	ishow = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	plt.imshow(ishow)
	
	plt.title(title)
	plt.show()
	
def do_grayLevel(black):
	global last
	global size_img
	global gray_img
	slicing_img = np.zeros((gray_img.shape[0], gray_img.shape[1]), gray_img.dtype)
	min_ = int(gray_min_entry.get())
	max_ = int(gray_max_entry.get())
	for i in range(gray_img.shape[0]):
		for j in range(gray_img.shape[1]):
			if gray_img[i, j][0] >min_ and gray_img[i, j][0] < max_:
				slicing_img[i, j] = gray_img[i, j][0]
			else:
				if black: slicing_img[i, j] = 0#black
				else: slicing_img[i, j]=gray_img[i, j][0]#original
				
	adjust = Image.fromarray(slicing_img)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last

def do_grayLevel_old():
	global true_mask
	global r2
	r, c = gray_img.shape
	gray_value = gray_min_entry.get()
	#8 bit-planes mask
	x = np.zeros((r, c), dtype = np.uint8)
	print("s.ndim = ", x.ndim)
	#create 8 empty 8 bit-planes
	r = np.zeros((r, c, 8), dtype = np.uint8)
	for i in range(8):
		x=2**i
		r[:, :, i] = cv2.bitwise_and(gray_img, x)
		test_mask = gray_img < int(gray_value)
		mask = r[:, :, i]>0
		true_mask = r[:, :, i]<=0
		r2 = np.copy(gray_img)
		#(selceted range is input value~256)
		#display unselected area as black
		r2[test_mask] = 0
		
	showImage("Adjust", r2)

def linear_change():
	global last
	global size_img
	global gray_img
	a = float(self_define_a_entry.get())
	b = float(self_define_b_entry.get())
	new_image = np.zeros(image.shape, image.dtype)
	for y in range(image.shape[0]):
		for x in range(image.shape[1]):
			for c in range(image.shape[2]):
				new_image[y, x, c] = np.clip(a*image[y, x, c] + b, 0, 255)
	adjust = Image.fromarray(new_image)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def exp_change():
	global last
	global size_img
	global gray_img
	a = float(self_define_a_entry.get())
	b = float(self_define_b_entry.get())
	new_image = np.zeros(image.shape, image.dtype)
	for y in range(image.shape[0]):
		for x in range(image.shape[1]):
			for c in range(image.shape[2]):
				tmp = np.exp(float(a*image[y, x, c] + b))
				tmp = str(tmp)
				new_image[y, x, c] = np.clip(a*image[y, x, c] + b, 0, 255)
	adjust = Image.fromarray(new_image)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def log_change():
	global last
	global sizez_img
	global gray_img
	a = float(self_define_a_entry.get())
	b = float(self_define_b_entry.get())
	new_image = np.zeros(image.shape, image.dtype)
	for y in range(image.shape[0]):
		for x in range(image.shape[1]):
			for c in range(image.shape[2]):
				tmp = np.log(float(a*image[y, x, c] + b))
				tmp = str(tmp)
				new_image[y, x, c] = np.clip(a*image[y, x, c] + b, 0, 255)
	adjust = Image.fromarray(new_image)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def reset():
	adjust = Image.fromarray(image)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last
		

image = None

window = tk.Tk()
window.title('DIP Class HW1')

#place for image to show up
image_place = tk.Label(window, width=500)
image_place.grid(column=0, row=2)
image_place.place(relx = 1.0, rely = 0, anchor = 'ne')

# create btn to import pic
btn = tk.Button(window, text = 'Open File', width=18, command = open_file)
btn.grid(column = 0, row = 0, padx=5, pady =5)

#create btn to save pic in .jpg
sjpg_btn = tk.Button(window, text = 'Save as .jpg', width=7, command = save_as_jpg)
sjpg_btn.grid(column = 0, row = 1, padx=0, pady=0)
sjpg_btn.place(x=5, y=38)

#create btn to save pic in .tif
stif_btn = tk.Button(window, text = 'Save as .tif', width=7, command = save_as_tif)
stif_btn.grid(column = 1, row = 1, padx=0, pady=0)
stif_btn.place(x=94, y=38)

#create brightness toggle
brightness_lbl = tk.Label(window, text='Brightness')
brightness_lbl.place(x=5, y=90)
brightness_value = tk.DoubleVar()
brightness=tk.Scale(window, from_=100, to=0, orient='horizontal', width=18, command=brightness_change, variable=brightness_value)
brightness.place(x=75, y=70)
brightness.set(50)

#create contrast toggle
contrast_lbl = tk.Label(window, text='Contrast')
contrast_lbl.place(x=5, y=130)
contrast_value = tk.DoubleVar()
contrast = tk.Scale(window, from_=100, to=0, orient='horizontal', width=18, 
command=contrast_change, variable=contrast_value)
contrast.place(x=75, y=110)
contrast.set(50)

#create size toggle
size_lbl = tk.Label(window, text='Size')
size_lbl.place(x=5, y=170)
size_value = tk.DoubleVar()
size = tk.Scale(window, from_=100, to=0, orient='horizontal', width=18,
command=size_change, variable=size_value)
size.place(x=75, y=150)
size.set(50)

#create a line
horizontal = tk.Frame(window, bg='black', height=1,width=170)
horizontal.place(x=5, y=200)

#create self define contrast and brightness label
self_define_lbl = tk.Label(window, text='Self Define : ')
self_define_lbl.place(x=5, y=215)
self_define_a_lbl = tk.Label(window, text='a(Contrast)')
self_define_a_lbl.place(x=5, y=250)
self_define_a_entry = tk.Entry(window, width=10)
self_define_a_entry.place(x=91, y=250)
self_define_b_lbl = tk.Label(window, text='b(Brightness)')
self_define_b_lbl.place(x=5, y=280)
self_define_b_entry = tk.Entry(window, width=10)
self_define_b_entry.place(x=91, y=280)

#create btn to linear change
linear_btn = tk.Button(window, text = 'linear', width=3, command = linear_change)
linear_btn.grid(column = 0, row = 1, padx=0, pady=0)
linear_btn.place(x=5, y=320)

#create btn to exp change
exp_btn = tk.Button(window, text = 'exp', width=3, command = exp_change)
exp_btn.grid(column = 1, row = 1, padx=0, pady=0)
exp_btn.place(x=65, y=320)

#create btn to log change
log_btn = tk.Button(window, text = 'log', width=3, command = log_change)
log_btn.grid(column = 2, row = 1, padx=0, pady=0)
log_btn.place(x=125, y=320)

#create a line
horizontal = tk.Frame(window, bg='black', height=1,width=170)
horizontal.place(x=5, y=370)

#create rotate box
rotate_lbl=tk.Label(window, text='Rotate')
rotate_lbl.place(x=5, y=380)
rotate_entry = tk.Entry(window, width=12)
rotate_entry.place(x=76, y=380)
rotate_btn = tk.Button(window, text='Rotate it', width=18, command=rotate_change)
rotate_btn.place(x=5, y=405)

#create box to input gray-level
gray_lbl=tk.Label(window, text='Gray-level')
gray_lbl.place(x=5, y=444)
gray_lbl=tk.Label(window, text='~')
gray_lbl.place(x=119, y=444)
gray_min_entry = tk.Entry(window, width=5)
gray_min_entry.place(x=75, y=443)
gray_max_entry = tk.Entry(window, width=5)
gray_max_entry.place(x=131, y=443)

#create btn to show gray-level slicing
gray_btn = tk.Button(window, text = 'Show origin', width=7, command = lambda:do_grayLevel(0))
gray_btn.grid(column = 0, row = 1, padx=0, pady=0)
gray_btn.place(x=5, y=472)
gray_btn = tk.Button(window, text = 'Turn black', width=7, command = lambda:do_grayLevel(1))
gray_btn.grid(column = 1, row = 1, padx=0, pady=0)
gray_btn.place(x=94, y=472)

#create btn to reset all
reset_btn = tk.Button(window, text = 'Reset ALL', width=18, command=reset)
reset_btn.grid(column = 0, row = 0, padx=5, pady =5)
reset_btn.place(x=5, y=510)


window.geometry("740x540")
window.mainloop()
