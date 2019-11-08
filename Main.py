#==-- IMPORTS --==#
import cv2
import numpy as np
from cv2 import imread
import random
import os
import matplotlib.pyplot as plt
from Matcher import Matcher
from GUI import *
from tkinter import filedialog

#==-- TKINTER GUI --==#
global methodpick


### Make new frame, including it's canvas and inner frame
def new_frame(h, w=500, scrollbar=False, orientv="vertical", sidev="right", fillv="y", movex=True):
    global outer, canvas, inner, scrolly, frameposx, frameposy, width_temp, height_temp
    width_temp = w
    height_temp = h
    #
    outer.append(Frame(root,relief=GROOVE,width=w,height=h,bd=1))
    outer[-1].place(x=frameposx,y=frameposy)
    if(movex):
        frameposx += (w+15)
    canvas.append(Canvas(outer[-1]))
    inner.append(Frame(canvas[-1]))
    #
    if(scrollbar):
        if(fillv == "y"):
            scrolly.append(Scrollbar(outer[-1],orient=orientv,command=canvas[-1].yview))
            canvas[-1].configure(yscrollcommand=scrolly[-1].set)
        else:
            scrolly.append(Scrollbar(outer[-1],orient=orientv,command=canvas[-1].xview))
            canvas[-1].configure(xscrollcommand=scrolly[-1].set)
        scrolly[-1].pack(side=sidev,fill=fillv)
    #
    canvas[-1].pack(side="left")
    canvas[-1].create_window((0,0),window=inner[-1],anchor='nw')
    inner[-1].bind("<Configure>",conf_frame)

### Configure scrollbar for canvas
def conf_frame(event):
    global width_temp, height_temp
    canvas[-1].configure(scrollregion=canvas[-1].bbox("all"),width=width_temp,height=height_temp)

### New text label
def new_text(i, txt, key=str(defkey), incy=1, y="default", x=0, bgcolor="SystemMenu", fgcolor="black", formatting="TkDefaultFont"):
    global rowg, defkey, labels
    if(y == "default"):
        y = rowg[i]
    #
    labels[key] = Label(inner[i], text=txt, bg=bgcolor, fg=fgcolor, font=formatting)
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
    Label(inner[i], image=img[-1]).grid(row=y, column=x, sticky='ew')
    root.update()
    rowg[i] += incy

### New button
def new_button(i, txt, cmd, key=str(defkey), btnstate="normal", incy=1, y="default", x=0, formatting="TkDefaultFont"):
    global rowg, defkey, buttons
    if(y == "default"):
        y = rowg[i]
    #
    buttons[key] = Button(inner[i], text=txt, command=cmd, state=btnstate, font=formatting)
    buttons[key].grid(row=y, column=x, sticky='ew', padx=2, pady=2)
    root.update()
    rowg[i] += incy
    defkey += 1

### Select directory from PC
def select_db():
    global dbpath, querypath, labels, buttons, matchready, tops
    dbpath = filedialog.askdirectory(initialdir=" ", title="Select Database Directory...")
    if (dbpath != ""):
        labels["dbpath"].config(text=shorten_path(dbpath), fg="black")
        buttons["extract_button"].config(state="normal", fg="green")
        topto = len(next(os.walk(dbpath))[2])
        if (topto > 20):
            topto = 20
        tops.config(state="normal", to=topto)

### Select file from PC
def select_query():
    global dbpath, querypath, labels, matchready
    querypath = filedialog.askopenfilename(initialdir=" ", title="Select Query JPG...", filetypes = (("JPEG files", "*.jpg"), ("All files", "*.*")))
    if (querypath != ""):
        labels["querypath"].config(text=shorten_path(querypath), fg="black")
        if (matchready):
            buttons["match_button"].config(state="normal", fg="purple")

### Create matcher variable and start extracting
def create_matcher():
    global ma, matchready, dbpath, querypath, labels, buttons, extractpick
    expick = extractpick.get()
    if (expick == "Extract from files"):
        ma = Matcher(dbpath, expick)
    else:
        pckpath = filedialog.askopenfilename(initialdir=" ", title="Select Pickle File...", filetypes = (("Pickle files", "*.pck"), ("All files", "*.*")))
        if(pckpath != ""):
            ma = Matcher(dbpath, expick, pckpath)
    matchready = True
    if (querypath != "" and querypath != "(No file selected)"):
        buttons["match_button"].config(state="normal", fg="purple")
    buttons["save_pickle"].config(state="normal")

def save_pickle():
    global ma
    pckpath = filedialog.asksaveasfilename(initialdir=" ", initialfile="features.pck", title="Save as Pickle File...", filetypes = (("Pickle files", "*.pck"), ("All files", "*.*")))
    if (pckpath != ""):
        ma.save(pckpath)

def do_match():
    run()

framesp = [PhotoImage(file='Pendahulu.gif',format = 'gif -index %i' %(i)) for i in range(3)]
framesa = [PhotoImage(file='About.gif',format = 'gif -index %i' %(i)) for i in range(3)]

