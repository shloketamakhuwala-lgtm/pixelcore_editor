import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

from .engine import PixelGrid


class PixelEditor3:

    def __init__(self, root):

        self.root = root
        self.root.title("PixelCore Editor3")

        self.grid = None
        self.tk_image = None
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

        canvas_frame = tk.Frame(root)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="white")

        vbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        hbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(
            yscrollcommand=vbar.set,
            xscrollcommand=hbar.set
        )

        vbar.pack(side="right", fill="y")
        hbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # mouse click binding
        self.canvas.bind("<Button-1>", self.click)

        # mouse wheel scroll
        self.canvas.bind("<MouseWheel>", self.scroll_y)

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
        # RGB sliders
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

    # -------------------------
    # Scroll with mouse wheel
    # -------------------------

    def scroll_y(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # -------------------------
    # Update RGB entry from sliders
    # -------------------------

    def update_rgb_entry(self, value=None):

        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()

        self.rgb.delete(0, "end")
        self.rgb.insert(0, f"{r},{g},{b}")

    # -------------------------
    # Open image
    # -------------------------

    def open_image(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        img = Image.open(path).convert("RGB")

        w, h = img.size

        self.grid = PixelGrid(w, h)
        self.grid.load_image(img)

        self.render()

    # -------------------------
    # New canvas
    # -------------------------

    def new_canvas(self):

        size = simpledialog.askinteger("Canvas Size", "Canvas size")

        if not size:
            return

        self.grid = PixelGrid(size, size)

        self.render()

    # -------------------------
    # Render image
    # -------------------------

    def render(self):

        matrix = self.grid.data()

        img = Image.fromarray(matrix)

        self.tk_image = ImageTk.PhotoImage(img)

        self.canvas.delete("all")

        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.canvas.config(scrollregion=(0, 0, img.width, img.height))

    # -------------------------
    # Click pixel
    # -------------------------

    def click(self, event):

        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))

        matrix = self.grid.data()

        h, w, _ = matrix.shape

        if x >= w or y >= h:
            return

        r, g, b = matrix[y, x]

        self.selected = (x, y)

        self.coord.config(text=f"Coord: ({x},{y}) RGB: {r,g,b}")

        self.rgb.delete(0, "end")
        self.rgb.insert(0, f"{r},{g},{b}")

        self.r_slider.set(r)
        self.g_slider.set(g)
        self.b_slider.set(b)

    # -------------------------
    # Apply pixel color
    # -------------------------

    def apply_pixel(self):

        if self.selected is None:
            return

        try:
            r, g, b = map(int, self.rgb.get().split(","))
        except:
            return

        x, y = self.selected

        self.grid.set_pixel(x, y, (r, g, b))

        self.render()