import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os


def apply_opacity(image, opacity):
    alpha = image.split()[3]
    alpha = alpha.point(lambda p: p * opacity)
    image.putalpha(alpha)
    return image


def apply_tile_watermark(base, watermark):
    base_width, base_height = base.size
    wm_width, wm_height = watermark.size

    wm_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))

    for x in range(0, base_width, wm_width):
        for y in range(0, base_height, wm_height):
            wm_layer.paste(watermark, (x, y), watermark)

    return Image.alpha_composite(base, wm_layer)


def apply_positioned_watermark(base, watermark, position):
    base_width, base_height = base.size
    wm_width, wm_height = watermark.size

    if position == "center":
        x = (base_width - wm_width) // 2
        y = (base_height - wm_height) // 2
    elif position == "top-left":
        x, y = 10, 10
    elif position == "top-right":
        x = base_width - wm_width - 10
        y = 10
    elif position == "bottom-left":
        x = 10
        y = base_height - wm_height - 10
    elif position == "bottom-right":
        x = base_width - wm_width - 10
        y = base_height - wm_height - 10
    else:
        x, y = 0, 0

    wm_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    wm_layer.paste(watermark, (x, y), watermark)

    return Image.alpha_composite(base, wm_layer)


class WatermarkApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.geometry("900x900")

        self.base = None
        self.mark = None
        self.result = None
        self.canvas = None
        self.info_label = None

        self.opacity = tk.DoubleVar(value=0.3)
        self.scale = tk.DoubleVar(value=0.2)
        self.position = tk.StringVar(value="center")

        self.setup_ui()

    def setup_ui(self):

        style=ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        label_main_image = ttk.Label(main_frame, text="Main image", font=("Arial", 10, "bold"))
        label_main_image.grid(column=0, row=0, columnspan=2, pady=5, sticky=tk.W)

        button_main_image = ttk.Button(main_frame, text="Load main image", command=self.load_main_image)
        button_main_image.grid(column=0, row=1, columnspan=2, pady=5, sticky=tk.W+tk.E)

        label_watermark_image = ttk.Label(main_frame, text="Watermark image", font=("Arial", 10, "bold"))
        label_watermark_image.grid(column=0, row=2, columnspan=2, pady=5, sticky=tk.W)

        button_watermark_image = ttk.Button(main_frame, text="Load watermark image", command=self.load_watermark_image)
        button_watermark_image.grid(column=0, row=3, columnspan=2, pady=5, sticky=tk.W + tk.E)

        label_settings = ttk.Label(main_frame, text="Settings", font=("Arial", 10, "bold"))
        label_settings.grid(column=0, row=4, columnspan=2, pady=5, sticky=tk.W)

        label_opacity = ttk.Label(main_frame, text="Opacity:")
        label_opacity.grid(column=0, row=5, sticky=tk.W, pady=5)

        opacity_scale = ttk.Scale(main_frame, from_=0.1, to=1.0, variable=self.opacity,
                                  orient=tk.HORIZONTAL, command=self.update_preview)
        opacity_scale.grid(column=1, row=5,  sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        label_opacity_value = ttk.Label(main_frame, textvariable=lambda: f"{self.opacity.get():.1f}")
        label_opacity_value.grid(column=2, row=5, padx=(5, 0))

        label_scale = ttk.Label(main_frame, text="Scale:")
        label_scale.grid(column=0, row=6, sticky=tk.W, pady=5)

        scale = ttk.Scale(main_frame, from_=0.1, to=1.0, variable=self.scale,
                                  orient=tk.HORIZONTAL, command=self.update_preview)
        scale.grid(column=1, row=6, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        label_scale_value = ttk.Label(main_frame, textvariable=lambda: f"{self.scale.get():.1f}")
        label_scale_value.grid(column=2, row=6, padx=(5, 0))

        label_pos = ttk.Label(main_frame, text="Position:")
        label_pos.grid(row=7, column=0, sticky=tk.W, pady=5)
        position_combo = ttk.Combobox(main_frame, textvariable=self.position,
                                      values=["center", "top-left", "top-right",
                                              "bottom-left", "bottom-right", "tile"])
        position_combo.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        position_combo.bind('<<ComboboxSelected>>', self.update_preview)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=(20, 10))

        ttk.Button(button_frame, text="Apply watermark",
                   command=self.apply_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save result",
                   command=self.save_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset",
                   command=self.reset_all).pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Preview:", font=('Arial', 10, 'bold')).grid(row=9, column=0, columnspan=3,
                                                                                     pady=(20, 10), sticky=tk.W)

        self.canvas = tk.Canvas(main_frame, bg='lightgray', width=600, height=400)
        self.canvas.grid(row=10, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        self.info_label = ttk.Label(main_frame, text="Please load image")
        self.info_label.grid(row=11, column=0, columnspan=3, pady=(10, 0))

    def load_main_image(self):
        file_path = filedialog.askopenfilename(
            title="Select main image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.base = Image.open(file_path).convert("RGBA")
                self.update_info(
                    f"Main image: {os.path.basename(file_path)} ({self.base.size[0]}x{self.base.size[1]})")
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Image can not be loaded: {str(e)}")

    def load_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select watermark image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.mark = Image.open(file_path).convert("RGBA")
                self.update_info(
                    f"Watermark image: {os.path.basename(file_path)} ({self.base.size[0]}x{self.base.size[1]})")
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Image can not be loaded: {str(e)}")

    def apply_watermark(self):
        if not self.base or not self.mark:
            messagebox.showwarning("Warning", "Please load both images!")
            return

        try:
            base = self.base.copy()
            watermark = self.mark.copy()

            new_size = (int(watermark.size[0] * self.scale.get()),
                        int(watermark.size[1] * self.scale.get()))
            watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)

            watermark = apply_opacity(watermark, self.opacity.get())

            if self.position.get() == "tile":
                self.result = apply_tile_watermark(base, watermark)
            else:
                self.result = apply_positioned_watermark(base, watermark, self.position.get())

            self.update_preview()
            self.update_info("Watermark applied successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Watermark can not be applied: {str(e)}")

    def save_result(self):
        if not self.result:
            messagebox.showwarning("Warning", "Firstly apply watermark.")
            return

        file_path=filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save result"
        )

        if file_path:
            try:
                if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
                    self.result.convert("RGB").save(file_path)
                else:
                    self.result.save(file_path)

                messagebox.showinfo("Success", "New image was saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Image can not be saved: {str(e)}")

    def reset_all(self):
        self.base = None
        self.mark = None
        self.result = None
        self.opacity.set(0.5)
        self.scale.set(0.3)
        self.position.set("center")
        self.update_info("Please load image.")
        self.update_preview()

    def update_preview(self, *args):
        if self.result:
            display_image = self.result
        elif self.base:
            display_image = self.base
        else:
            self.canvas.delete("all")
            self.canvas.create_text(450, 200, text="Please load image",
                                    font=('Arial', 16), fill='gray')
            return

        canvas_width = self.canvas.winfo_width() or 600
        canvas_height = self.canvas.winfo_height() or 400

        img_width, img_height = display_image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height, 1)
        new_size = (int(img_width * ratio), int(img_height * ratio))

        resized_img = display_image.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img.convert("RGB"))

        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2,
                                 image=photo, anchor=tk.CENTER)
        self.canvas.image = photo

    def update_info(self, text):
        self.info_label.config(text=text)