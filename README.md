# 🖼️ Linux-Based Python Image Processing System

This is a **Python-based image processing system on Linux**, designed to simulate core functionalities of **Photoshop**, including filtering, color manipulation, FFT/DFT analysis, and various enhancement techniques. It integrates the content of **three homework projects (HW1–HW3)**.

---

## 📂 Getting Started

- Use **"Open File"** (top-left corner) to load an image.
- Explore different features grouped into HW1, HW2, and HW3 sections.

---

## 🧪 HW1 — Basic Image Operations

### ✨ Functions

- **Brightness / Contrast**  
  Adjust image brightness or contrast via sliders.  
  (*Implemented with `PIL.ImageEnhance`*)

- **Rotate**  
  Enter an angle, then click **"Rotate it"** to rotate the image.

- **Self-Defined Transforms**  
  Input values `a` and `b` and apply:
  - Linear
  - Exponential
  - Logarithmic

- **Gray-level Range Selection**  
  Show pixels in a specific gray-level range.  
  - "Turn black": non-range pixels become gray.  
  - "Show origin": non-range pixels stay unchanged.

- **Reset**  
  Restore original image state.

- **Save As**  
  Export images as `.jpg` or `.tif`.

### 📦 Libraries Used

- `PIL` for image enhancements
- `ImageTk`, `imutils` for display & resizing
- `matplotlib.pyplot` for visualizations

---

## 📊 HW2 — Histogram & Bit-plane Processing

### 🔍 Features

- **Histogram Display**  
  View grayscale histogram of the image.

- **Auto-Leveling**  
  Perform auto histogram equalization (`cv2.equalizeHist`).

- **Bit-plane Slicing (0–7)**  
  Enter a number (0–7) and visualize corresponding bit-plane.

- **Smooth / Sharp Toggle**  
  Use Gaussian blur + sharpening mask (`cv2.GaussianBlur`, `cv2.addWeighted`).

- **Compare Two Images (Avg / Mid)**  
  - Select two images and compare with average or median filters.  
  - Outputs difference image and **MSE** in terminal.  
  - Uses `cv2.filter2D` + `ImageChops.difference`.

- **Laplacian Filter**  
  Apply median blur, then Laplacian mask  
  `[[1, 1, 1], [1, -8, 1], [1, 1, 1]]` for edge enhancement.

---

## 🧬 HW3 — Advanced Image Processing

### 🧯 Filter (Average / Median)

- Input a spatial size (e.g., `3*3`, `7*7`)
- Apply average or median blur accordingly.

### 🌐 FFT (Fast Fourier Transform)

- Show 6 images:
  - Magnitude spectrum: `20*log(abs(f))`
  - Phase spectrum: `angle(fshift)`
  - Inverse FFT: `np.fft.ifft2`

### 📡 DFT (Discrete Fourier Transform)

- Display 5 DFT-related image outputs.

### 🎨 Color Operations

- **RGB Components**  
  Show R, G, B channels via slicing.

- **RGB to HSI Conversion**  
  Extract RGB via `split()` and calculate H, S, I using formulas.

- **Color Complement**  
  Display original and complemented image (`255 - img`).

- **Compare RGB/HSI – Smooth / Sharp**  
  Apply both smoothing and sharpening, then compare RGB and HSI results.

### 🖌️ Hue / Saturation Enhancement

- Convert to HSV
- Use `cv2.inRange()` to mask feathers based on H/S
- Apply `binary_closing()` and `measure.label()`
- Visualize using `color.label2rgb()`

---

## 📎 Requirements

- Python 3.x
- `PIL`, `opencv-python`, `numpy`, `matplotlib`, `scikit-image`, `imutils`

Install via pip:

```bash
pip install pillow opencv-python numpy matplotlib scikit-image imutils
```
Copyright © 2023 by 1ching. All rights reserved.