def update(ind):
    frp = framesp[ind]
    fra = framesa[ind]
    ind = (ind+1)%3
    titlep.configure(image=frp)
    titlea.configure(image=fra)
    root.after(100, update, ind)

### Initialize frame #0
def init_frame0():
    global methodpick, extractpick, topof, tops, titlep, titlea
    new_frame(h=360, w=770)# scrollbar=True, orientv="horizontal", sidev="bottom", fillv="x")
    titlea = Label(inner[0])
    titlea.grid(row=0, column=0)
    titlep = Label(inner[0])
    titlep.grid(row=0, column=1)
    root.after(0, update, 0)
    rowg[0] += 1
    new_button(i=0, txt="Select database directory", cmd=select_db, incy=0)
    new_text(i=0, key="dbpath", txt=dbpath, x=1, bgcolor="white", fgcolor="red")
    exframe = Frame(inner[0])
    exframe.grid(row=rowg[0], column=0, sticky="nesw")
    extractpick = StringVar()
    extractpick.set("Extract from files")
    om = OptionMenu(exframe, extractpick, "Extract from files", "Load from pickle")
    om.configure(width=20)
    om.grid(row=0, column=0, sticky="nesw")
    buttons["extract_button"] = Button(exframe, text="❯❯", command=create_matcher)
    buttons["extract_button"].grid(row=0, column=1, sticky="nsew")
    buttons["extract_button"].config(state="disabled")
    new_text(i=0, key="extract_status", txt=progress, x=1, bgcolor="white", fgcolor="gray", incy=0)
    new_button(i=0, key="save_pickle", txt="Save to pickle", x=2, cmd=save_pickle, btnstate="disabled")
    new_button(i=0, txt="Select query image", cmd=select_query, incy=0)
    new_text(i=0, key="querypath", txt=querypath, x=1, bgcolor="white", fgcolor="red")
    new_text(i=0, txt="Matching method:", incy=0)
    rbframe = Frame(inner[0])
    rbframe.grid(row=rowg[0], column=1, sticky="nesw")
    methodpick = IntVar()
    methodpick.set(0)
    Radiobutton(rbframe, text="Cosine", variable=methodpick, value=0).grid(row=0,column=0)
    Radiobutton(rbframe, text="Euclidean", variable=methodpick, value=1).grid(row=0,column=1)
    rowg[0] += 1
    new_text(i=0, txt="Show Results Top of:", incy=0)
    topof = IntVar()
    topof.set(1)
    tops = Scale(inner[0], variable=topof, state="disabled", orient=HORIZONTAL, from_=1, to=1)
    tops.grid(row=rowg[0], column=1, sticky="ew")
    rowg[0] += 1
    new_button(i=0, key="match_button", txt="Match!", cmd=do_match, btnstate="disabled")
    new_button(i=0, key="clear_results", txt="Clear results", cmd=clear_frame1)

def init_frame1():
    new_frame(h=550, w=220, scrollbar=True, movex=False) # frame #1

def clear_frame1():
    global inner, root
    inner[-1].destroy()
    canvas[-1].destroy()
    outer[-1].destroy()
    init_frame1()
    root.update()

def init_gui():
    global root
    sizex = 1240
    sizey = 600
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.title("Pendahulu: Image Processing")
    # Create main frames
    init_frame0()
    init_frame1()

    root.mainloop()

def show_img(path):
    img = imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()

def shorten_path(path):
    if len(path) > 40:
        return (os.path.splitdrive(path))[0]+"/.../"+os.path.basename(path)
    else:
        return path
    # return path

def run():
    global topof
    topget = topof.get()
    new_text(i=-1, txt='Query image', formatting="Consolas 13 bold", fgcolor="cyan", bgcolor="black")
    new_text(i=-1, txt=(os.path.splitext(os.path.basename(querypath))[0]), formatting="Consolas 10 bold", bgcolor="black", fgcolor="white")
    new_image(i=-1, path=querypath, w=200, h=200)
    names, match = ma.match(querypath, topn=topget, method=methodpick.get())
    new_text(i=-1, txt='Result images', formatting="Consolas 12 bold", fgcolor="white", bgcolor="black")
    for j in range(topget):
        # we got cosine distance, less cosine distance between vectors
        # more they similar, thus we subtruct it from 1 to get match value
        if(methodpick.get()==0):
            new_text(i=-1, txt=('#%d Match %.8f' % (j+1, (1-match[j]))), formatting="Consolas 9", bgcolor="yellow")
            new_text(i=-1, txt=(os.path.splitext(os.path.basename(names[j]))[0]), formatting="Consolas 8", bgcolor="yellow")
        else:
            new_text(i=-1, txt=('#%d Match %.8f' % (j+1, (1-match[j]/2))), formatting="Consolas 9", bgcolor="yellow")
        new_image(i=-1, path=(os.path.join(dbpath, os.path.basename(names[j]))), w=160, h=160)


init_gui()
