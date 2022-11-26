from PIL import Image, ImageTk, ImageEnhance, ImageChops
import cv2
import tkinter as tk
import numpy as np
import imutils
from tkinter import filedialog
import matplotlib.pyplot as plt
import glob

def open_file():
	global compare
	compare = 0
	path_image = filedialog.askopenfilename(filetypes=[
			("image", ".jpg"), 
			("image", ".jpeg"), 
			("image", ".png"), 
			("image", ".tif"),
			("image", ".tiff"), ])
	if len(path_image) > 0:
		image1_place.configure(image=None)
		image1_place.image = None
		image2_place.configure(image=None)
		image2_place.image = None
		image1_place.grid_forget()
		image1_place.pack_forget()
		image1_place.place_forget()
		image2_place.grid_forget()
		image2_place.pack_forget()
		image2_place.place_forget()
		open2btn.grid_forget()
		open2btn.pack_forget()
		open2btn.place_forget()
		
		global image
		global gray_img
		global bit_plane_img
		global last
		global size_img
		image = cv2.imread(path_image)
		image = imutils.resize(image, height = 750)
		bit_plane_img = cv2.imread(path_image, 0)
		last = image
		size_img = last
		gray_img = last
		#show image
		imageToShow = imutils.resize(image, height=750)
		im = Image.fromarray(imageToShow)
		img = ImageTk.PhotoImage(image = im)
		image_place.configure(image=img)
		image_place.image = img

def open_2_file(x):
	global compare
	compare=1
	check_same_type = 0
	path_images = filedialog.askopenfilenames(filetypes=[
			("image", ".jpg"), 
			("image", ".jpeg"), 
			("image", ".png"), 
			("image", ".tif"),
			("image", ".raw"),])
	images=[0,0]
	if len(path_images) > 1:
		image_place.configure(image=None)
		image_place.image = None
		image1_place.grid(column=0, row=2)
		image1_place.place(x=320, y=20)
		image2_place.grid(column=0, row=2)
		image2_place.place(x=320, y=390)
		for i in range(0,2):
			if '.raw' in path_images[i]:
				fd = open(path_images[i], 'rb')
				rows = 512
				cols = 512
				f = np.fromfile(fd, dtype=np.uint8,count=rows*cols)
				images[i] = f.reshape((rows, cols)) #notice row, column format
			else:
				images[i] = cv2.imread(path_images[i])
			images[i] = imutils.resize(images[i], height = 640)
			# show image
			imageToShow = imutils.resize(images[i], height=390)
			im = Image.fromarray(imageToShow)
			img = ImageTk.PhotoImage(image = im)
			if i == 0:
				image1_place.configure(image=img)
				image1_place.image = img
			else:
				image2_place.configure(image=img)
				image2_place.image = img
	#compare two imgs
	img1, img2 = Image.fromarray(images[0]), Image.fromarray(images[1])
	
	
	# hsv1 = cv2.cvtColor(images[0], cv2.COLOR_BGR2HSV)
	# hsv2 = cv2.cvtColor(images[1], cv2.COLOR_BGR2HSV)
	# h_bins = 50
	# s_bins = 60
	# histSize = [h_bins, s_bins]
	# h_ranges = [0, 180]
	# s_ranges = [0, 256]
	# ranges = h_ranges + s_ranges
	# channels = [0, 1]
	# hist1 = cv2.calcHist([hsv1], channels, None, histSize, ranges, accumulate=False)
	# cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
	# hist2 = cv2.calcHist([hsv2], channels, None, histSize, ranges, accumulate=False)
	# cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
	# compare_method = cv2.HISTCMP_CORREL
	# compare1_2 = cv2.compareHist(hist1, hist2, compare_method)
	# print('Similarity = ', compare1_2)
	#avg
	if x==1:
		kernel = np.ones((3,3),np.float32)/9
		dst1, dst2 = cv2.filter2D(images[0],-1,kernel), cv2.filter2D(images[1],-1,kernel)
		err = np.sum((dst1.astype("float") - dst2.astype("float")) ** 2)
		err /= float(dst1.shape[0] * dst2.shape[1])
		print('MSE :', err)
		dst1, dst2 = Image.fromarray(dst1), Image.fromarray(dst2)
		diff = ImageChops.difference(dst1, dst2)
		diff.show()
	#mid
	if x == 0:
		mid1, mid2 = cv2.medianBlur(images[0], 3), cv2.medianBlur(images[1], 3)
		err = np.sum((mid1.astype("float") - mid2.astype("float")) ** 2)
		err /= float(mid1.shape[0] * mid2.shape[1])
		print('MSE :',err)
		mid1, mid2 = Image.fromarray(mid1), Image.fromarray(mid2)
		diff = ImageChops.difference(mid1, mid2)
		diff.show()

