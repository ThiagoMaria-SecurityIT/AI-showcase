from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import os
import time
import numpy as np
from PIL import Image
import sys

class YOLODetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced YOLO Object Detector")
        self.root.geometry("800x600")
        self.current_image_path = None
        self.scaling_mode = "fit"  # Default scaling mode
        self.model = YOLO("yolo11x.pt").to('cpu')
         
        # Load model once
        self.model = YOLO("yolo11x.pt").to('cpu')
        
        # Video detection variables
        self.cap = None
        self.is_playing = False
        self.frame_count = 0
        self.last_results = None
        self.original_results = None
        self.video_file_path = None
        
        # Create filter controls frame
        self.create_filter_controls()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_image_tab()
        self.create_video_tab()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        if hasattr(self.model, 'names'):
            self.class_dropdown['values'] = list(self.model.names.values())
            
        if hasattr(self, 'class_dropdown') and hasattr(self.model, 'names'):
            self.class_dropdown['values'] = list(self.model.names.values())

    def create_filter_controls(self):
        """Create simplified filter controls"""
        self.filter_frame = ttk.LabelFrame(self.root, text="Detection Settings", padding=10)
        self.filter_frame.pack(fill='x', padx=10, pady=5)
        
        # Confidence threshold slider
        ttk.Label(self.filter_frame, text="Confidence:").grid(row=0, column=0, padx=5)
        self.confidence = tk.DoubleVar(value=0.25)  # Default confidence
        ttk.Scale(
            self.filter_frame,
            from_=0.1,
            to=0.9,
            variable=self.confidence,
            orient=tk.HORIZONTAL,
            length=150,
            command=lambda v: self.apply_filters()
        ).grid(row=0, column=1, padx=5)
        ttk.Label(self.filter_frame, textvariable=self.confidence).grid(row=0, column=2, padx=5)
        
        # Class selection dropdown
        ttk.Label(self.filter_frame, text="Class:").grid(row=0, column=3, padx=5)
        self.class_var = tk.StringVar()
        self.class_dropdown = ttk.Combobox(
            self.filter_frame,
            textvariable=self.class_var,
            state="readonly",
            width=15
        )
        # Initialize with empty values, will be updated after model loads
        self.class_dropdown['values'] = []
        self.class_dropdown.grid(row=0, column=4, padx=5)
        self.class_dropdown.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Reset button
        ttk.Button(
            self.filter_frame,
            text="Reset",
            command=self.reset_filters
        ).grid(row=0, column=5, padx=5)

    def apply_filters(self, *args):
        """Apply confidence threshold and class filter"""
        if not hasattr(self, 'original_results') or not self.original_results:
            return
        
        # Get current filter values
        conf_thresh = self.confidence.get()
        selected_class = self.class_var.get()
        
        # Create filtered results
        filtered_results = self.original_results[0].new()
        filtered_results.orig_img = self.original_results[0].orig_img.copy()
        filtered_results.orig_shape = self.original_results[0].orig_shape
        filtered_results.path = self.original_results[0].path
        filtered_results.names = self.original_results[0].names
        
        # Apply confidence threshold
        if self.original_results[0].boxes:
            boxes = self.original_results[0].boxes
            mask = boxes.conf >= conf_thresh
            filtered_results.boxes = boxes[mask]
        
        # Apply class filter if selected
        if selected_class and filtered_results.boxes and hasattr(self.model, 'names'):
            try:
                class_names = list(self.model.names.values())
                if selected_class in class_names:
                    class_id = class_names.index(selected_class)
                    mask = filtered_results.boxes.cls == class_id
                    filtered_results.boxes = filtered_results.boxes[mask]
            except Exception as e:
                print(f"Error applying class filter: {e}")
        
        # Update display
        self.display_filtered_results(filtered_results)

    def reset_filters(self):
        """Reset filters to defaults"""
        self.confidence.set(0.25)
        self.class_var.set("")
        if hasattr(self, 'original_results') and self.original_results:
            self.display_filtered_results(self.original_results[0])

    def apply_filters_to_frame(self, results):
        """Apply filters to video frame results"""
        if not results.boxes:
            return
        
        conf_thresh = self.confidence.get()
        selected_class = self.class_var.get()
        
        # Apply confidence threshold
        mask = results.boxes.conf >= conf_thresh
        results.boxes = results.boxes[mask]
        
        # Apply class filter if selected
        if selected_class and results.boxes and hasattr(self.model, 'names'):
            try:
                class_names = list(self.model.names.values())
                if selected_class in class_names:
                    class_id = class_names.index(selected_class)
                    mask = results.boxes.cls == class_id
                    results.boxes = results.boxes[mask]
            except Exception as e:
                print(f"Error applying class filter: {e}")

    def create_image_tab(self):
        """Create the image detection tab with properly working scrollbars"""
        self.image_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_tab, text="Image Detection")
        
        ttk.Button(
            self.image_tab,
            text="Select Image & Detect",
            command=self.process_image,
            style='Accent.TButton'
        ).pack(pady=20)
        
        # Scaling options frame
        scaling_frame = ttk.Frame(self.image_tab)
        scaling_frame.pack(pady=5)
        
        ttk.Label(scaling_frame, text="Scaling:").pack(side=tk.LEFT, padx=5)
        
        # Set default to "original" instead of "fit"
        self.scaling_var = tk.StringVar(value="fit")  # Changed here
        
        scaling_options = [
            ("Fill", "fill"),
            ("Fit", "fit"),
            ("Stretch", "stretch"),
            ("Original", "original")
        ]
        
        for text, mode in scaling_options:
            ttk.Radiobutton(
                scaling_frame,
                text=text,
                variable=self.scaling_var,
                value=mode,
                command=self.update_image_scaling  # This ensures immediate update
            ).pack(side=tk.LEFT, padx=5)
        
        # Create a frame to hold canvas and scrollbars
        image_frame = ttk.Frame(self.image_tab)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.image_canvas = tk.Canvas(image_frame, bg='white')
        self.h_scroll = ttk.Scrollbar(image_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        self.v_scroll = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        
        # Configure canvas scrolling
        self.image_canvas.configure(
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )
        
        # Grid layout for proper scrollbar placement
        self.image_canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        image_frame.grid_rowconfigure(0, weight=1)
        image_frame.grid_columnconfigure(0, weight=1)
        
        # Container frame for the image
        self.image_container = ttk.Frame(self.image_canvas)
        self.image_window = self.image_canvas.create_window(
            (0, 0), 
            window=self.image_container, 
            anchor="nw",
            tags="image_container"
        )
        
        # The actual image label
        self.image_panel = ttk.Label(self.image_container)
        self.image_panel.pack()
        
        # Bind to canvas resize events
        self.image_canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.image_stats = ttk.Label(
            self.image_tab,
            text="",
            font=('Helvetica', 10)
        )
        self.image_stats.pack()

    def _on_canvas_configure(self, event):
        """Handle canvas resize events"""
        if hasattr(self, 'current_image_tk') and self.current_image_tk:
            self._update_scroll_region()

    def _update_scroll_region(self):
        """Update the scroll region based on current image and scaling mode"""
        if not hasattr(self, 'current_image_tk') or not self.current_image_tk:
            return
        
        # Get the actual size of the image in the label
        img_width = self.current_image_tk.width()
        img_height = self.current_image_tk.height()
        
        # Set scroll region to match the image size
        self.image_canvas.config(scrollregion=(0, 0, img_width, img_height))
        
        # Update the container size
        self.image_container.config(width=img_width, height=img_height)

    def create_video_tab(self):
        """Create the video detection tab"""
        self.video_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.video_tab, text="Video Detection")
        
        # Video detection UI
        self.video_btn = ttk.Button(
            self.video_tab,
            text="Select Video",
            command=self.toggle_video,
            style='Accent.TButton'
        )
        self.video_btn.pack(pady=20)
        
        # Add playback controls
        control_frame = ttk.Frame(self.video_tab)
        control_frame.pack(pady=5)
        
        ttk.Button(
            control_frame,
            text="⏸",
            command=self.pause_video,
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="⏭",
            command=self.next_frame,
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        self.video_panel = ttk.Label(self.video_tab)
        self.video_panel.pack()
        
        self.video_stats = ttk.Label(
            self.video_tab,
            text="FPS: 0 | Frame: 0 | Objects: 0",
            font=('Helvetica', 10)
        )
        self.video_stats.pack()

    def process_image(self):
        """Process an image file with object detection"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        
        if not file_path:
            return
        
        try:
            start_time = time.time()
            self.current_image_path = file_path
            print(f"Processing selected image: {file_path}")
            
            # Clear previous display
            self.image_panel.config(image='')
            self.image_panel.image = None
            self.root.update()
            
            # Run inference
            timestamp = int(time.time())
            results = self.model.predict(
                file_path,
                conf=0.25,
                save=True,
                exist_ok=True,
                project="runs/detect",
                name=f"predict_{timestamp}",
                save_txt=True
            )
            
            if not results:
                raise ValueError("No detection results returned")
                
            self.original_results = results
            output_dir = results[0].save_dir
            
            # Find the actual output image (YOLO may rename it)
            output_image_path = None
            for file in os.listdir(output_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                    output_image_path = os.path.join(output_dir, file)
                    break
            
            if not output_image_path:
                raise FileNotFoundError(f"No output image found in {output_dir}")
            
            self.output_image_path = output_image_path  # Store the correct path
            print(f"Output found at: {self.output_image_path}")
            
            self.display_detection_results(results[0])
            
            proc_time = (time.time() - start_time) * 1000
            self.image_stats.config(
                text=f"Processing time: {proc_time:.1f}ms | Objects detected: {len(results[0].boxes)}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            import traceback
            traceback.print_exc()

    def display_detection_results(self, results):
        """Display the detection results"""
        try:
            if not hasattr(self, 'output_image_path'):
                raise ValueError("Output image path not set")
                
            print(f"Displaying image from: {self.output_image_path}")
            
            # Load image with quality preservation
            img = Image.open(self.output_image_path)
            self.original_img_size = img.size
            
            # Calculate new size based on scaling mode
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            new_width, new_height = self.get_scaled_size(
                img.width, img.height,
                canvas_width, canvas_height
            )
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_image_tk = ImageTk.PhotoImage(img)
            self.image_panel.config(image=self.current_image_tk)
            
            # Update container and scroll region
            self.image_container.config(width=new_width, height=new_height)
            self._update_scroll_region()
            
        except Exception as e:
            raise RuntimeError(f"Failed to display results: {str(e)}")

    def update_image_scaling(self):
        """Update the image display when scaling mode changes"""
        if not hasattr(self, 'output_image_path') or not os.path.exists(self.output_image_path):
            print("No valid output image path found for scaling update.")
            return

        try:
            # Load the image from the stored output path
            img = Image.open(self.output_image_path)
            self.original_img_size = img.size  # Store original size

            # Get canvas dimensions
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            # Calculate new size based on selected scaling mode
            new_width, new_height = self.get_scaled_size(
                img.width, img.height,
                canvas_width, canvas_height
            )

            # Resize with high-quality filtering
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage and update display
            self.current_image_tk = ImageTk.PhotoImage(img)
            self.image_panel.config(image=self.current_image_tk)

            # Update container and scroll region
            self.image_container.config(width=new_width, height=new_height)
            self._update_scroll_region()

        except Exception as e:
            print(f"Error updating image scaling: {e}")

    
    def get_scaled_size(self, original_width, original_height, canvas_width, canvas_height):
        """Calculate the scaled size based on the selected mode"""
        mode = self.scaling_var.get()
        
        if mode == "original":
            return (original_width, original_height)
        
        if mode == "fill":
            # Fill the canvas completely (may crop)
            ratio = max(canvas_width/original_width, canvas_height/original_height)
            return (int(original_width*ratio), int(original_height*ratio))
        
        elif mode == "fit":
            # Fit within canvas while maintaining aspect ratio
            ratio = min(canvas_width/original_width, canvas_height/original_height)
            return (int(original_width*ratio), int(original_height*ratio))
        
        elif mode == "stretch":
            # Stretch to fill canvas exactly (distorts aspect ratio)
            return (canvas_width, canvas_height)
        
        return (original_width, original_height)  # Default
    
    def toggle_video(self):
        """Toggle video playback or open a video file if none is loaded"""
        if self.cap is None:
            # Open a video file
            file_path = filedialog.askopenfilename(
                filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
            )
            if not file_path:
                return
                
            try:
                self.video_file_path = file_path
                self.cap = cv2.VideoCapture(file_path)
                self.is_playing = True
                self.frame_count = 0
                self.video_btn.config(text="Stop Video")
                self.play_video()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open video: {str(e)}")
        else:
            # Stop video playback
            self.stop_video()

    def play_video(self):
        """Play the video with object detection"""
        if self.is_playing and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                
                # Run detection on the frame
                results = self.model.track(frame, persist=True, conf=0.25)
                
                # Apply filters if any
                self.apply_filters_to_frame(results[0])
                
                # Display the frame with detections
                annotated_frame = results[0].plot()
                self.update_video_display(annotated_frame)
                
                # Calculate FPS
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                
                # Update stats
                self.video_stats.config(
                    text=f"FPS: {fps:.1f} | Frame: {self.frame_count} | Objects: {len(results[0].boxes)}"
                )
                
                # Schedule next frame
                delay = max(1, int(1000/fps)) if fps > 0 else 30
                self.root.after(delay, self.play_video)
            else:
                # Video ended
                self.stop_video()

    def pause_video(self):
        """Pause video playback"""
        if self.cap:
            self.is_playing = not self.is_playing
            if self.is_playing:
                self.play_video()

    def next_frame(self):
        """Move to next frame manually"""
        if self.cap and not self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                results = self.model.track(frame, persist=True, conf=0.25)
                self.apply_filters_to_frame(results[0])
                self.update_video_display(results[0].plot())
                self.video_stats.config(
                    text=f"Frame: {self.frame_count} | Objects: {len(results[0].boxes)} (Paused)"
                )

    def stop_video(self):
        """Stop video playback and release resources"""
        self.is_playing = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_btn.config(text="Select Video")
        self.video_stats.config(text="Video stopped")

    def apply_filters(self):
        """Apply current filters to the results"""
        if not self.original_results:
            messagebox.showinfo("Info", "No detection results to filter")
            return
        
        # Create a new Results object with the same base attributes
        filtered_results = self.original_results[0].new()
        
        # Copy the original image and other attributes
        filtered_results.orig_img = self.original_results[0].orig_img.copy()
        filtered_results.orig_shape = self.original_results[0].orig_shape
        filtered_results.path = self.original_results[0].path
        filtered_results.names = self.original_results[0].names
        
        # Get filter values
        max_objects = self.max_objects.get()
        target_class = self.object_filter.get().strip().lower()
        
        # Initialize empty boxes
        filtered_results.boxes = None
        
        # Apply max objects filter
        if self.original_results[0].boxes:
            boxes = self.original_results[0].boxes
            if max_objects > 0 and len(boxes) > max_objects:
                confidences = boxes.conf.cpu().numpy()
                top_indices = confidences.argsort()[-max_objects:][::-1]
                filtered_results.boxes = boxes[top_indices]
            else:
                filtered_results.boxes = boxes
        
        # Apply class filter
        if target_class and filtered_results.boxes:
            class_names = filtered_results.names
            matching_indices = []
            
            for i, cls in enumerate(filtered_results.boxes.cls):
                class_name = class_names[int(cls)].lower()
                if target_class in class_name:
                    matching_indices.append(i)
            
            if matching_indices:
                filtered_results.boxes = filtered_results.boxes[matching_indices]
            else:
                messagebox.showinfo("Filter Result", 
                    f"No objects of type '{target_class}' detected")
                return
        
        # Display filtered results
        self.display_filtered_results(filtered_results)

    def apply_filters_to_frame(self, results):
        """Apply filters to video frame results"""
        if not results.boxes:
            return
        
        conf_thresh = self.confidence.get()
        selected_class = self.class_var.get()
        
        # Apply confidence threshold
        mask = results.boxes.conf >= conf_thresh
        results.boxes = results.boxes[mask]
        
        # Apply class filter if selected
        if selected_class and results.boxes and hasattr(self.model, 'names'):
            try:
                class_names = list(self.model.names.values())
                if selected_class in class_names:
                    class_id = class_names.index(selected_class)
                    mask = results.boxes.cls == class_id
                    results.boxes = results.boxes[mask]
            except Exception as e:
                print(f"Error applying class filter: {e}")

    def reset_filters(self):
        """Reset all filters to their default values"""
        self.max_objects.set(0)
        self.object_filter.set("")
        
        if self.original_results:
            self.display_filtered_results(self.original_results[0])

    def display_filtered_results(self, results):
        """Display filtered results in the appropriate tab"""
        # For image tab
        if hasattr(self, 'image_panel'):
            output_path = os.path.join(results.save_dir, os.path.basename(results.path))
            if os.path.exists(output_path):
                img = Image.open(output_path)
                img = img.resize((800, int(800/img.size[0]*img.size[1])), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.image_panel.config(image=img)
                self.image_panel.image = img
                
                self.image_stats.config(
                    text=f"Objects detected: {len(results.boxes)}" + 
                    (" (Filtered)" if self.max_objects.get() > 0 or self.object_filter.get() else "")
                )

    def update_video_display(self, frame):
        """Update the video display panel with a new frame"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        self.video_panel.config(image=img)
        self.video_panel.image = img

    def on_close(self):
        """Handle window close event"""
        self.stop_video()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Modern theme (requires ttkthemes or sun-valley-ttk)
    try:
        from ttkthemes import ThemedStyle
        style = ThemedStyle(root)
        style.set_theme("arc")
    except ImportError:
        pass
    
    app = YOLODetectionApp(root)
    root.mainloop()
