import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image

from .engine import PixelGrid


class PixelEditor:

    def __init__(self,root):

        self.root = root
        self.root.title("PixelCore Editor")

        self.pixel_size = 8
        self.grid = None
        self.selected_pixel = None
        self.rect_grid = None

        top = tk.Frame(root)
        top.pack()

        tk.Button(top,text="Open Image",command=self.open_image).pack(side="left")
        tk.Button(top,text="New Canvas",command=self.new_canvas).pack(side="left")
        
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(fill="both",expand=True)

        self.canvas = tk.Canvas(canvas_frame,bg="white")

        hbar = tk.Scrollbar(canvas_frame,orient="horizontal",command=self.canvas.xview)
        vbar = tk.Scrollbar(canvas_frame,orient="vertical",command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=hbar.set,yscrollcommand=vbar.set)

        hbar.pack(side="bottom",fill="x")
        vbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)

        info = tk.Frame(root)
        info.pack()

        self.coord_label = tk.Label(info,text="Coord:")
        self.coord_label.pack()

        self.rgb_entry = tk.Entry(info,width=20)
        self.rgb_entry.pack()

        tk.Button(info,text="Apply Pixel",command=self.update_pixel).pack()

    # ---------------------

    def open_image(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        img = Image.open(path).convert("RGB")

        w,h = img.size

        self.grid = PixelGrid(w,h)
        self.grid.load_image(img)

        self.draw_image()

    # ---------------------

    def new_canvas(self):

        size = simpledialog.askinteger("Canvas Size","Enter canvas size")

        if not size:
            return

        self.grid = PixelGrid(size,size)

        self.draw_image()

    # ---------------------

    def draw_image(self):

        if self.grid is None:
            return

        matrix = self.grid.data()

        h,w,_ = matrix.shape

        width = w*self.pixel_size
        height = h*self.pixel_size

        self.canvas.config(scrollregion=(0,0,width,height))
        self.canvas.delete("all")

        self.rect_grid = [[None for _ in range(w)] for _ in range(h)]

        for y in range(h):
            for x in range(w):

                r,g,b = matrix[y,x]

                color = f'#{r:02x}{g:02x}{b:02x}'

                rect = self.canvas.create_rectangle(
                    x*self.pixel_size,
                    y*self.pixel_size,
                    (x+1)*self.pixel_size,
                    (y+1)*self.pixel_size,
                    fill=color,
                    outline="gray"
                )

                self.rect_grid[y][x] = rect

        self.canvas.bind("<Button-1>",self.click_pixel)

    # ---------------------

    def click_pixel(self,event):

        x = int(self.canvas.canvasx(event.x)) // self.pixel_size
        y = int(self.canvas.canvasy(event.y)) // self.pixel_size

        matrix = self.grid.data()

        h,w,_ = matrix.shape

        if x>=w or y>=h:
            return

        r,g,b = matrix[y,x]

        self.selected_pixel = (x,y)

        self.coord_label.config(text=f"Coord: ({x},{y}) RGB: {r,g,b}")

        self.rgb_entry.delete(0,"end")
        self.rgb_entry.insert(0,f"{r},{g},{b}")

    # ---------------------

    def update_pixel(self):

        if self.selected_pixel is None:
            return

        try:
            r,g,b = map(int,self.rgb_entry.get().split(","))
        except:
            return

        x,y = self.selected_pixel

        self.grid.set_pixel(x,y,(r,g,b))

        color = f'#{r:02x}{g:02x}{b:02x}'

        rect = self.rect_grid[y][x]

        self.canvas.itemconfig(rect,fill=color)
