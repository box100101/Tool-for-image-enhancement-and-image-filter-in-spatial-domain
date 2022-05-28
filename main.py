from email.mime import image
from pydoc import cli
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import PIL
from tkinter import filedialog
from cv2 import cvtColor, imread, imshow
import numpy as np
import cv2 as cv
import os
from tkinter.filedialog import asksaveasfilename


# CODE

form_main = Tk()
form_main.geometry("1300x750+120+20")
form_main.title("Digital Image Processing")

# Label
namePorject = Label(form_main, text= "Tool for image enhancement and image filter in spatial domain")
namePorject.config(font=("Courier bold", 14), bg="green", fg="white")
namePorject.pack()
label_1 = Label(form_main, text= "Original")
label_1.config(font=("Courier", 12))
label_1.place(x=35, y=35)
label_2 = Label(form_main, text= "After processing")
label_2.config(font=("Courier", 12))
label_2.place(x=35, y=345)

label_transformation_function = Label(form_main, text= "Transformation Functions")
label_transformation_function.config(font=("Courier", 12), bg="orange", fg="black")
label_transformation_function.place(x=460, y=60)

label_filter = Label(form_main, text= "Filter")
label_filter.config(font=("Courier", 12), bg="orange", fg="black")
label_filter.place(x=880, y=60)
# ----------------------------------------------------------------------------

# Frame
frame_original = Frame(form_main, width=398, height=258, highlightbackground = "black", highlightthickness= 2 , bg= "white", relief=SUNKEN)
frame_original.place(x=35, y=60)
frame_after_processing = Frame(form_main, width=398, height=258, highlightbackground = "black", highlightthickness= 2 , bg= "white", relief=SUNKEN)
frame_after_processing.place(x=35, y=370)

frame_function_transformation = Frame(form_main, width=400, height=600, highlightbackground = "black", highlightthickness= 2 , bg= "white", relief=SUNKEN)
frame_function_transformation.place(x=460, y=90)
frame_filter = Frame(form_main, width=400, height=600, highlightbackground = "black", highlightthickness= 2 , bg= "white", relief=SUNKEN)
frame_filter.place(x=880, y=90)
# ----------------------------------------------------------------------------

