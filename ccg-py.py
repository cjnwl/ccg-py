#------------------------------------------------------------------------------------------
# CCG v5.00
# python version, (c) CNE - Jan to Mar 2018
#------------------------------------------------------------------------------------------

"""
+---------------
| CCG todo list
+---------------
- INI (use sqlite ? use options table, defColours, etc)
- MRU
- Status bar : file name (*) | tab, status, grid position
- Title bar : project name (*)
- Import/Export : CS : json, csv/sep, native = db3
- Import/Export Colours : (rgb), (r,g,b), hex, cmyk, hsl
- CS grid : dynamic header row
- Std colours, on colours tab
- Multiple canvases

Project files
- ccg     : main project file
- ccg gui : define the gui
- ccg app : gui behaviour, grids, buttons, etc
- ccg img : canvas drawing routines
- ccg cls : class definitions
- ccg def : function definitions

to-do :
-------
flesh out datagrid params, make it data-aware, master-detail, button(s) functionality
status bar locked to bottom of window
resize, scrollbars
file read/write, open & save
    db3, json, yaml, other ?
mru
import/export
options
    db3, ini, other ?
algorithm
    modify current db3, add element order
shapes
save to bitmap
save to svg
skins ? --> in options
help file, eML, markdown, helpndoc, etc
website, mobirise, wordpress blog, etc
------------------------------------
data-aware
options/ini
read/write/save
mru
algorithm
image save
icon
tutorial
reference
website
print image ?
print manifest
print all tabs
shapes
status bar
resize
"""

from tkinter import Tk
from tkinter import Menu
from tkinter import *
from tkinter import ttk
from tkintertable import TableCanvas, TableModel

class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=SW)
        self.label.pack(side=BOTTOM, fill=X)
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def savebitmap(event, w, canvas_width, canvas_height):
    sb.set("Saving {0}%")
    img = PhotoImage(width = canvas_width, height = canvas_height)
    perc = -1
    for y in range(canvas_height):
        perc1 = (100*y) // canvas_height
        if perc1 != perc:
            perc = perc1
            sb.set(perc)
        row = "{"
        for x in range(canvas_width):
            ids = w.find_overlapping(x, y, x, y)
            color = w.itemcget(ids[-1], "fill") if ids else canvas_background
            row += color + " "
        img.put(row + "}", (0, y))
    img.write("test.ppm", format="ppm")
    sb.set("done")
       
def createcanvas():
    try:
        t1 = Toplevel(app)
        t1.title(" canvas ")
        t1frame = ttk.Labelframe(t1, text = " canvas 2 ")
        t1frame.grid(row = 0, column=0, sticky=(N, W, E, S))
        canvas = Canvas(t1frame, width=600, height=250, bg = 'white')
        canvas.create_polygon(205,105,285,125,166,177,210,199,205,105, outline = 'red', fill='white')
        drawbox(canvas,5,5,30,50, 'red', 'yellow')
        drawline(canvas,5,5,30,50, 'green')
        drawline(canvas,30,5,5,50, 'cyan')
        drawunits(canvas,5, 5, 50, 50, 5,5,30,50, 5)
        canvas.pack()
        t1.geometry('500x400+400+400')
#        t1.lift(aboveThis=app)
        t1.focus_set()
        canvas.update()
#        savebitmap(None, canvas, 600, 250)  --> raises exception
#        canvas.postscript("test.eps", colormode="color")
    except ValueError:
        print("error")

def drawbox(canvas,t,l,b,r,fg,bg):
    try:
        canvas.create_polygon(l,t,r,t,r,b,l,b,l,t,outline = fg,fill=bg)
    except ValueError:
        pass

def drawline(canvas,t,l,b,r,fg):
    try:
        canvas.create_polygon(l,t,r,b,outline=fg)
    except ValueError:
        pass