def lapacian():
	image_place.configure(image=None)
	image_place.image = None
	image1_place.grid(column=0, row=2)
	image1_place.place(x=320, y=20)
	image2_place.grid(column=0, row=2)
	image2_place.place(x=320, y=390)

	# imageToShow = imutils.resize(image, height=350)
	# im = Image.fromarray(imageToShow)
	# img = ImageTk.PhotoImage(image = im)
	# image1_place.configure(image=img)
	# image1_place.image = img

	mid = cv2.medianBlur(image, 3)
	mid = imutils.resize(mid, height=390)
	tmp = mid
	mid = Image.fromarray(mid)
	mid = ImageTk.PhotoImage(image = mid)
	image1_place.configure(image=mid)
	image1_place.image = mid

	kernel = np.array([[1, 1, 1],
                   [1, -8, 1],
                   [1, 1, 1]])
	dst = cv2.filter2D(tmp,-1,kernel)
	dst = imutils.resize(dst, height=390)
	tmp1 = dst
	dst = Image.fromarray(dst)
	dst = ImageTk.PhotoImage(image = dst)
	image2_place.configure(image=dst)
	image2_place.image = dst

	mid, dst = cv2.medianBlur(tmp, 3), cv2.medianBlur(tmp1, 3)
	err = np.sum((mid.astype("float") - dst.astype("float")) ** 2)
	err /= float(mid.shape[0] * dst.shape[1])
	print('MSE :',err)
	mid, dst = Image.fromarray(mid), Image.fromarray(dst)
	diff = ImageChops.difference(mid, dst)
	diff.show()


def open2(x):
	open2btn.place(x=895, y=5)
	open2btn.config(command = lambda: open_2_file(x))

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

def ss_change(event):
	global last
	global size_img
	global gray_img
	degree = int(sscontrol_value.get())
	if degree <=50:degree = (degree-50)*-1
	dst = cv2.GaussianBlur(image, (0,0), degree)
	if degree > 50:dst = cv2.addWeighted(image, 1.5, dst, -0.5, 0)
	adjust = Image.fromarray(dst)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

# def spatial_smooth():
# 	global last
# 	global size_img
# 	global gray_img
# 	degree = int(spatial_smooth_entry.get())
# 	degree_ = degree*degree
# 	kernel = np.ones((degree, degree),np.float32)/degree_
# 	dst = cv2.filter2D(image,-1,kernel)
# 	adjust = Image.fromarray(dst)
# 	img = ImageTk.PhotoImage(image = adjust)
# 	image_place.configure(image=img)
# 	image_place.image = img
# 	last = np.array(adjust)
# 	size_img = last
# 	gray_img = last

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
	plt.axis('off')
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
				else: 
					# slicing_img[i, j]=gray_img[i, j][0]#original
					slicing_img=gray_img
	adjust = Image.fromarray(slicing_img)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last

def bit_plane():
	global true_mask
	global r2
	r, c = bit_plane_img.shape
	gray_value = 20
	#8 bit-planes mask
	x = np.zeros((r, c), dtype = np.uint8)
	print("s.ndim = ", x.ndim)
	#create 8 empty 8 bit-planes
	r = np.zeros((r, c, 8), dtype = np.uint8)
	# for i in range(8):
	i = int(btip_entry.get())
	x=2**i
	r[:, :, i] = cv2.bitwise_and(bit_plane_img, x)
	mask = r[:, :, i]>0
	r2 = np.copy(r)
	r2[mask] = 255
	showImage(str(i), r2[:, :, i])
	

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
	global size_img
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

def show_histogram():
	# if picture isn't gray
	# gray = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
	gray = last
	plt.hist(last.ravel(), 256, [0, 256])
	plt.show()

def auto_level():
	global last
	global size_img
	global gray_img
	gray = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	plt.hist(gray.ravel(), 256, [0, 256])
	gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
	adjust = Image.fromarray(gray)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last
	plt.show()

def reset():
	global last
	global size_img
	global gray_img
	adjust = Image.fromarray(image)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last
		

image = None
compare = 1

window = tk.Tk()
window.title('DIP Class HW1')

#place for image to show up
image_place = tk.Label(window, width=750)
image_place.grid(column=0, row=2)
image_place.place(relx = 1.0, rely = 0, anchor = 'ne')

#pace for two imgs to show up
image1_place = tk.Label(window, width=400)
image1_place.grid(column=0, row=2)
image1_place.place(x=320, y=20)
image2_place = tk.Label(window, width=400)
image2_place.grid(column=0, row=2)
image2_place.place(x=320, y=390)

open2btn = tk.Button(window, text = 'Open two Files', width=14)
open2btn.place(x=895, y=5)
open2btn.grid_forget()
open2btn.pack_forget()
open2btn.place_forget()


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

#create smooth/sharp toggle
sscontrol_lbl1 = tk.Label(window, text='smooth/')
sscontrol_lbl1.place(x=5, y=160)
sscontrol_lbl2 = tk.Label(window, text='sharp')
sscontrol_lbl2.place(x=5, y=180)
sscontrol_value = tk.DoubleVar()
sscontrol = tk.Scale(window, from_=100, to=0, orient='horizontal', width=18,
command=ss_change, variable=sscontrol_value)
sscontrol.place(x=75, y=150)
sscontrol.set(50)