# Function
def files_images():
    file_path = filedialog.askopenfilename(
        initialdir="./images", title="Select File", filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    return file_path
    

def importFile():
    global image
    global import_img_path
    global originalImage
    import_img_path = files_images()
    originalImage = cv.imread(import_img_path)
    originalImage = cv.resize(originalImage, (390, 250))
    image = cv.cvtColor(originalImage, cv.COLOR_BGR2RGB)
    originalImage = image
    updateOrignal(originalImage)
    updateAfterProcessing(image)


def saveFile():
    store_temp_image(frame_after_processing.picture)


def clear():
    updateAfterProcessing(image)

def store_temp_image(imagetk):
    new_file_name = asksaveasfilename(initialdir="./Images after processing/", title="Select file", defaultextension=".png", filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
    imgpil = ImageTk.getimage(imagetk)
    imgpil.save(os.path.join("./Images after processing/", new_file_name), "PNG")
    imgpil.close()


def updateOrignal(img):
    np_array = np.array(img)
    pil_image=Image.fromarray(np_array)
    frame_original.picture = ImageTk.PhotoImage(pil_image)   
    frame_original.label = Label(frame_original, image = frame_original.picture)
    frame_original.label.place(x=0, y=0)


def updateAfterProcessing(img):
    np_array = np.array(img)
    pil_image=Image.fromarray(np_array)
    frame_after_processing.picture = ImageTk.PhotoImage(pil_image)   
    frame_after_processing.label = Label(frame_after_processing, image = frame_after_processing.picture)
    frame_after_processing.label.place(x=0, y=0)


# Binary
def binary(var):
    img_temp = cvtColor(image, cv.COLOR_BGR2GRAY)
    img = cv.adaptiveThreshold(img_temp, maxValue=255, adaptiveMethod=cv.ADAPTIVE_THRESH_MEAN_C, 
                                  thresholdType=cv.THRESH_BINARY, blockSize=15, C=sliderBinary.get())
    updateAfterProcessing(img)
  
def setBinaryValue():
    sliderBinary.set(8)
    binary
# ---------------------------------------------------------------------------

# Negative
def negative():
    img_temp = 255 - image
    updateAfterProcessing(img_temp)    
# ---------------------------------------------------------------------------

# Log Transformation
def logTransformation(var):
    c = 255 / np.log(1 + sliderlogTransformation.get())
    img_temp = c * (np.log(image + 1))
    img_temp = np.array(img_temp, dtype= np.uint8)
    updateAfterProcessing(img_temp)

def setLogTransformationValue():
    sliderlogTransformation.set(255)
    sliderlogTransformation
# ---------------------------------------------------------------------------


# Power Law Transformation
def powerLawTransformation(var):
    img_temp = np.array(sliderPowerLawTransformation_const.get()*(image/255)**(sliderPowerLawTransformation_gamma.get()),dtype='uint8')
    updateAfterProcessing(img_temp)

def setPowerLawTransformationValue():
    sliderPowerLawTransformation_const.set(255)
    sliderPowerLawTransformation_gamma.set(1.2)
    powerLawTransformation
# ---------------------------------------------------------------------------


# Piecewise-Linear Transformation  
def pieceWiseLinearTransformation(self):
    r1 = sliderPiecewiseLinearTransformation_r1.get()
    s1 = sliderPiecewiseLinearTransformation_s1.get()
    r2 = sliderPiecewiseLinearTransformation_r2.get()
    s2 = sliderPiecewiseLinearTransformation_s2.get()
    def pixelVal(pix, r1, s1, r2, s2):
        if (0 <= pix and pix <= r1):
            return (s1 / r1)*pix
        elif (r1 < pix and pix <= r2):
            return ((s2 - s1)/(r2 - r1)) * (pix - r1) + s1
        else:
            return ((255 - s2)/(255 - r2)) * (pix - r2) + s2
    pixelVal_vec = np.vectorize(pixelVal)
  
    img_temp = pixelVal_vec(image, r1, s1, r2, s2)
    img_temp = img_temp.astype(np.uint8)
    updateAfterProcessing(img_temp)

def setPieceWiseLinearTransformation():
    sliderPiecewiseLinearTransformation_r1.set(70)
    sliderPiecewiseLinearTransformation_s1.set(0)
    sliderPiecewiseLinearTransformation_r2.set(140)
    sliderPiecewiseLinearTransformation_s2.set(255)
    pieceWiseLinearTransformation
# ---------------------------------------------------------------------------

# Median Blur
def medianBlur(var):
    if(sliderMedianBlur.get() % 2 != 0):
        img_temp = cv.medianBlur(image, ksize= sliderMedianBlur.get())
        updateAfterProcessing(img_temp)

def setMedianBlurValue():
    sliderMedianBlur.set(5)
    medianBlur
# ---------------------------------------------------------------------------

# Sharpening
def sharpening():
    kernel = np.array([[0, -1,  0],
                    [-1,  5, -1],
                    [0, -1,  0]])
    img_temp = cv.filter2D(src=image, ddepth=-1, kernel=kernel)
    updateAfterProcessing(img_temp)
# ---------------------------------------------------------------------------

# Min Filter 
def minFilter():
    size = (3, 3)
    shape = cv.MORPH_RECT
    kernel = cv.getStructuringElement(shape, size)
    img_temp = cv.erode(image, kernel)
    updateAfterProcessing(img_temp)
# ---------------------------------------------------------------------------

# Max Filter
def maxFilter():
    size = (3, 3)
    shape = cv.MORPH_RECT
    kernel = cv.getStructuringElement(shape, size)
    img_temp = cv.dilate(image, kernel)
    updateAfterProcessing(img_temp)
# ---------------------------------------------------------------------------

# Laplace
def laplace(var):
    if(sliderLaplace.get() % 2 != 0):
        img_temp = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        img_temp = cv.Laplacian(img_temp, -1, ksize=sliderLaplace.get(), scale=1, delta=0, borderType=cv.BORDER_DEFAULT)
        updateAfterProcessing(img_temp)

def setLaplaceValue():
    sliderLaplace.set(15)
    laplace

# ---------------------------------------------------------------------------

# Gaussian Blur
def gaussianBlur(var):
    if(sliderGaussianBlur.get() % 2 != 0):
        c = sliderGaussianBlur.get()
        img_temp = cv.GaussianBlur(image, (c,c), 0)
        updateAfterProcessing(img_temp)

def setGaussianBlurValue():
    sliderGaussianBlur.set(5)
    gaussianBlur
# ---------------------------------------------------------------------------


# *Button control
btn_quit = Button(form_main, text="Quit", command = form_main.quit, width=15, height=2, fg="white", bg="black")
btn_quit.place(x=1150, y=700)

# +Button Import image
btn_import_img = Button(form_main, text="Import image", command =importFile, width=15, height=2, fg="black", bg="#96c0eb")
btn_import_img.place(x=30, y=700)

btn_save_img = Button(form_main, text="Save image", command =lambda:saveFile(), width=15, height=2, fg="black", bg="yellow")
btn_save_img.place(x=170, y=700)

# +Button clear
btn_clear = Button(form_main, text="Clear", command = clear, width=15, height=2, fg="black", bg="gray")
btn_clear.place(x=310, y=700)

# Button processing
btn_binary = Button(form_main, text="Binary", command = setBinaryValue, width=15, height=2, fg="black", bg="#FF6666")
btn_binary.place(x=665, y=120)

btn_negative = Button(form_main, text="Negative", command = negative, width=15, height=2, fg="black", bg="#FF6666")
btn_negative.place(x=470, y=460)

btn_logTransformation = Button(form_main, text="Log Transformation", command = setLogTransformationValue, width=15, height=2, fg="black", bg="#FF6666")
btn_logTransformation.place(x=665, y=250)

btn_powerLawTransformation = Button(form_main, text="Power Law Transformation", command = setPowerLawTransformationValue, width=20, height=2, fg="black", bg="#FF6666")
btn_powerLawTransformation.place(x=665, y=380)

btn_piecewiseLinearTransformation = Button(form_main, text="Piecewise-Linear Transformation", command = setPieceWiseLinearTransformation, width=25, height=2, fg="black", bg="#FF6666")
btn_piecewiseLinearTransformation.place(x=470, y=120)

btn_MedianBlur = Button(form_main, text="Median Blur", command = setMedianBlurValue, width=20, height=2, fg="black", bg="#2467BF")
btn_MedianBlur.place(x=890, y=120)

btn_sharpening = Button(form_main, text="Sharpening", command = sharpening, width=20, height=2, fg="black", bg="#2467BF")
btn_sharpening.place(x=1120, y=120)

btn_minFilter = Button(form_main, text="Min Filter", command = minFilter, width=20, height=2, fg="black", bg="#2467BF")
btn_minFilter.place(x=1120, y=170)

btn_maxFilter = Button(form_main, text="Max Filter", command = maxFilter, width=20, height=2, fg="black", bg="#2467BF")
btn_maxFilter.place(x=1120, y=220)

btn_laplace = Button(form_main, text="Laplace", command = setLaplaceValue, width=20, height=2, fg="black", bg="#2467BF")
btn_laplace.place(x=890, y=250)

btn_gaussianBlur = Button(form_main, text="Gaussian Blur", command = setGaussianBlurValue, width=20, height=2, fg="black", bg="#2467BF")
btn_gaussianBlur.place(x=890, y=380)
# ----------------------------------------------------------------------------

# *Sliders control
sliderBinary = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = binary, sliderlength = 10, length = 180, label="c", width=10, bg = "white")
sliderBinary.place(x=665, y=165)

sliderlogTransformation = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = logTransformation, sliderlength = 10, length = 180, label = "pixel value", width=10, bg = "white")
sliderlogTransformation.place(x=665, y=295)

