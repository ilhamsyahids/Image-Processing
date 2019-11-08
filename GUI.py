from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

### Global variables
global rowg, outer, canvas, inner, scrolly, labels, buttons, defkey, img, dbpath, querypath, pckpath, topof, frameposx, frameposy, matchready, progess
rowg = [0, 0]
outer = []
canvas = []
inner = []
scrolly = []
labels = {}
buttons = {}
defkey = 0
img = []
dbpath = "(No path selected)"
querypath = "(No file selected)"
pckpath = ""
frameposx = 10
frameposy = 10
matchready = False
progress = "Not extracted yet"

root = Tk()
