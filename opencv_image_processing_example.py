# -------------------------------------
# OpenCV example with Python
#  Using the EXAMPLE to run the different example
# -------------------------------------
import cv2
from matplotlib import pyplot as plt
import requests                 # Not necessary for OpenCV
import urllib.request           # Not necessary for OpenCV
from bs4 import BeautifulSoup   # Not necessary for OpenCV
import os                       # Not necessary for OpenCV

# 1: base, 2: color space, 3: filtering, 4: edge, circles
EXAMPLE = 4

DOWNLOAD_FLAG = 0
PIC_DOWNLOAD = "download.jpg"
PIC_KEYWORD = "ian goodfellow deep learning"
LINK_PRE = "https://search.books.com.tw/search/query/key/"
LINK_POST = "/cat/all"

# -------------------------------------
# Case 1: basic image operating
#  ref: https://docs.opencv.org/3.1.0/dc/d2e/tutorial_py_image_display.html
# -------------------------------------
def case1():
    print("Case 1: basic image operating")
    # -- gray
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    # -- resize
    img_resize = cv2.resize(img_gray, (640, 480), interpolation=cv2.INTER_CUBIC)

    cv2.imshow('orignal', img_src)
    cv2.imshow('gray', img_gray)
    cv2.imshow('resize', img_resize)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # -- write the changed pciture to a file named xxx.png
    cv2.imwrite('xxx.png',img_resize)

# -------------------------------------
#  Case 2: color space changing
# -------------------------------------
def case2():
    print("Case 2: color space changing")
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.resize(img_gray, (640, 480), interpolation=cv2.INTER_CUBIC)

    img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
    img_hsv = cv2.resize(img_hsv, (640, 480), interpolation=cv2.INTER_CUBIC)

    cv2.imshow('orignal', img_src)
    cv2.imshow('gray', img_gray)
    cv2.imshow('hsv', img_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# -------------------------------------
# Case 3: image filtering
#   Averaging, Gaussian Blurring, Median Blurring, Bilateral Filtering
#  ref: https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
# -------------------------------------
def case3():
    print("Case 3: image filtering")
    img_resize = cv2.resize(img_src, (640, 480), interpolation=cv2.INTER_CUBIC)
    img_blur = cv2.blur(img_resize, (5,5))
    img_gaussian = cv2.GaussianBlur(img_resize, (5,5), 0)
    img_median = cv2.medianBlur(img_resize, 5)
    img_bilateral = cv2.bilateralFilter(img_resize,9,75,75)

    cv2.imshow('orignal', img_resize)
    cv2.imshow('blur', img_blur)
    cv2.imshow('gaussian', img_gaussian)
    cv2.imshow('median', img_median)
    cv2.imshow('bilateral', img_bilateral)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
# -------------------------------------
# Case 4: edge detection
#   Sobel ref: https://blog.csdn.net/sunny2038/article/details/9170013
#   Laplace ref: https://blog.csdn.net/sunny2038/article/details/9188441
# -------------------------------------
def case4():
    print("Case 4: edge detection")
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_gray, (640, 480), interpolation=cv2.INTER_CUBIC)

    # -- no filter
    img_noFilter = cv2.Canny(img_resize, 100, 255)

    # -- w/ filter - GaussianBlur
    img_gaussian = cv2.GaussianBlur(img_resize, (5,5), 0)
    img_useFilter = cv2.Canny(img_gaussian, 100, 255)

    # -- Sobel
    grad_x = cv2.Sobel(img_useFilter, cv2.CV_16S, 1, 0)
    grad_y = cv2.Sobel(img_useFilter, cv2.CV_16S, 0, 1)
    img_abs_x = cv2.convertScaleAbs(grad_x)
    img_abs_y = cv2.convertScaleAbs(grad_y)
    img_sobel = cv2.addWeighted(img_abs_x, 0.5, img_abs_y, 0.5, 0)

    # -- Laplace
    img_laplace = cv2.Laplacian(img_useFilter, cv2.CV_32F, ksize = 3)    
    img_laplace = cv2.convertScaleAbs(img_laplace)

    cv2.imshow('orignal', img_resize)
    cv2.imshow('no filter', img_noFilter)
    cv2.imshow('use filter', img_useFilter) 
    cv2.imshow('sobel - abs_x', img_abs_x)
    cv2.imshow('sobel - abs_y', img_abs_y)
    cv2.imshow('sobel', img_sobel)
    cv2.imshow('laplace', img_laplace)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# -------------------------------------
# Download sample image
# -------------------------------------
def download_pic():
    if PIC_KEYWORD.find(' '):
        PIC_KEYWORD.replace(' ', '%20')

    html = requests.get(LINK_PRE + PIC_KEYWORD + LINK_POST)
    body = BeautifulSoup(html.text, 'html.parser')
    blank = body.select("img[class='itemcov']")
    img_link = blank[0]['data-original'].split('?')[1].split('&')[0].split('=')[1]
    print("[INF]Download picture from: " + img_link)

    urllib.request.urlretrieve(img_link, PIC_DOWNLOAD)
    

# -------------------------------------
# Main
# -------------------------------------
img_src = cv2.imread(PIC_DOWNLOAD)

if img_src is None:
    print ("[WRN]The image didn't exist!")
    download_pic()
    img_src = cv2.imread(PIC_DOWNLOAD)
    DOWNLOAD_FLAG = 1

if   EXAMPLE == 1:
    case1()
elif EXAMPLE == 2:
    case2()
elif EXAMPLE == 3:
    case3()
elif EXAMPLE == 4:
    case4()
else:
    print("[WRN]No matched any sample case!")

if DOWNLOAD_FLAG == 1:
    print ("[INF]Deleted the downloaded image file.")
    os.remove(PIC_DOWNLOAD)


