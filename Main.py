#==-- IMPORTS --==#
import cv2
import numpy as np
from cv2 import imread
import random
import os
import matplotlib.pyplot as plt
from Matcher import Matcher
from GUI import *

#==-- TKINTER GUI --==#
global methodpick


### Make new frame, including it's canvas and inner frame
def new_frame(h, w=500, scrollbar=False):
    global outer, canvas, inner, scrolly, frameposx, frameposy, width_temp, height_temp
    width_temp = w
    height_temp = h
    #
    outer.append(Frame(root,relief=GROOVE,width=w,height=h,bd=1))
    outer[-1].place(x=frameposx,y=frameposy)
    frameposx += (w+15)
    canvas.append(Canvas(outer[-1]))
    inner.append(Frame(canvas[-1]))
    #
    if(scrollbar):
        scrolly.append(Scrollbar(outer[-1],orient="vertical",command=canvas[-1].yview))
        canvas[-1].configure(yscrollcommand=scrolly[-1].set)
        scrolly[-1].pack(side="right",fill="y")
    #
    canvas[-1].pack(side="left")
    canvas[-1].create_window((0,0),window=inner[-1],anchor='nw')
    inner[-1].bind("<Configure>",conf_frame)

### Configure scrollbar for canvas
def conf_frame(event):
    global width_temp, height_temp
    canvas[-1].configure(scrollregion=canvas[-1].bbox("all"),width=width_temp,height=height_temp)

### New text label
def new_text(i, txt, key=str(defkey), incy=1, y="default", x=0, bgcolor="SystemMenu", fgcolor="black"):
    global rowg, defkey, labels
    if(y == "default"):
        y = rowg[i]
    #
    labels[key] = Label(inner[i], text=txt, bg=bgcolor, fg=fgcolor)
    labels[key].grid(row=y, column=x, sticky='ew', padx=2, pady=2)
    root.update()
    rowg[i] += incy
    defkey += 1

### New image label
def new_image(i, path, w, h, incy=1, y="default", x=0):
    global rowg, img
    if(y == "default"):
        y = rowg[i]
    #
    img.append(ImageTk.PhotoImage(Image.open(path).resize((w,h), Image.ANTIALIAS)))
    Label(inner[i], image=img[-1]).grid(row=y, column=x, sticky='w')
    root.update()
    rowg[i] += incy

### New button
def new_button(i, txt, cmd, key=str(defkey), btnstate="normal", incy=1, y="default", x=0):
    global rowg, defkey, buttons
    if(y == "default"):
        y = rowg[i]
    #
    buttons[key] = Button(inner[i], text=txt, command=cmd, state=btnstate)
    buttons[key].grid(row=y, column=x, sticky='ew', padx=2, pady=2)
    root.update()
    rowg[i] += incy
    defkey += 1

### Select directory from PC
def select_db():
    global dbpath, querypath, labels, buttons, matchready
    dbpath = filedialog.askdirectory(initialdir=" ", title="Select Database Directory...")
    if (dbpath != ""):
        labels["dbpath"].config(text=dbpath, fg="black")
        buttons["extract_button"].config(state="normal", fg="green")

### Select file from PC
def select_query():
    global dbpath, querypath, labels, matchready
    querypath = filedialog.askopenfilename(initialdir=" ", title="Select Query JPG...", filetypes = (("JPEG files", "*.jpg"), ("All files", "*.*")))
    if (querypath != ""):
        labels["querypath"].config(text=querypath, fg="black")
        if (matchready):
            buttons["match_button"].config(state="normal", fg="purple")


### Create matcher variable and start extracting
def create_matcher():
    global ma, matchready, dbpath, querypath, labels, buttons
    ma = Matcher(dbpath)
    matchready = True
    if (querypath != "" and querypath != "(No file selected)"):
        buttons["match_button"].config(state="normal", fg="purple")

def do_match():
    run()

### Initialize frame #0
def init_frame0():
    global methodpick
    new_frame(h=270, w=600)
    new_image(i=0, path="title.png", w=400, h=100, x=1)
    new_button(i=0, txt="Select database directory", cmd=select_db, incy=0)
    new_text(i=0, key="dbpath", txt=dbpath, x=1, bgcolor="white", fgcolor="red")
    new_button(i=0, txt="Select query image", cmd=select_query, incy=0)
    new_text(i=0, key="querypath", txt=querypath, x=1, bgcolor="white", fgcolor="red")
    new_button(i=0, key="extract_button", txt="Extract now", cmd=create_matcher, btnstate="disabled", incy=0)
    new_text(i=0, key="extract_status", txt=progress, x=1, bgcolor="white", fgcolor="gray")
    new_text(i=0, txt="Matching method:", incy=0)
    rbframe = Frame(inner[0])
    rbframe.grid(row=rowg[0], column=1, sticky="nesw")
    methodpick = IntVar()
    methodpick.set(0)
    Radiobutton(rbframe, text="Cosine", variable=methodpick, value=0).grid(row=0,column=0)
    Radiobutton(rbframe, text="Euclidean", variable=methodpick, value=1).grid(row=0,column=1)
    rowg[0] += 1
    new_button(i=0, key="match_button", txt="Match!", cmd=do_match, btnstate="disabled", incy=0)

def init_frame1():
    new_frame(h=600, w=450, scrollbar=True) # frame #1

def init_gui():
    global root
    sizex = 1200
    sizey = 600
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    # Create main frames
    init_frame0()
    init_frame1()

    root.mainloop()

def show_img(path):
    img = imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()


def run():
    new_text(i=1, txt='Query image ==========================================')
    new_image(i=1, path=querypath, w=200, h=200)
    names, match = ma.match(querypath, topn=10, method=methodpick.get())
    new_text(i=1, txt='Result images ========================================')
    for i in range(10):
        # we got cosine distance, less cosine distance between vectors
        # more they similar, thus we subtruct it from 1 to get match value
        new_text(i=1, txt=('Match %.8f' % (1-match[i])))
        # show_img(os.path.join(images_path, names[i]))
        new_image(i=1, path=(os.path.join(dbpath, os.path.basename(names[i]))), w=200, h=200)


init_gui()
