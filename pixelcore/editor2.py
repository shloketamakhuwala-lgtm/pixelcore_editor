import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image

from .engine import PixelGrid


class PixelEditor2:

    def __init__(self, root):

        self.root = root
        self.root.title("PixelCore Editor2")

        self.pixel_size = 8
        self.grid = None
        self.rectangles = None
        self.selected = None

        # -------------------------
        # Top buttons
        # -------------------------

        top = tk.Frame(root)
        top.pack()

        tk.Button(top, text="Open Image", command=self.open_image).pack(side="left")
        tk.Button(top, text="New Canvas", command=self.new_canvas).pack(side="left")
        
        # -------------------------
        # Scrollable canvas
        # -------------------------

        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(frame, bg="white")

        hbar = tk.Scrollbar(frame, orient="horizontal", command=self.canvas.xview)
        vbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        hbar.pack(side="bottom", fill="x")
        vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # -------------------------
        # Info panel
        # -------------------------

        info = tk.Frame(root)
        info.pack()

        self.coord = tk.Label(info, text="Coord:")
        self.coord.pack()

        self.rgb = tk.Entry(info, width=20)
        self.rgb.pack()

        tk.Button(info, text="Apply Pixel", command=self.apply_pixel).pack()

        # -------------------------
        # RGB Sliders
        # -------------------------

        sliders = tk.Frame(root)
        sliders.pack(pady=10)

        self.r_slider = tk.Scale(sliders, from_=0, to=255,
                                 orient="horizontal",
                                 label="Red",
                                 command=self.update_rgb_entry)
        self.r_slider.pack(fill="x")

        self.g_slider = tk.Scale(sliders, from_=0, to=255,
                                 orient="horizontal",
                                 label="Green",
                                 command=self.update_rgb_entry)
        self.g_slider.pack(fill="x")

        self.b_slider = tk.Scale(sliders, from_=0, to=255,
                                 orient="horizontal",
                                 label="Blue",
                                 command=self.update_rgb_entry)
        self.b_slider.pack(fill="x")

    # --------------------------------

    def update_rgb_entry(self, value=None):

        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()

        self.rgb.delete(0, "end")
        self.rgb.insert(0, f"{r},{g},{b}")

    # --------------------------------

    def open_image(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        img = Image.open(path).convert("RGB")

        w, h = img.size

        self.grid = PixelGrid(w, h)
        self.grid.load_image(img)

        self.build_canvas()

    # --------------------------------

    def new_canvas(self):

        size = simpledialog.askinteger("Canvas Size", "Canvas size")

        if not size:
            return

        self.grid = PixelGrid(size, size)

        self.build_canvas()

    # --------------------------------

    def build_canvas(self):

        matrix = self.grid.data()

        h, w, _ = matrix.shape

        width = w * self.pixel_size
        height = h * self.pixel_size

        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, width, height))

        self.rectangles = [[None for _ in range(w)] for _ in range(h)]

        for y in range(h):
            for x in range(w):

                r, g, b = matrix[y, x]

                color = f'#{r:02x}{g:02x}{b:02x}'

                rect = self.canvas.create_rectangle(
                    x*self.pixel_size,
                    y*self.pixel_size,
                    (x+1)*self.pixel_size,
                    (y+1)*self.pixel_size,
                    fill=color,
                    outline="gray"
                )

                self.rectangles[y][x] = rect

        self.canvas.bind("<Button-1>", self.click)

    # --------------------------------

    def click(self, event):

        x = int(self.canvas.canvasx(event.x)) // self.pixel_size
        y = int(self.canvas.canvasy(event.y)) // self.pixel_size

        matrix = self.grid.data()

        h, w, _ = matrix.shape

        if x >= w or y >= h:
            return

        r, g, b = matrix[y, x]

        self.selected = (x, y)

        self.coord.config(text=f"Coord: ({x},{y}) RGB: {r,g,b}")

        self.rgb.delete(0, "end")
        self.rgb.insert(0, f"{r},{g},{b}")

        # update sliders to match pixel
        self.r_slider.set(r)
        self.g_slider.set(g)
        self.b_slider.set(b)

    # --------------------------------

    def apply_pixel(self):

        if self.selected is None:
            return

        try:
            r, g, b = map(int, self.rgb.get().split(","))
        except:
            return

        x, y = self.selected

        self.grid.set_pixel(x, y, (r, g, b))

        color = f'#{r:02x}{g:02x}{b:02x}'

        rect = self.rectangles[y][x]

        self.canvas.itemconfig(rect, fill=color)