def drawunits(canvas,vstart, hstart, voffset, hoffset, t,l,b,r, qty):
    try:
        i = 1
        while (i <= qty):
            drawbox(canvas, t,l+i*voffset,b,r+i*hoffset, 'tan', 'beige')
            i = i + 1
    except ValueError:
        pass
        
def createGrid(parent, rows, cols, title, data, headers=None, widths=10, buttons=[["+","plus"],["-","minus"]], disp="h"):
    if buttons == []:
        buttons = [["+","plus"],["-","minus"]]
    """ check for rows, cols = 0 => autorows and cols """
    """ check for widths = 0 => autowidths """
    if not isinstance(widths,(int,list)):
        widths = 10
    outer = ttk.Labelframe(parent, text=title)
    outer.grid(column=0, padx=10, pady=10, row=0, sticky=(N, W, E, S))
    datagrid = ttk.Labelframe(outer,text="grid")
    buttonfr = ttk.Labelframe(outer,text="buttons")
    if disp == "h":
        datagrid.grid(row=0, column=0, padx=10, pady=10, sticky=(N, W, E, S))
        buttonfr.grid(row=0, column=1, padx=10, pady=10, sticky=(N, W, E, S))
    else:
        datagrid.grid(row=0, column=0, padx=10, pady=10, sticky=(N, W, E, S))
        buttonfr.grid(row=1, column=0, padx=10, pady=10, sticky=(N, W, E, S))
    for j in range(cols): #Columns
        if headers == None:
            b = Label(datagrid, text=chr(65+j), bg = "grey80") 
        else:
            b = Label(datagrid, text=headers[j], bg = "grey80")
        b.grid(row=0, column=j, sticky = "news")
    for i in range(1, rows): #Rows
        for j in range(cols): #Columns
            if type(widths) == int:
#            if widths.is_integer():
                b = Entry(datagrid, text="", width=widths)
            else:
                b = Entry(datagrid, text="", width=widths[j])
            b.grid(row=i, column=j)
    r,c = 0,0
    for b in buttons:
        onclick = lambda cmd=b[1]: buttoncmd(cmd)
        ttk.Button(buttonfr, text=b[0], command=onclick).grid(row=r, column=c, padx=1, pady=1, sticky=(N, W, E, S))
        if disp == "h":
            r += 1
        else:
            c += 1
    return outer

def buttoncmd(cmd):
    print(cmd)
    
#------------------------------------------------------------------------------------------

