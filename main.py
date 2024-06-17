import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Image Processing App")
        
        self.image = None
        self.processed_image = None
        self.current_image = None
        self.roi_start = None
        self.roi_end = None
        self.roi_rect = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)
        
        self.process_button = tk.Button(self.root, text="Process Image", command=self.process_image, state=tk.DISABLED)
        self.process_button.pack(pady=5)
        
        self.save_button = tk.Button(self.root, text="Save Processed Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=5)
        
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_display)
        self.clear_button.pack(pady=5)
        
        self.zoom_label = tk.Label(self.root, text="Zoom:")
        self.zoom_label.pack()
        
        self.zoom_scale = tk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, resolution=0.1, command=self.update_zoom, state=tk.DISABLED)
        self.zoom_scale.pack()
        
        self.original_label = tk.Label(self.root, text="Original Image")
        self.original_label.pack()
        
        self.processed_label = tk.Label(self.root, text="Processed Image")
        self.processed_label.pack()
        
        self.histogram_button = tk.Button(self.root, text="Show Histogram", command=self.show_histogram, state=tk.DISABLED)
        self.histogram_button.pack(pady=5)
        
        self.histogram_label = tk.Label(self.root)
        self.histogram_label.pack()
        
        self.real_time_var = tk.IntVar()
        self.real_time_checkbox = tk.Checkbutton(self.root, text="Real-Time Processing", variable=self.real_time_var, command=self.toggle_real_time, state=tk.DISABLED)
        self.real_time_checkbox.pack(pady=5)
        
        self.blur_label = tk.Label(self.root, text="Gaussian Blur Kernel Size:")
        self.blur_label.pack()
        self.blur_scale = tk.Scale(self.root, from_=1, to=15, orient=tk.HORIZONTAL, command=None)
        self.blur_scale.set(5)
        self.blur_scale.pack()
        
        self.canny_threshold_label = tk.Label(self.root, text="Canny Edge Detection Thresholds:")
        self.canny_threshold_label.pack()
        self.canny_low_scale = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=None)
        self.canny_low_scale.set(30)
        self.canny_low_scale.pack()
        self.canny_high_scale = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=None)
        self.canny_high_scale.set(150)
        self.canny_high_scale.pack()
        
        self.threshold_label = tk.Label(self.root, text="Segmentation Threshold:")
        self.threshold_label.pack()
        self.threshold_scale = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=None)
        self.threshold_scale.set(127)
        self.threshold_scale.pack()
        
        self.create_menu()
        self.create_toolbar()
        
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load Image", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Save Processed Image", command=self.save_image, state=tk.DISABLED)
        file_menu.add_command(label="Save ROI Image", command=self.save_roi_image, state=tk.DISABLED)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Batch Processing", command=self.create_batch_processing_window)
        tools_menu.add_separator()
        tools_menu.add_command(label="About", command=self.about_dialog)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        
        self.root.config(menu=menu_bar)
    
    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        
        load_button = tk.Button(toolbar, text="Load", command=self.load_image)
        load_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.save_button_toolbar = tk.Button(toolbar, text="Save", command=self.save_image, state=tk.DISABLED)
        self.save_button_toolbar.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.save_roi_button = tk.Button(toolbar, text="Save ROI", command=self.save_roi_image, state=tk.DISABLED)
        self.save_roi_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        clear_button = tk.Button(toolbar, text="Clear", command=self.clear_display)
        clear_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.current_image = self.image.copy()
            self.display_original_image()
            self.process_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.DISABLED)
            self.save_button_toolbar.config(state=tk.DISABLED)
            self.histogram_button.config(state=tk.NORMAL)
            self.real_time_checkbox.config(state=tk.NORMAL)
            self.zoom_scale.config(state=tk.NORMAL)
            self.update_histogram()
            self.clear_roi_selection()
            self.reset_parameters()
            cv2.namedWindow("Image")
            cv2.setMouseCallback("Image", self.roi_selection_callback)
    
    def display_original_image(self):
        self.display_image(self.current_image, self.original_label)
    
    def display_processed_image(self, processed_image):
        self.display_image(processed_image, self.processed_label)
    
    def display_image(self, image, label):
        for child in label.winfo_children():
            child.destroy()
        
        img = Image.fromarray(image)
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(label, image=img)
        panel.image = img
        panel.pack()
    
    def process_image(self, *_):
        if self.image is not None:
            blur_kernel_size = self.blur_scale.get()
            if blur_kernel_size % 2 == 0:
                blur_kernel_size += 1
            blurred_image = cv2.GaussianBlur(self.image, (blur_kernel_size, blur_kernel_size), 0)
            
            canny_low_threshold = self.canny_low_scale.get()
            canny_high_threshold = self.canny_high_scale.get()
            edges = cv2.Canny(blurred_image, canny_low_threshold, canny_high_threshold)
            
            threshold_value = self.threshold_scale.get()
            _, segmented_image = cv2.threshold(blurred_image, threshold_value, 255, cv2.THRESH_BINARY)
            
            self.display_processed_image(segmented_image)
            
            self.processed_image = segmented_image
            self.save_button.config(state=tk.NORMAL)
            self.save_button_toolbar.config(state=tk.NORMAL)
            self.update_histogram()
    
    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                try:
                    cv2.imwrite(file_path, self.processed_image)
                    messagebox.showinfo("Success", "Image saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving image: {str(e)}")
    
    def clear_display(self):
        for child in self.original_label.winfo_children():
            child.destroy()
        for child in self.processed_label.winfo_children():
            child.destroy()
        
        self.image = None
        self.processed_image = None
        self.current_image = None
        self.process_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.save_button_toolbar.config(state=tk.DISABLED)
        self.histogram_button.config(state=tk.DISABLED)
        self.real_time_checkbox.config(state=tk.DISABLED)
        self.zoom_scale.config(state=tk.DISABLED)
        self.clear_roi_selection()
        self.reset_parameters()
    
    def update_zoom(self, value):
        if self.current_image is not None:
            zoom_factor = float(value)
            height, width = self.current_image.shape[:2]
            zoomed_image = cv2.resize(self.current_image, (int(width * zoom_factor), int(height * zoom_factor)))
            self.display_image(zoomed_image, self.original_label)
    
    def show_histogram(self):
        if self.image is not None:
            plt.figure("Histogram")
            plt.hist(self.image.ravel(), bins=256, range=[0, 256])
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.show()
    
    def update_histogram(self):
        if self.image is not None:
            self.histogram_label.config(text=f"Histogram: Mean={np.mean(self.image):.2f}, Std={np.std(self.image):.2f}")
    
    def toggle_real_time(self):
        if self.real_time_var.get():
            self.blur_scale.config(command=self.process_image)
            self.canny_low_scale.config(command=self.process_image)
            self.canny_high_scale.config(command=self.process_image)
            self.threshold_scale.config(command=self.process_image)
        else:
            self.blur_scale.config(command=None)
            self.canny_low_scale.config(command=None)
            self.canny_high_scale.config(command=None)
            self.threshold_scale.config(command=None)
    
    def reset_parameters(self):
        self.blur_scale.set(5)
        self.canny_low_scale.set(30)
        self.canny_high_scale.set(150)
        self.threshold_scale.set(127)
    
    def save_roi_image(self):
        if self.current_image is not None and self.roi_rect:
            x, y, w, h = self.roi_rect
            roi_image = self.current_image[y:y+h, x:x+w]
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                try:
                    cv2.imwrite(file_path, roi_image)
                    messagebox.showinfo("Success", "ROI image saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving ROI image: {str(e)}")
    
    def roi_selection_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_start = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.roi_end = (x, y)
            self.roi_rect = (self.roi_start[0], self.roi_start[1], self.roi_end[0] - self.roi_start[0], self.roi_end[1] - self.roi_start[1])
            cv2.rectangle(self.current_image, self.roi_start, self.roi_end, (255, 0, 0), 2)
            self.display_original_image()
            self.save_roi_button.config(state=tk.NORMAL)
    
    def clear_roi_selection(self):
        self.roi_start = None
        self.roi_end = None
        self.roi_rect = None
        self.save_roi_button.config(state=tk.DISABLED)
    
    def create_batch_processing_window(self):
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Processing")
        
        select_folder_button = tk.Button(batch_window, text="Select Folder", command=self.select_batch_folder)
        select_folder_button.pack(pady=10)
        
        self.batch_folder_label = tk.Label(batch_window, text="")
        self.batch_folder_label.pack()
        
        process_batch_button = tk.Button(batch_window, text="Process Batch", command=self.process_batch)
        process_batch_button.pack(pady=10)
    
    def select_batch_folder(self):
        self.batch_folder = filedialog.askdirectory()
        if self.batch_folder:
            self.batch_folder_label.config(text=f"Selected Folder: {self.batch_folder}")
    
    def process_batch(self):
        if self.batch_folder:
            for filename in os.listdir(self.batch_folder):
                file_path = os.path.join(self.batch_folder, filename)
                image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    self.image = image
                    self.process_image()
                    save_path = os.path.join(self.batch_folder, f"processed_{filename}")
                    cv2.imwrite(save_path, self.processed_image)
            messagebox.showinfo("Success", "Batch processing completed.")
    
    def about_dialog(self):
        messagebox.showinfo("About", "Medical Image Processing App\nVersion 1.0")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