sliderPowerLawTransformation_const = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = powerLawTransformation, sliderlength = 10, length = 180, label="c", width=10, bg = "white")
sliderPowerLawTransformation_const.place(x=665, y=425)
sliderPowerLawTransformation_gamma = Scale(form_main, from_=0, to =2.5, orient = HORIZONTAL, tickinterval= 0.5, command = powerLawTransformation, sliderlength = 10, length = 180, label="gamma", width=10, bg = "white", resolution=0.2)
sliderPowerLawTransformation_gamma.place(x=665, y=495)

sliderPiecewiseLinearTransformation_r1 = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = pieceWiseLinearTransformation, sliderlength = 10, length = 180, label="r1", width=10, bg = "white")
sliderPiecewiseLinearTransformation_r1.place(x=470, y=165)
sliderPiecewiseLinearTransformation_s1 = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = pieceWiseLinearTransformation, sliderlength = 10, length = 180, label="s1", width=10, bg = "white")
sliderPiecewiseLinearTransformation_s1.place(x=470, y=235)
sliderPiecewiseLinearTransformation_r2 = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = pieceWiseLinearTransformation, sliderlength = 10, length = 180, label="r2", width=10, bg = "white")
sliderPiecewiseLinearTransformation_r2.place(x=470, y=305)
sliderPiecewiseLinearTransformation_s2 = Scale(form_main, from_=0, to =255, orient = HORIZONTAL, tickinterval= 51, command = pieceWiseLinearTransformation, sliderlength = 10, length = 180, label="s2", width=10, bg = "white")
sliderPiecewiseLinearTransformation_s2.place(x=470, y=375)

sliderMedianBlur = Scale(form_main, from_=1, to =15, orient= HORIZONTAL, tickinterval= 3, command = medianBlur, sliderlength = 10, length = 180, label = 'ksize', width =10, bg = "white")
sliderMedianBlur.place(x=890, y=165)

sliderLaplace = Scale(form_main, from_=1, to =15, orient= HORIZONTAL, tickinterval= 3, command = laplace, sliderlength = 10, length = 180, label = 'ksize', width =10, bg = "white")
sliderLaplace.place(x=890, y=295)

sliderGaussianBlur = Scale(form_main, from_=1, to =15, orient= HORIZONTAL, tickinterval= 3, command = gaussianBlur, sliderlength = 10, length = 180, label = 'ksize', width =10, bg = "white")
sliderGaussianBlur.place(x=890, y=425)
# ----------------------------------------------------------------------------


mainloop()
