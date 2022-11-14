from tkinter import filedialog

import cv2
import sys
import tkinter

def GetFile():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return filedialog.askopenfilename(title="Select Image")

def DisplayDecay(disvar):
    count = 0
    resvar = 0
    for i in range(0, disvar.shape[0]):
        for j in range(0, disvar.shape[1]):
            if alpha[i, j] == 0:
                resvar += 1
            if disvar[i, j] < tkvar.get():
                count += 1
    percent = (count / resvar) * 100
    DiseasePercent.set("Disease %: " + str(round(percent, 2)) + "%")

def GetAlphaChannel(img):
    global alpha
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i, j, 0] > 200 and img[i, j, 1] > 200 and img[i, j, 2] > 200:
                alpha[i, j] = 255
            else:
                alpha[i, j] = 0

def ProcessImage(self):
    img = cv2.imread(filename, 1)
    cv2.imshow("Original Image", img)
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    cv2.imshow("Red Channel", r)
    cv2.imshow("Green Channel", g)
    cv2.imshow("Blue Channel", b)
    disvar = r - g
    global alpha
    alpha = b
    GetAlphaChannel(img)
    cv2.imshow("Alpha Channel", alpha)
    ThresholdingFactor = tkvar.get()
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if int(g[i, j]) > ThresholdingFactor:
                disvar[i, j] = 255
    cv2.imshow("Segmented Image", disvar)
    DisplayDecay(disvar)
    tkvar.bind('<ButtonRelease-1>', ProcessImage)
    MainWindow.mainloop()





alpha = None
MainWindow = tkinter.Tk()
MainWindow.title("Plant Disease Detector")

tkvar = tkinter.Scale(MainWindow, from_=0, to=255, length=500, orient=tkinter.HORIZONTAL,
                  background='white', fg='black', troughcolor='white', label="Thresholding Factor")
tkvar.pack()
tkvar.set(150)

DiseasePercent = tkinter.StringVar()
L = tkinter.Label(MainWindow, textvariable=DiseasePercent)
L.pack()

filename = GetFile()
if filename != "":
    ProcessImage(None)
else:
    print("No File Uploaded!")
    exit(0)