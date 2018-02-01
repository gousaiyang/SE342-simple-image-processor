# SE342-simple-image-processor

## Introduction
This is a repo which contains the project of the course **Computer Vision** (SE342) in SJTU in year 2017-2018.

## Project Requirements
This project implements a simple image processing tool with the following functionalities:
- Color Image Processing
  - [x] RGB Bands Splitting
  - [x] Color -> Grayscale
  - [x] HSL Adjusting
  - [ ] Color Gradation Adjusting (Bonus)
- Binarization
  - [x] Otsu's method
  - [x] Manual (Two Thresholds)
- Arithmetic & Geometric Ops
  - [x] Addition, Subtraction, Multiplication, Crop
  - [x] Scaling and Rotation (Nearest, Bilinear)
- Contrast Adjustment
  - [x] Linear, Piecewise Linear
  - [x] Logarithmic, Exponential
  - [x] Histogram Display
  - [x] Histogram Equalization
- Smooth Filter
  - [x] Average
  - [x] Median
  - [x] Gaussian
  - [x] Custom Filter
- Edge Detection
  - [x] Sobel
  - [x] Laplacian
  - [ ] Canny
- Hough Transform (Bonus)
  - [ ] Line Detection
  - [ ] Circle Detection
- Binary Morphology
  - [x] Dilation, Erosion
  - [x] Opening, Closing
  - [x] Thinning, Thickening
  - [x] Distance Transform
  - [x] Skeletonization, Skeleton Reconstruction
  - [x] Morphology Reconstruction
- Grayscale Morphology
  - [x] Dilation, Erosion
  - [x] Opening, Closing
  - [x] Morphology Reconstruction
  - [ ] Watershed

The program should have a convenient GUI, which can:
- [x] Read / Save common image formats
- [x] Display realtime cursor position and pixel value

As required by our instructor, we should implement all algorithms by ourselves instead of directly calling functions of existing CV libraries (e.g. OpenCV). However, we can use such libraries to read and write images.

Also, after finishing implementation, we should use our own tool to analyse eyeball images to detect lesion.

## Environment
This project is supposed to run well on any major OS (Windows, Linux, macOS). It requires Python 3, and you should have the following modules installed:
- `tkinter` (for GUI)
- `pillow` (for image reading and writing)
- `numpy` and `matplotlib` (for histogram display)

## About Performance
Python programs (interpreted) often run (much) slower than C++ programs (compiled). And image operations in this project are not optimized at all. So the program demonstates a poor performance when dragging some of the sliders (realtime calculation and display). Personally, I'm choosing Python for rapid development. Here are some possible methods to improve performance:
- Use [PyPy](http://pypy.org/) to run the program (the JIT compiler)
- Use matrix representation and operations provided by `numpy` (optimized C implementation)
- Use C++ to develop the whole project or the algorithm modules

## Appendixes
- [A brief document](./附加部分说明.pdf) discribing project features and eyeball lesion detection.
- [An eyeball image](./test_imgs/eyeball.jpg) provided by our instructor.

## License
- The eyeball image is provided by our instructor and can only be used for educational purposes.
- All the code in this repo follows the MIT license.
