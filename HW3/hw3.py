from PIL import Image, ImageTk, ImageEnhance, ImageChops
import cv2
import tkinter as tk
import numpy as np
import imutils
from tkinter import filedialog
import matplotlib.pyplot as plt
import glob
import math
from scipy import ndimage as nd
from skimage import io, measure, color


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
		global hsi_lwpImg 
		image = cv2.imread(path_image)
		image = imutils.resize(image, height = 750)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		bit_plane_img = cv2.imread(path_image, 0)
		last = image
		size_img = last
		gray_img = last
		hsi_lwpImg = last
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
	open2btn.place(x=980, y=5)
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

# right
def spatial_smooth(x):
	global last
	global size_img
	global gray_img
	degree = int(spatial_smooth_entry.get())
	if(x == 1):
		degree_ = degree*degree
		kernel = np.ones((degree, degree),np.float32)/degree_
		dst = cv2.filter2D(image,-1,kernel)
	else:
		dst = cv2.medianBlur(image,degree)

	adjust = Image.fromarray(dst)
	img = ImageTk.PhotoImage(image = adjust)
	image_place.configure(image=img)
	image_place.image = img
	last = np.array(adjust)
	size_img = last
	gray_img = last

def fft_spec():
	# magnitude
	img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20*np.log(np.abs(fshift))
	phase_spectrum = np.angle(fshift)

	f_mag = np.abs(f)
	f_pha = f / (np.abs(f))
	mag = np.fft.ifft2(f_mag)
	pha  = np.fft.ifft2(f_pha)
	mag = np.real(mag)
	pha = np.real(pha)
	
	f_ishift = np.fft.ifftshift(fshift)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.real(img_back)
	
	plt.subplot(231),plt.imshow(img, cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(232),plt.imshow(magnitude_spectrum, cmap = 'gray')
	plt.title('Magintude Spectrum'), plt.xticks([]), plt.yticks([])
	plt.subplot(233),plt.imshow(phase_spectrum, cmap = 'gray')
	plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
	plt.subplot(234),plt.imshow(mag, cmap = 'gray')
	plt.title('Magnitude only ifft'), plt.xticks([]), plt.yticks([])
	plt.subplot(235),plt.imshow(pha, cmap = 'gray')
	plt.title('Phase only ifft'), plt.xticks([]), plt.yticks([])
	plt.subplot(236),plt.imshow(img_back, cmap = 'gray')
	plt.title('IFFT'), plt.xticks([]), plt.yticks([])
	plt.show()

def rgb_compo():
	img = image
	r, g, b = cv2.split(img)       # get b,g,r
	rgb_img = cv2.merge([r,g,b])
	x,y,z = np.shape(img)
	red = np.zeros((x,y,z),dtype=int)
	green = np.zeros((x,y,z),dtype=int)
	blue = np.zeros((x,y,z),dtype=int)
	for i in range(0,x):
		for j in range(0,y):
			red[i][j][0] = rgb_img[i][j][0]
			green[i][j][1]= rgb_img[i][j][1]
			blue[i][j][2] = rgb_img[i][j][2]
	
	plt.subplot(131),plt.imshow(red)
	plt.title('Red'), plt.xticks([]), plt.yticks([])
	plt.subplot(132),plt.imshow(green)
	plt.title('Green'), plt.xticks([]), plt.yticks([])
	plt.subplot(133),plt.imshow(blue)
	plt.title('Blue'), plt.xticks([]), plt.yticks([])
	plt.show()


def rgb_to_hue(b, g, r):
    angle = 0
    if b != g != r:
        angle = 0.5 * ((r - g) + (r - b)) / math.sqrt(((r - g) ** 2) + (r - b) * (g - b))
    if b <= g:
        return math.acos(angle)
    else:
        return 2 * math.pi - math.acos(angle)


def rgb_to_intensity(b, g, r):
    val = (b + g + r) / 3.
    if val == 0:
        return 0
    else:
        return val


def rgb_to_saturity(b, g, r):
    if r + g + b != 0:
        return 1. - 3. * np.min([r, g, b]) / (r + g + b)
    else:
        return 0

def HSI_to_bgr(h, s, i):
    h = math.degrees(h)
    if 0 < h <= 120 :
        b = i * (1 - s)
        r = i * (1 + (s * math.cos(math.radians(h)) / math.cos(math.radians(60) - math.radians(h))))
        g = i * 3 - (r + b)
    elif 120 < h <= 240:
        h -= 120
        r = i * (1 - s)
        g = i * (1 + (s * math.cos(math.radians(h)) / math.cos(math.radians(60) - math.radians(h))))
        b = 3 * i - (r + g)
    elif 0 < h <= 360:
        h -= 240
        g = i * (1 - s)
        b = i * (1 + (s * math.cos(math.radians(h)) / math.cos(math.radians(60) - math.radians(h))))
        r = i * 3 - (g + b)
    return [b, g, r]



def to_hsi(x):
	global hsi_lwpImg 
	src = image

	height = int(src.shape[0])
	width = int(src.shape[1])
	b, g, r = cv2.split(src)
	new_image = np.zeros((height, width, 3), dtype=np.uint8)
	
	I = np.zeros((height, width))
	S = np.zeros((height, width))
	H = np.zeros((height, width))

	for i in range(height) :
		for j in range(width) :
			b = src[i][j][0] / 255.
			g = src[i][j][1] / 255.
			r = src[i][j][2] / 255.
			H[i][j] = rgb_to_hue(b, g, r)
			S[i][j] = rgb_to_saturity(b, g, r)
			I[i][j] = rgb_to_intensity(b, g, r)
			# I[i][j] = 1. - I[i][j]

			bgr_tuple = HSI_to_bgr(H[i][j], S[i][j], I[i][j])

			new_image[i][j][0] = round(bgr_tuple[0] * 255.)
			new_image[i][j][1] = round(bgr_tuple[1] * 255.)
			new_image[i][j][2] = round(bgr_tuple[2] * 255.)
	
	if x==1:		
		plt.subplot(131),plt.imshow(H, cmap = 'gray')
		plt.title('Hue'), plt.xticks([]), plt.yticks([])
		plt.subplot(132),plt.imshow(S, cmap = 'gray')
		plt.title('Saturation'), plt.xticks([]), plt.yticks([])
		plt.subplot(133),plt.imshow(I, cmap = 'gray')
		plt.title('Intensity'), plt.xticks([]), plt.yticks([])
		plt.show()
	if x== 2:
		return H, S, I, width, height, new_image

# def to_hsi1(x):
	global hsi_lwpImg 
	rgb_lwpImg = image

	rows = int(rgb_lwpImg.shape[0])
	cols = int(rgb_lwpImg.shape[1])
	r, g, b = cv2.split(rgb_lwpImg)
	# 歸一化到[0,1]
	b = b / 255.0
	g = g / 255.0
	r = r / 255.0
	hsi_lwpImg = rgb_lwpImg.copy()
	hsi_lwpImg1 = rgb_lwpImg.copy()
	hsi_lwpImg2 = rgb_lwpImg.copy()
	hsi_lwpImg3 = rgb_lwpImg.copy()
	H, S, I = cv2.split(hsi_lwpImg)
	for i in range(rows):
		for j in range(cols):
			num = 0.5 * ((r[i, j]-g[i, j])+(r[i, j]-b[i, j]))
			den = np.sqrt((r[i, j]-g[i, j])**2+(r[i, j]-b[i, j])*(g[i, j]-b[i, j]))
			theta = float(math.cos(num/den))

			if den == 0:
					H = 0
			elif b[i, j] <= g[i, j]:
				H = theta
			else:
				H = 2*3.14169265 - theta

			min_RGB = min(min(b[i, j], g[i, j]), r[i, j])
			sum = b[i, j]+g[i, j]+r[i, j]
			if sum == 0:
				S = 0
			else:
				S = 1 - 3*min_RGB/sum

			H = H/(2*3.14159265)
			I = sum/3.0
			# 輸出HSI影象，擴充到255以方便顯示，一般H分量在[0,2pi]之間，S和I在[0,1]之間
			hsi_lwpImg1[i, j, 0] = H*255
			hsi_lwpImg2[i, j, 1] = S*255
			hsi_lwpImg3[i, j, 2] = I*255
			hsi_lwpImg[i, j, 0] = H*255
			hsi_lwpImg[i, j, 1] = S*255
			hsi_lwpImg[i, j, 2] = I*255

	hsi_lwpImg1 = cv2.cvtColor(hsi_lwpImg1, cv2.COLOR_RGB2GRAY)
	hsi_lwpImg2 = cv2.cvtColor(hsi_lwpImg2, cv2.COLOR_RGB2GRAY)
	hsi_lwpImg3 = cv2.cvtColor(hsi_lwpImg3, cv2.COLOR_RGB2GRAY)
	
	if x==1:
		plt.subplot(131),plt.imshow(hsi_lwpImg1, cmap = 'gray')
		plt.title('Hue'), plt.xticks([]), plt.yticks([])
		plt.subplot(132),plt.imshow(hsi_lwpImg2, cmap = 'gray')
		plt.title('Saturation'), plt.xticks([]), plt.yticks([])
		plt.subplot(133),plt.imshow(hsi_lwpImg3, cmap = 'gray')
		plt.title('Intensity'), plt.xticks([]), plt.yticks([])
		plt.show()
	if x== 2:
		return H, S, I

def color_complement():
	img = image
	comp = 255-img
	plt.subplot(121), plt.imshow(img)
	plt.title('RGB image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122), plt.imshow(comp)
	plt.title('Complement image'), plt.xticks([]), plt.yticks([])
	plt.show()

def compare_smooth():
	H, S, I, width, height, hsi = to_hsi(2)
	rgb = image
	new_image = np.zeros((height, width, 3), dtype=np.uint8)
	degree = 5
	degree_ = degree*degree
	kernel = np.ones((degree, degree),np.float32)/degree_

	I=cv2.filter2D(I,-1,kernel)
	for i in range(height) :
		for j in range(width) :
			
			# I[i][j] = 1. - I[i][j]

			bgr_tuple = HSI_to_bgr(H[i][j], S[i][j], I[i][j])

			new_image[i][j][0] = round(bgr_tuple[0] * 255.)
			new_image[i][j][1] = round(bgr_tuple[1] * 255.)
			new_image[i][j][2] = round(bgr_tuple[2] * 255.)
	
	
	# hsi = new_image
	rgb_ = cv2.filter2D(image,-1,kernel)
	
	rgb1, rgb2 = Image.fromarray(rgb), Image.fromarray(rgb_)
	hsi1, hsi2 = Image.fromarray(hsi), Image.fromarray(new_image)

	diff_rgb = ImageChops.difference(rgb1, rgb2)
	diff_hsi = ImageChops.difference(hsi1, hsi2)
	diff_rgb_hsi = ImageChops.difference(rgb2, hsi2)

	plt.subplot(331), plt.imshow(rgb)
	plt.title('RGB image'), plt.xticks([]), plt.yticks([])
	plt.subplot(332), plt.imshow(rgb_)
	plt.title('Smooth RGB'), plt.xticks([]), plt.yticks([])
	plt.subplot(333), plt.imshow(diff_rgb)
	plt.title('smoothed RGB vs Origin'), plt.xticks([]), plt.yticks([])

	plt.subplot(334), plt.imshow(hsi)
	plt.title('HSI to rgb image'), plt.xticks([]), plt.yticks([])
	plt.subplot(335), plt.imshow(hsi)
	plt.title('Smooth HSI to rgb'), plt.xticks([]), plt.yticks([])
	plt.subplot(336), plt.imshow(diff_hsi)
	plt.title('smoothed HSI vs smoothed Origin'), plt.xticks([]), plt.yticks([])
	plt.subplot(337), plt.imshow(diff_rgb_hsi)
	plt.title('smoothed HSI vs smoothed RGB'), plt.xticks([]), plt.yticks([])
	
	plt.show()

def compare_sharp():
	H, S, I, width, height, hsi = to_hsi(2)
	new_image = np.zeros((height, width, 3), dtype=np.uint8)
	rgb = image
	kernel = np.array([[1, 1, 1],
                   [1, -8, 1],
                   [1, 1, 1]])

	I_ = cv2.filter2D(I,-1,kernel)
	I = I+I_
	for i in range(height) :
		for j in range(width) :
			
			bgr_tuple = HSI_to_bgr(H[i][j], S[i][j], I[i][j])

			new_image[i][j][0] = round(bgr_tuple[0] * 255.)
			new_image[i][j][1] = round(bgr_tuple[1] * 255.)
			new_image[i][j][2] = round(bgr_tuple[2] * 255.)

	rgb_ = cv2.filter2D(rgb,-1,kernel)


	hsi1, hsi2 = Image.fromarray(hsi), Image.fromarray(new_image)
	sharp_hsi = Image.fromarray(new_image)

	rgb1, rgb2 = Image.fromarray(rgb), Image.fromarray(rgb_)
	sharp_rgb = ImageChops.difference(rgb1, rgb2)

	# gray
	gsharp_hsi = Image.fromarray(cv2.cvtColor(new_image, cv2.COLOR_RGB2GRAY))
	ghsi = Image.fromarray(cv2.cvtColor(hsi, cv2.COLOR_RGB2GRAY))
	grgb1, grgb2 = Image.fromarray(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)), Image.fromarray(cv2.cvtColor(rgb_, cv2.COLOR_RGB2GRAY))
	gsharp_rgb = ImageChops.difference(grgb1, grgb2)

	diff_rgb = ImageChops.difference(grgb1, gsharp_rgb)
	diff_hsi = ImageChops.difference(ghsi, gsharp_hsi)
	diff_rgb_hsi = ImageChops.difference(gsharp_hsi, gsharp_rgb)
	# diff_rgb = cv2.cvtColor(diff_rgb, cv2.COLOR_RGB2GRAY)
	# diff_hsi = cv2.cvtColor(diff_hsi, cv2.COLOR_RGB2GRAY)
	# diff_rgb_hsi = cv2.cvtColor(diff_rgb_hsi, cv2.COLOR_RGB2GRAY)

	
	plt.subplot(331), plt.imshow(rgb)
	plt.title('RGB image'), plt.xticks([]), plt.yticks([])
	plt.subplot(332), plt.imshow(sharp_rgb)
	plt.title('Sharp RGB'), plt.xticks([]), plt.yticks([])
	plt.subplot(333), plt.imshow(diff_rgb, cmap='gray')
	plt.title('Sharped RGB vs RGB'), plt.xticks([]), plt.yticks([])
	plt.subplot(334), plt.imshow(hsi)
	plt.title('HSI image'), plt.xticks([]), plt.yticks([])
	plt.subplot(335), plt.imshow(new_image)
	plt.title('Sharp HSI'), plt.xticks([]), plt.yticks([])
	plt.subplot(336), plt.imshow(diff_hsi, cmap='gray')
	plt.title('Sharped HSI vs HSI'), plt.xticks([]), plt.yticks([])
	plt.subplot(337), plt.imshow(diff_rgb_hsi, cmap='gray')
	plt.title('Sharped HSI vs Sharped RGB'), plt.xticks([]), plt.yticks([])
	
	plt.show()

def hs_enhance():
	img = image
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	mask = cv2.inRange(hsv, (149, 130, 0), (158, 255, 120))
	closed_mask = nd.binary_closing(mask, np.ones((9, 9)))
	label_img = measure.label(closed_mask)
	image_label_overlay = color.label2rgb(label_img, image=img)


	plt.subplot(231), plt.imshow(img)
	plt.title('RGB image'), plt.xticks([]), plt.yticks([])
	plt.subplot(232), plt.imshow(hsv)
	plt.title('HSV image'), plt.xticks([]), plt.yticks([])
	plt.subplot(233), plt.imshow(mask)
	plt.title('choosing feather'), plt.xticks([]), plt.yticks([])
	plt.subplot(234), plt.imshow(closed_mask)
	plt.title('mask'), plt.xticks([]), plt.yticks([])
	plt.subplot(235), plt.imshow(label_img)
	plt.title('mask image'), plt.xticks([]), plt.yticks([])
	plt.subplot(236), plt.imshow(image_label_overlay)
	plt.title('final image'), plt.xticks([]), plt.yticks([])
	
	plt.show()

def dft():
	img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	N,M = np.shape(img)
	i, j = np.meshgrid(np.arange(M), np.arange(N))
	mult_factor = np.power( np.ones((N,M)) * -1 , i + j )
	tmp = img * mult_factor
	dft = np.fft.fft2(tmp)
	conj = dft.conj()
	idft = np.fft.ifft2(conj)
	out_img = np.abs((mult_factor * idft.real) + (1j * idft.imag))

	plt.subplot(231), plt.imshow(mult_factor, cmap='gray')
	plt.title('1'), plt.xticks([]), plt.yticks([])
	plt.subplot(232), plt.imshow(np.real(dft), cmap='gray')
	plt.title('2'), plt.xticks([]), plt.yticks([])
	plt.subplot(233), plt.imshow(np.real(conj), cmap='gray')
	plt.title('3'), plt.xticks([]), plt.yticks([])
	plt.subplot(234), plt.imshow(np.real(idft), cmap='gray')
	plt.title('4'), plt.xticks([]), plt.yticks([])
	plt.subplot(235), plt.imshow(out_img, cmap='gray')
	plt.title('5'), plt.xticks([]), plt.yticks([])
	plt.show()



image = None
compare = 1

window = tk.Tk()
window.title('DIP Class HW1')

#place for image to show up
image_place = tk.Label(window, width=750)
image_place.grid(column=0, row=2)
image_place.place(x=200 , y=5)

#pace for two imgs to show up
image1_place = tk.Label(window, width=400)
image1_place.grid(column=0, row=2)
image1_place.place(x=320, y=20)
image2_place = tk.Label(window, width=400)
image2_place.grid(column=0, row=2)
image2_place.place(x=320, y=390)

open2btn = tk.Button(window, text = 'Open two Files', width=14)
open2btn.place(x=980, y=5)
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

# right
#create filter entry and button
spatial_smooth_lbl = tk.Label(window, text='Filter')
spatial_smooth_lbl.place(x = 965, y = 45)
spatial_smooth_entry = tk.Entry(window, width=12)
spatial_smooth_entry.place(x = 1032, y = 45)
avg_spatial_smooth_btn = tk.Button(window, text='Avg', width=7, command=lambda:spatial_smooth(1))
avg_spatial_smooth_btn.grid(column = 0, row = 1, padx=5, pady =5)
avg_spatial_smooth_btn.place(x=965, y=70)
mid_spatial_smooth_btn = tk.Button(window, text='Mid', width=7, command=lambda:spatial_smooth(0))
mid_spatial_smooth_btn.grid(column = 1, row = 1, padx=5, pady =5)
mid_spatial_smooth_btn.place(x=1050, y=70)

# fft
fft_lbl = tk.Label(window, text='FFT')
fft_lbl.place(x = 965, y=115)
fft_btn = tk.Button(window, text='spectrum', width=18, command=fft_spec)
fft_btn.place(x = 965, y = 135)

# red component
red_compo_btn = tk.Button(window, text='RGB component', command=rgb_compo, width=18)
red_compo_btn.place(x = 965, y = 180)

# rgb to hsi
tohsi_btn = tk.Button(window, text='RGB to HSI', command=lambda:to_hsi(1), width=18)
tohsi_btn.place(x=965, y = 220)

# color complement
color_complement_btn = tk.Button(window, text = 'Color complement', command=color_complement, width=18)
color_complement_btn.place(x=965, y=260)

# compare rgb origin hsi
compare_smooth_btn = tk.Button(window, text = 'Compare RGB/HSI smooth', command=compare_smooth, width=18)
compare_smooth_btn.place(x = 965, y=300)
compare_sharp_btn = tk.Button(window, text = 'Compare RGB/HSI sharp', command=compare_sharp, width=18)
compare_sharp_btn.place(x=965, y=340)

# hs enhance
hs_enhance_btn = tk.Button(window, text = 'Hue/Saturation enhance', command=hs_enhance, width=18)
hs_enhance_btn.place(x=965, y=380)

# dft 
dft_btn = tk.Button(window, text='DFT', command=dft, width=18)
dft_btn.place(x=965, y=420)

window.geometry("1150x790")
window.mainloop()