def createMenus(app):
    # Create the submenus (tearoff is if menu can pop out)
    file_menu = Menu(menu_bar, tearoff=1)
    view_menu = Menu(menu_bar, tearoff=1)
    help_menu = Menu(menu_bar, tearoff=1)
    
    # Add commands to submenus
    file_menu.add_command(label="New", command=createcanvas)
    file_menu.add_command(label="Open", command=app.destroy)
    file_menu.add_command(label="Save", command=app.destroy)
    file_menu.add_command(label="Save as...", command=app.destroy)
    file_menu.add_command(label="Save a copy", command=app.destroy)
    file_menu.add_command(label="Recent >", command=app.destroy)
    file_menu.add_command(label="Quit", command=app.destroy)
    
    view_menu.add_command(label="Colours", command=createcanvas)
    view_menu.add_command(label="Options", command=optionScreen)
    
    help_menu.add_command(label="Help", command=app.destroy)
    help_menu.add_command(label="About", command=app.destroy)
    
    # Add the drop down sub-menus in the main menu bar
    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_cascade(label="View", menu=view_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    app.config(menu=menu_bar)

def createWidgets(app):
    # create main screen frame
    mainframe = ttk.Frame(app, padding="3 3 3 3")
    mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    # create tabs
    tabs = ttk.Notebook(mainframe)
    tab1 = ttk.Frame(tabs)
    tab2 = ttk.Frame(tabs)
    tab3 = ttk.Frame(tabs)
    tab4 = ttk.Frame(tabs)
    tab5 = ttk.Frame(tabs)
    tab6 = ttk.Frame(tabs)
    tabs.add(tab1, text=' params ')
    tabs.add(tab2, text=' sizes ')
    tabs.add(tab3, text=' templates ')
    # tabs.add(tab4, text=' colour schemes ')
    tabs.add(tab4, text=' tkintertable ')
    tabs.add(tab5, text=' colours ')
    tabs.add(tab6, text=' counter sheets ')
    # create frame on tab 1
    tab1buttons = [["add","tab1add"], ["del","tab1del"]]
    tab1frame1 = createGrid(tab1, 4, 3, "general", "data", ["AA","BB","CC"], [15,5,10], tab1buttons, "v")
    # create frame on tab 2
    tab2frame1 = createGrid(tab2, 4, 5, "sizes", "data", None, 5, [], "h")
    # create frames on tab 3
    tab3frame1 = createGrid(tab3, 6, 2, "master", "data", None, "widths", [], "v")
    tab3frame1.grid(row=0, column=0, padx=10, pady=10, sticky=(N, W, E, S))
    tab3frame2 = createGrid(tab3, 10, 5, "detail", "data", None, "widths", [], "v")
    tab3frame2.grid(row=0, column=1, padx=10, pady=10, sticky=(N, W, E, S))
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    # create frames on tab 4
    #tab4frame1 = Frame(tab4)
    tab4frame1 = Frame(tab4)
    tab4frame1.pack
    data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
       'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}
       } 
    model = TableModel()
    tab4table1 = TableCanvas(tab4frame1, model=model, data=data,
        cellwidth=100, cellbackgr='#e3f698',
        thefont=('Arial',12),rowheight=25, rowheaderwidth=100,
        rowselectedcolor='yellow', editable=True)
    tab4table1.createTableFrame()
    tab4table1.show
        
def createStatusBar(app):
    sb = StatusBar(app)
    sb.grid(row=1, column=0, sticky=(W, E, S))
    return sb
    
def optionScreen():
    options = Toplevel(app)
    options.title(" options ")
    
    toprow = ttk.Labelframe(options, text = " author ")
    toprow.grid(row=0, column=0, columnspan=2, sticky="news")
    lblAuthor = Label(toprow, text=" Author ")
    lblAuthor.grid(row=0, column=0, sticky = "news")
    cAuthor = StringVar()
    author = Entry(toprow, textvariable=cAuthor)
    author.grid(row=0, column=1, columnspan=3, sticky = "news")
    
    topleft = ttk.Labelframe(options, text = " startup ")
    topleft.grid(row=1, column=0, columnspan=2, sticky="news")
#    tb1 = Tickbox(topleft, text="Save window size and position")
#    tb1.grid(row=0, column=0, columnspan=2, sticky="news")
    
    topright = ttk.Labelframe(options, text = " image folder ")
    topright.grid(row=1, column=0, columnspan=2, sticky="news")
    
    botleft = ttk.Labelframe(options, text = " file ")
    botleft.grid(row=1, column=0, columnspan=2, sticky="news")
    
    botright = ttk.Labelframe(options, text = " output ")
    botright.grid(row=1, column=0, columnspan=2, sticky="news")
    
    return options
    
#------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = Tk()
    app.title(" ccg2.py ")
    app.iconbitmap(default="CCGv5.ico")
    app.geometry('900x600+400+300')
    menu_bar = Menu(app)
    createMenus(app)
    app.config(menu=menu_bar)
    createWidgets(app)
    sb = createStatusBar(app)
    sb.set(" CCG status bar ")
    
    ttk.Style().configure("TButton", padding=0, relief="flat", background="#fff")
#    btn = ttk.Button(text="Sample")
#    btn.pack()
    
    
    app.mainloop()
 
#------------------------------------------------------------------------------------------
# eof
#------------------------------------------------------------------------------------------
