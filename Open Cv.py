import cv2  #for image processing
import matplotlib.pyplot as plt
import numpy as np #to store image
import easygui # to open the filebox
import imageio # to read image stored at particular path
import os
import sys
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

#-----step 1------------------------------------UI---------------------------------------------------

top=tk.Tk()
top.geometry('600x400')
top.title('Cartonize image')
Label(top, text='cartonize image is here', fg='black', bg='white', relief='solid',font='font').place(x=200,y=20)

# --step 2---------------------------------BUILDING BOX TO CHOOESE THE FILE--------------------------
# fileopenbox() is the method in easyGUI module which returns
# the path of the chosen file as a string and choose the file from the device
def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)
# --step 3-----------------------------HOW IMAGE IS STORED---------------------------------------
#--how image is stored and a computer can read that, computers are reading images as numbers,so here 
# we cmp are rdng d file thru numpy arrays
# Imread is a method in cv2 which is used to store images in the form of numbers
# cv2.cvtColor() method is used to convert an image from one color space to another
def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    
# ------------------------------------STEP 4 GRAYING THE IMAGE--------------------------------------
# Beginning with image transformations,first we will change it to gray, then we will try to extract
# the edges and then shape print out our photos
    #converting an image to grayscale
    ReSized1 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    # After each transformation, we resize the resultant image
    # using the resize() method in cv2 and display it using imshow() method.

# step 5------------------------------SMOOTHING THE GRAY IMAGE---------------------------------------
   #applying median blur to smoothen an image
    
# STEP 6-------------------------------RETRIEVING THE EDGES---------------------------------------    
    # retrieving the edges for cartoon effect
    # by using thresholding technique
    # The threshold value is the mean of the neighborhood pixel values area minus the constant C
    # Thresh_binary is the type of threshold applied, and the remaining parameters 
    # determine the block size.
    # C is a constant that is subtracted from the mean or weighted sum of the neighborhood pixels.
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
# STEP 7--------------#Preparing a Mask Image(an image with binary numbers)------------------ 
    # applying bilateral filter to remove noise and keep edge sharp as required or extent smoothing
    # here the forth remove roughness in image and make it to look like vicious or water paint
    # BEAUTIFY
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))

# STEP 9:-------------------------------PLOTTING ALL THE TRANSITIONS TOGETHER--------------------      
    '''
squeeze: Boolean value specifying whether to squeeze out extra dimension
 from the returned axes array ax. The default value is False.
subplot_kw: Dict of keywords to be passed to the add_subplot call to add keywords to each subplot. 
The default value is None.
gridspec_kw: Dict of grid specifications passed to GridSpec constructor
to place grids on each subplot. The default value is None.
**fig_kw: Any additional keyword arguments to be 
subl=plots in a plot and display one-one images in each block on the axis using imshow() method.

plt.show() plots the whole plot at once after we plot on each subplot  '''
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save cartoon image",command=lambda: save(ReSized6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
# ------------------------------------STEP 11 : FUNCTIONALLY OF SAVE BUTTON-----------------------    

    #saving an image using imwrite()
def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()


top.mainloop()
   