#create size toggle
size_lbl = tk.Label(window, text='Size')
size_lbl.place(x=5, y=210)
size_value = tk.DoubleVar()
size = tk.Scale(window, from_=100, to=0, orient='horizontal', width=18,
command=size_change, variable=size_value)
size.place(x=75, y=190)
size.set(50)

#create a line
horizontal = tk.Frame(window, bg='black', height=1,width=170)
horizontal.place(x=5, y=240)

#create self define contrast and brightness label
self_define_lbl = tk.Label(window, text='Self Define : ')
self_define_lbl.place(x=5, y=255)
self_define_a_lbl = tk.Label(window, text='a(Contrast)')
self_define_a_lbl.place(x=5, y=290)
self_define_a_entry = tk.Entry(window, width=10)
self_define_a_entry.place(x=91, y=290)
self_define_b_lbl = tk.Label(window, text='b(Brightness)')
self_define_b_lbl.place(x=5, y=320)
self_define_b_entry = tk.Entry(window, width=10)
self_define_b_entry.place(x=91, y=320)

#create btn to linear change
linear_btn = tk.Button(window, text = 'linear', width=3, command = linear_change)
linear_btn.grid(column = 0, row = 1, padx=0, pady=0)
linear_btn.place(x=5, y=360)

#create btn to exp change
exp_btn = tk.Button(window, text = 'exp', width=3, command = exp_change)
exp_btn.grid(column = 1, row = 1, padx=0, pady=0)
exp_btn.place(x=65, y=360)

#create btn to log change
log_btn = tk.Button(window, text = 'log', width=3, command = log_change)
log_btn.grid(column = 2, row = 1, padx=0, pady=0)
log_btn.place(x=125, y=360)

#create a line
horizontal = tk.Frame(window, bg='black', height=1,width=170)
horizontal.place(x=5, y=405)

#create rotate box
rotate_lbl=tk.Label(window, text='Rotate')
rotate_lbl.place(x=5, y=420)
rotate_entry = tk.Entry(window, width=12)
rotate_entry.place(x=76, y=420)
rotate_btn = tk.Button(window, text='Rotate it', width=18, command=rotate_change)
rotate_btn.place(x=5, y=445)

#create box to input gray-level
gray_lbl=tk.Label(window, text='Gray-level')
gray_lbl.place(x=5, y=484)
gray_lbl=tk.Label(window, text='~')
gray_lbl.place(x=119, y=484)
gray_min_entry = tk.Entry(window, width=5)
gray_min_entry.place(x=75, y=483)
gray_max_entry = tk.Entry(window, width=5)
gray_max_entry.place(x=131, y=483)

#create btn to show gray-level slicing
gray_btn = tk.Button(window, text = 'Show origin', width=7, command = lambda:do_grayLevel(0))
gray_btn.grid(column = 0, row = 1, padx=0, pady=0)
gray_btn.place(x=5, y=512)
gray_btn = tk.Button(window, text = 'Turn black', width=7, command = lambda:do_grayLevel(1))
gray_btn.grid(column = 1, row = 1, padx=0, pady=0)
gray_btn.place(x=94, y=512)

#create btn to show bit plane
bitp_lbl = tk.Label(window, text='Bit-plane to show (0~7): ')
bitp_lbl.place(x=5, y=551)
btip_entry = tk.Entry(window, width=9)
btip_entry.place(x=5, y=576, height=25)
bitp_btn = tk.Button(window, text = 'Show', width=7, command=bit_plane)
bitp_btn.place(x=94, y=576)

#create btn to show histogram
histogram_btn = tk.Button(window, text='Histogram', width=7, command=show_histogram)
histogram_btn.grid(column = 0, row = 1, padx=0, pady=0)
histogram_btn.place(x=5, y=611)
#create btn to do auto-level
auto_level_btn = tk.Button(window, text='Auto', width=7, command=auto_level)
auto_level_btn.grid(column = 1, row = 1, padx=0, pady=0)
auto_level_btn.place(x=94, y=611)

#create btn to avg compare two img
compare_lbl = tk.Label(window, text='Compare two images: ')
compare_lbl.place(x=5, y=650)
avgcompare_btn = tk.Button(window, text='Avg', width=7, command=lambda:open2(1))
avgcompare_btn.grid(column = 0, row = 1, padx=5, pady =5)
avgcompare_btn.place(x=5, y=674)
#create btn to mid compare two img
midcompare_btn = tk.Button(window, text='Mid', width=7, command=lambda:open2(0))
midcompare_btn.grid(column = 1, row = 1, padx=5, pady =5)
midcompare_btn.place(x=94, y=674)

#creat btn to lapacian
lapacian = tk.Button(window, text='Lapacian', width = 18, command=lapacian)
lapacian.grid(column = 0, row = 0, padx=5, pady =5)
lapacian.place(x=5, y = 718)

#create btn to reset all
reset_btn = tk.Button(window, text = 'Reset ALL', width=18, command=reset)
reset_btn.grid(column = 0, row = 0, padx=5, pady =5)
reset_btn.place(x=5, y=755)



window.geometry("1040x790")
window.mainloop()
