import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set window size to 40% of screen size
        window_width = int(0.4 * screen_width)
        window_height = int(0.4 * screen_height)

        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Configure styling
        self.root.configure(bg="#f0f0f0")
        self.button_bg = "#4CAF50"
        self.button_fg = "#FFFFFF"

        self.img = None
        self.processed_img = None

        # Create Frame for buttons
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        # Create open image button
        self.btn_open = tk.Button(self.button_frame, text="Open Image", command=self.open_image, bg=self.button_bg, fg=self.button_fg)
        self.btn_open.grid(row=0, column=0, padx=5, pady=5)

        # Create buttons for image processing operations
        operations = [
            ("Convert to Gray", self.convert_to_gray),
            ("Select ROI", self.select_roi),
            ("Logarithmic", self.Logarithmic),
            ("Histogram Processing", self.histogram_processing),
            ("Gaussian Noise", self.gaussian_noise),
            ("Salt & Pepper Noise", self.salt_pepper_noise),
            ("Median Filter", self.median_filter),
            ("Max Filter", self.max_filter),
            ("Min Filter", self.min_filter),
            ("Midpoint Filter", self.midpoint_filter) 
        ]

        for i, (text, command) in enumerate(operations):
            button = tk.Button(self.button_frame, text=text, command=command, bg=self.button_bg, fg=self.button_fg, width=15, height=2)
            button.grid(row=i // 3, column=i % 3 + 1, padx=5, pady=5)
    def display(self,img):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(img)
            self.imgtk = ImageTk.PhotoImage(image=im)
            self.labelTop.configure(image=self.imgtk)
            self.labelTop.pack()
            
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = cv2.imread(file_path)
            self.newWindow = tk.Toplevel(self.root)
            self.newWindow.geometry("1500x1000")
            self.labelTop= tk.Label(self.newWindow)
            self.display(self.img)
            # Enable buttons after image selection
            for child in self.button_frame.winfo_children():
                child.config(state=tk.NORMAL)

    def convert_to_gray(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return
        grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.display(grayImg)

    def select_roi(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return
        roi = self.img[50:150, 50:150]
        self.display(roi) 
    def Logarithmic(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return
	    # Logarithmic transformation
        c = 255 / np.log1p(255)  # Scaling constant
        log_img = c * np.log1p(self.img.astype(np.float32))
        log_img = np.clip(log_img, 0, 255).astype(np.uint8)  # Clip values to [0, 255]
        self.display(log_img)
    def histogram_processing(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return
        gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        equalized_img = cv2.equalizeHist(gray_img)
        self.display(equalized_img)
        

    def gaussian_noise(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        height, width, _ = self.img.shape
        noise = np.random.randn(height, width, 3) * 25
        noisy_img = np.clip(self.img + noise, 0, 255).astype(np.uint8)
        self.display(noisy_img)
    
    def salt_pepper_noise(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        height, width, _ = self.img.shape
        noise = np.random.rand(height, width)
        salt = noise > 0.98
        pepper = noise < 0.02

        noisy_img = self.img.copy()
        noisy_img[salt] = 255
        noisy_img[pepper] = 0
        self.display(noisy_img)


    def median_filter(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        median_filtered_img = cv2.medianBlur(self.img, 5)
        self.display(median_filtered_img)

    def max_filter(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        max_filtered_img = cv2.dilate(self.img, None, iterations=1)
        self.display(max_filtered_img)

    def min_filter(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        min_filtered_img = cv2.erode(self.img, None, iterations=1)
        self.display(min_filtered_img)

    def midpoint_filter(self):
        if self.img is None:
            messagebox.showerror("Error", "Please open an image first.")
            return

        max_filtered_img = cv2.dilate(self.img, None, iterations=1)
        min_filtered_img = cv2.erode(self.img, None, iterations=1)
        midpoint_filtered_img = cv2.addWeighted(min_filtered_img, 0.5, max_filtered_img, 0.5, 0)
        self.display(midpoint_filtered_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
