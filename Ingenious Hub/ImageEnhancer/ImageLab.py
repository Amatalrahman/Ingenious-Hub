import sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QGraphicsScene, \
    QGraphicsView, QComboBox, QInputDialog, QLabel, QSlider, QRubberBand
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QImage, QPen, QColor
import matplotlib.pyplot as plt
from io import BytesIO
import cv2


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer with Histograms and ROI")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize image variables
        self.previous_image = None  # To store the state before any changes
        self.original_image = None
        self.current_image = None
        self.output_images = [None, None, None]  # Store images for each port
        self.zoom_factor = 1

        # ROI variables

            # Other initializations
        self.rois = {'signal': [], 'background': [], 'noise': []}
        self.rois_port1 = {'signal': [], 'background': [], 'noise': []}
        self.rois_port2 = {'signal': [], 'background': [], 'noise': []} # Store multiple ROIs #where the signals are stored, this is a list
        self.current_selection = "None"
        self.rubber_band = None

        self.rubber_band_original = None
        self.rubber_band1 = None
        self.rubber_band2 = None

        self.init_ui()

    def init_ui(self):
        # Layouts
        main_layout = QVBoxLayout(self)
        image_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        histogram_layout = QHBoxLayout()

        # Buttons
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.zoom_button = QPushButton("Zoom")
        self.zoom_button.clicked.connect(self.zoom_image)
        button_layout.addWidget(self.zoom_button)

        self.interpolation_dropdown = QComboBox()
        self.interpolation_dropdown.addItem("Select Interpolation Method")
        self.interpolation_dropdown.addItem("Nearest-Neighbor")
        self.interpolation_dropdown.addItem("Linear")
        self.interpolation_dropdown.addItem("Bilinear")
        self.interpolation_dropdown.addItem("Cubic")
        button_layout.addWidget(self.interpolation_dropdown)

        self.apply_zoom_button = QPushButton("Apply Zoom")
        self.apply_zoom_button.clicked.connect(self.apply_zoom)
        button_layout.addWidget(self.apply_zoom_button)

        # Noise Dropdown
        self.noise_dropdown = QComboBox()
        self.noise_dropdown.addItem("Select Noise Type")
        self.noise_dropdown.addItem("Salt and Pepper")
        self.noise_dropdown.addItem("Gaussian")
        self.noise_dropdown.addItem("Speckle")
        button_layout.addWidget(self.noise_dropdown)

        self.apply_noise_button = QPushButton("Apply Noise")
        self.apply_noise_button.clicked.connect(self.apply_noise)
        button_layout.addWidget(self.apply_noise_button)

        # Denoise Dropdown
        self.denoise_method_dropdown = QComboBox()
        self.denoise_method_dropdown.addItem("Select Denoise Method")
        self.denoise_method_dropdown.addItem("Gaussian Blur")
        self.denoise_method_dropdown.addItem("Median Blur")
        self.denoise_method_dropdown.addItem("Bilateral Filter")
        self.denoise_method_dropdown.addItem("FastNlMeansDenoising")
        button_layout.addWidget(self.denoise_method_dropdown)

        self.denoise_button = QPushButton("Denoise")
        self.denoise_button.clicked.connect(self.denoise_image)
        button_layout.addWidget(self.denoise_button)

        # Filter Dropdown
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItem("Select Filter")
        self.filter_dropdown.addItem("Lowpass")
        self.filter_dropdown.addItem("Highpass")
        button_layout.addWidget(self.filter_dropdown)

        self.apply_filter_button = QPushButton("Apply Filter")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(self.apply_filter_button)

        # Add dropdown for contrast enhancement methods
        self.cnr_dropdown = QComboBox()
        self.cnr_dropdown.addItem("Select CNR Method")
        self.cnr_dropdown.addItem("Histogram Equalization")
        self.cnr_dropdown.addItem("CLAHE")
        self.cnr_dropdown.addItem("Gamma Correction")
        self.cnr_dropdown.addItem("Custom Contrast")
        button_layout.addWidget(self.cnr_dropdown)

        # Button to apply CNR adjustments
        self.apply_cnr_button = QPushButton("Apply CNR Adjustment")
        self.apply_cnr_button.clicked.connect(self.apply_cnr_adjustment)
        button_layout.addWidget(self.apply_cnr_button)

        new_line_layout = QHBoxLayout()

        # Add new widgets for CNR adjustments in the button layout
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100 , 100)  # Range from -100 to +100 for brightness
        self.brightness_slider.setValue(0)
        new_line_layout.addWidget(QLabel("Brightness"))
        new_line_layout.addWidget(self.brightness_slider)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 200)  # Range from 0 to 200 for contrast (100 is normal)
        self.contrast_slider.setValue(100)
        new_line_layout.addWidget(QLabel("Contrast"))
        new_line_layout.addWidget(self.contrast_slider)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_last_change)
        new_line_layout.addWidget(self.undo_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        new_line_layout.addWidget(self.quit_button)



        main_layout.addLayout(button_layout)
        main_layout.addLayout(new_line_layout)

        # Output Port Selection
        self.output_port_dropdown = QComboBox()
        self.output_port_dropdown.addItem("Original Image")
        self.output_port_dropdown.addItem("PORT 1")
        self.output_port_dropdown.addItem("PORT 2")
        button_layout.addWidget(self.output_port_dropdown)

        # Image Displays
        self.graphics_view_original = QGraphicsView(self)
        self.graphics_scene_original = QGraphicsScene(self)
        self.graphics_view_original.setScene(self.graphics_scene_original)
        image_layout.addWidget(self.graphics_view_original)

        self.graphics_view1 = QGraphicsView(self)
        self.graphics_scene1 = QGraphicsScene(self)
        self.graphics_view1.setScene(self.graphics_scene1)
        image_layout.addWidget(self.graphics_view1)

        self.graphics_view2 = QGraphicsView(self)
        self.graphics_scene2 = QGraphicsScene(self)
        self.graphics_view2.setScene(self.graphics_scene2)
        image_layout.addWidget(self.graphics_view2)

        main_layout.addLayout(image_layout)

        # Histogram Displays
        self.histogram_original = QLabel(self)
        histogram_layout.addWidget(self.histogram_original)

        self.histogram1 = QLabel(self)
        histogram_layout.addWidget(self.histogram1)

        self.histogram2 = QLabel(self)
        histogram_layout.addWidget(self.histogram2)

        main_layout.addLayout(histogram_layout)

        # ROI Buttons
        self.button_signal = QPushButton("Select Signal ROI")
        self.button_signal.clicked.connect(self.select_signal_roi)
        new_line_layout.addWidget(self.button_signal)

        self.button_background = QPushButton("Select Background ROI")
        self.button_background.clicked.connect(self.select_background_roi)
        new_line_layout.addWidget(self.button_background)

        self.button_noise = QPushButton("Select Noise ROI")
        self.button_noise.clicked.connect(self.select_noise_roi)
        new_line_layout.addWidget(self.button_noise)

        self.button_calculate_snr = QPushButton("Calculate SNR")
        self.button_calculate_snr.clicked.connect(self.calculate_snr)
        new_line_layout.addWidget(self.button_calculate_snr)

        self.button_calculate_cnr = QPushButton("Calculate CNR")
        self.button_calculate_cnr.clicked.connect(self.calculate_cnr)
        new_line_layout.addWidget(self.button_calculate_cnr)

        self.button_undo = QPushButton("Undo Selection")
        self.button_undo.clicked.connect(self.undo_selection)
        new_line_layout.addWidget(self.button_undo)

        self.setLayout(main_layout)

    def load_image(self):
        """Load an image from file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.bmp *.tiff *.gif);;All Files (*.*)")
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert("L")
                self.current_image = self.original_image.copy()
                self.output_images[0] = self.original_image.copy()
                self.output_images[1] = self.original_image.copy()
                self.output_images[2] = self.original_image.copy()
                self.display_image(self.original_image, 0)
                self.display_histogram(self.original_image, 0)
            except Exception as e:
                print(f"Error loading image: {e}")

    def display_image(self, image, output_port):
        """Display the image in the selected output port."""
        pixmap = self.pil_to_pixmap(image)
        if output_port == 0:
            self.graphics_scene_original.clear()
            self.graphics_scene_original.addPixmap(pixmap)
        elif output_port == 1:
            self.graphics_scene1.clear()
            self.graphics_scene1.addPixmap(pixmap)
        elif output_port == 2:
            self.graphics_scene2.clear()
            self.graphics_scene2.addPixmap(pixmap)

    def pil_to_pixmap(self, image):
        """Convert PIL Image to QPixmap for PyQt."""
        image_qt = image.convert("RGBA")
        data = image_qt.tobytes("raw", "RGBA")
        qimage = QImage(data, image_qt.width, image_qt.height, image_qt.width * 4, QImage.Format_RGBA8888)
        return QPixmap(qimage)

    def display_histogram(self, image, histogram_port):
        """Compute and display histogram."""
        image_array = np.array(image)

        # Generate histogram
        plt.figure(figsize=(4, 3))
        plt.hist(image_array.ravel(), bins=256, range=(0, 255), color='gray', alpha=0.7)
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.title("Histogram")
        plt.tight_layout()

        # Convert histogram plot to QPixmap
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        histogram_pixmap = QPixmap()
        histogram_pixmap.loadFromData(buf.read())
        buf.close()

        # Assign to the selected histogram label
        if histogram_port == 0:
            self.histogram_original.setPixmap(histogram_pixmap)
        elif histogram_port == 1:
            self.histogram1.setPixmap(histogram_pixmap)
        elif histogram_port == 2:
            self.histogram2.setPixmap(histogram_pixmap)

    def select_signal_roi(self):
        self.current_selection = "signal"
        self.start_roi_selection()

    def select_background_roi(self):
        self.current_selection = "background"
        self.start_roi_selection()

    def select_noise_roi(self):
        self.current_selection = "noise"
        self.start_roi_selection()

    def start_roi_selection(self):
        """Start the process for selecting a Region of Interest (ROI)."""
        if self.current_image:
            # Create rubber bands for each graphics view (port)
            self.rubber_band_original = QRubberBand(QRubberBand.Rectangle, self.graphics_view_original)
            self.rubber_band1 = QRubberBand(QRubberBand.Rectangle, self.graphics_view1)
            self.rubber_band2 = QRubberBand(QRubberBand.Rectangle, self.graphics_view2)

            # Set the cursor to a cross cursor for all views
            self.graphics_view_original.setCursor(Qt.CrossCursor)
            self.graphics_view1.setCursor(Qt.CrossCursor)
            self.graphics_view2.setCursor(Qt.CrossCursor)

            # Connect mouse events for ROI selection for each graphics view
            self.graphics_view_original.mousePressEvent = lambda event: self.roi_mouse_press(event, 'original')
            self.graphics_view_original.mouseMoveEvent = lambda event: self.roi_mouse_move(event, 'original')
            self.graphics_view_original.mouseReleaseEvent = lambda event: self.roi_mouse_release(event, 'original')

            self.graphics_view1.mousePressEvent = lambda event: self.roi_mouse_press(event, 'port1')
            self.graphics_view1.mouseMoveEvent = lambda event: self.roi_mouse_move(event, 'port1')
            self.graphics_view1.mouseReleaseEvent = lambda event: self.roi_mouse_release(event, 'port1')

            self.graphics_view2.mousePressEvent = lambda event: self.roi_mouse_press(event, 'port2')
            self.graphics_view2.mouseMoveEvent = lambda event: self.roi_mouse_move(event, 'port2')
            self.graphics_view2.mouseReleaseEvent = lambda event: self.roi_mouse_release(event, 'port2')

    def roi_mouse_press(self, event, port):
        """Handle mouse press event for ROI selection."""
        self.start_point = event.pos()

        # Select the correct rubber band for the active view (port)
        if port == 'original':
            self.rubber_band = self.rubber_band_original
        elif port == 'port1':
            self.rubber_band = self.rubber_band1
        elif port == 'port2':
            self.rubber_band = self.rubber_band2

        # Ensure the rubber band is created for the port (check if it's None)
        if self.rubber_band is None:
            print(f"Error: Rubber band is None for port {port}")
            return

        # Set the initial geometry for the rubber band
        self.rubber_band.setGeometry(QRect(self.start_point, QSize()))
        self.rubber_band.show()

    def roi_mouse_move(self, event, port):
        """Handle mouse move event for ROI selection."""
        if self.rubber_band:
            self.rubber_band.setGeometry(QRect(self.start_point, event.pos()).normalized())
        else:
            print(f"Error: Rubber band is None for port {port}")

    def roi_mouse_release(self, event, port):
        """Handle mouse release event for ROI selection."""
        # Reset cursor back to default arrow
        if port == 'original':
            self.graphics_view_original.setCursor(Qt.ArrowCursor)
        elif port == 'port1':
            self.graphics_view1.setCursor(Qt.ArrowCursor)
        elif port == 'port2':
            self.graphics_view2.setCursor(Qt.ArrowCursor)

        # Hide the rubber band after selection
        if self.rubber_band:
            self.rubber_band.hide()
            rect = self.rubber_band.geometry()

            # Convert ROI coordinates to image coordinates for the selected port
            if port == 'original':
                scene_pos = self.graphics_view_original.mapToScene(rect.topLeft())
            elif port == 'port1':
                scene_pos = self.graphics_view1.mapToScene(rect.topLeft())
            elif port == 'port2':
                scene_pos = self.graphics_view2.mapToScene(rect.topLeft())

            # Extract the x, y, width, and height for the selected ROI
            x, y = int(scene_pos.x()), int(scene_pos.y())
            width, height = rect.width(), rect.height()

            # Store the selected ROI for the correct port's image
            roi_tuple = (x, y, width, height)

            # Only store the ROI for the current port's selection
            if port == 'original':
                self.rois[self.current_selection].append(roi_tuple)
            elif port == 'port1':
                self.rois_port1[self.current_selection].append(roi_tuple)
            elif port == 'port2':
                self.rois_port2[self.current_selection].append(roi_tuple)

            # Mark the ROI on the selected port's image
            self.mark_roi(x, y, width, height, port)

            # Reset the current selection after marking
            self.current_selection = "None"
            self.rubber_band = None
        else:
            print(f"Error: Rubber band is None for port {port}")

    def mark_roi(self, x, y, width, height, port):
        """Draw a rectangle to mark the selected ROI on the selected image (port)."""
        # Choose the color for the ROI depending on the selection type
        color = QColor(255, 0, 0) if self.current_selection == "signal" else \
            QColor(0, 255, 0) if self.current_selection == "background" else \
                QColor(0, 0, 255)  # Default to blue for noise

        # Define the pen for the rectangle (line thickness and style)
        pen = QPen(color, 2, Qt.SolidLine)

        # Mark the ROI only on the selected port's image
        if port == 'original':
            self.graphics_scene_original.addRect(x, y, width, height, pen)
        elif port == 'port1':
            self.graphics_scene1.addRect(x, y, width, height, pen)
        elif port == 'port2':
            self.graphics_scene2.addRect(x, y, width, height, pen)

    def calculate_snr(self):
        """Calculate and display SNR based on selected Signal and Noise ROIs for the current port."""
        try:
            # Get the current output port index
            selected_port = self.output_port_dropdown.currentIndex()

            # Check if there are Signal and Noise ROIs for the selected port
            if selected_port == 0:  # Original port
                signal_rois = self.rois['signal']
                noise_rois = self.rois['noise']
            elif selected_port == 1:  # Port 1
                signal_rois = self.rois_port1['signal']
                noise_rois = self.rois_port1['noise']
            elif selected_port == 2:  # Port 2
                signal_rois = self.rois_port2['signal']
                noise_rois = self.rois_port2['noise']

            # Ensure at least one signal and one noise ROI are selected for the port
            if len(signal_rois) == 0:
                self.histogram_original.setText(f"SNR: Please select a Signal ROI for Port {selected_port + 1}")
                return
            if len(noise_rois) == 0:
                self.histogram_original.setText(f"SNR: Please select a Noise ROI for Port {selected_port + 1}")
                return

            # Extract pixel data for the last selected signal and noise ROIs
            signal_roi = signal_rois[-1]  # Only use the last signal ROI
            noise_roi = noise_rois[-1]  # Only use the last noise ROI

            signal_data = self.extract_roi_data(signal_roi, selected_port)
            noise_data = self.extract_roi_data(noise_roi, selected_port)

            # Check if the extracted data is empty
            if signal_data.size == 0 or noise_data.size == 0:
                self.histogram_original.setText(f"SNR: No data in selected ROIs for Port {selected_port + 1}")
                return

            # Calculate SNR: mean_signal / std_noise
            mean_signal = np.mean(signal_data)
            std_noise = np.std(noise_data)
            snr = mean_signal / std_noise if std_noise > 0 else 0  # Avoid division by zero

            # Display SNR
            self.histogram_original.setText(f"SNR for Port {selected_port + 1}: {snr:.2f}")
        except Exception as e:
            self.histogram_original.setText(f"SNR: Error - {str(e)}")

    def calculate_cnr(self):
        """Calculate and display CNR based on selected Signal, Background, and Noise ROIs for the current port."""
        try:
            # Get the current output port index
            selected_port = self.output_port_dropdown.currentIndex()

            # Check if there are Signal, Background, and Noise ROIs for the selected port
            if selected_port == 0:  # Original port
                signal_rois = self.rois['signal']
                background_rois = self.rois['background']
                noise_rois = self.rois['noise']
            elif selected_port == 1:  # Port 1
                signal_rois = self.rois_port1['signal']
                background_rois = self.rois_port1['background']
                noise_rois = self.rois_port1['noise']
            elif selected_port == 2:  # Port 2
                signal_rois = self.rois_port2['signal']
                background_rois = self.rois_port2['background']
                noise_rois = self.rois_port2['noise']

            # Ensure at least one ROI exists for each required type
            if len(signal_rois) == 0:
                self.histogram_original.setText(f"CNR: Please select a Signal ROI for Port {selected_port + 1}")
                return
            if len(background_rois) == 0:
                self.histogram_original.setText(f"CNR: Please select a Background ROI for Port {selected_port + 1}")
                return
            if len(noise_rois) == 0:
                self.histogram_original.setText(f"CNR: Please select a Noise ROI for Port {selected_port + 1}")
                return

            # Extract pixel data for the last selected signal, background, and noise ROIs
            signal_roi = signal_rois[-1]  # Only use the last signal ROI
            background_roi = background_rois[-1]  # Only use the last background ROI
            noise_roi = noise_rois[-1]  # Only use the last noise ROI

            signal_data = self.extract_roi_data(signal_roi, selected_port)
            background_data = self.extract_roi_data(background_roi, selected_port)
            noise_data = self.extract_roi_data(noise_roi, selected_port)

            # Check if the extracted data is empty
            if signal_data.size == 0 or background_data.size == 0 or noise_data.size == 0:
                self.histogram_original.setText(f"CNR: No data in selected ROIs for Port {selected_port + 1}")
                return

            # Calculate CNR: (mean_signal - mean_background) / std_noise
            mean_signal = np.mean(signal_data)
            mean_background = np.mean(background_data)
            std_noise = np.std(noise_data)
            cnr = abs((mean_signal - mean_background) / std_noise if std_noise > 0 else 0)

            # Display CNR
            self.histogram_original.setText(f"CNR for Port {selected_port + 1}: {cnr:.2f}")
        except Exception as e:
            self.histogram_original.setText(f"CNR: Error - {str(e)}")

    def extract_roi_data(self, roi, port):
        """Extract pixel data from the given ROI, for a specific port."""
        try:
            x, y, width, height = roi

            # Get the image for the selected port
            if port == 0:  # Original port
                img_array = np.array(self.output_images[0])  # Adjust based on how images are stored
            elif port == 1:  # Port 1
                img_array = np.array(self.output_images[1])
            elif port == 2:  # Port 2
                img_array = np.array(self.output_images[2])

            # Extract the region of interest (ROI) data
            roi_data = img_array[y:y + height, x:x + width]

            # Flatten the ROI data to make it a 1D array for easier processing
            return roi_data.flatten()  # Flatten to a list of pixel values
        except Exception as e:
            print(f"Error extracting ROI data for Port {port + 1}: {str(e)}")
            return np.array([])

    def undo_selection(self):
        """Undo the most recent ROI selection for the current type."""
        if self.current_selection != "None" and self.rois[self.current_selection]:
            # Remove the last ROI from the list
            self.rois[self.current_selection].pop()
            self.display_image(self.output_images[self.output_port_dropdown.currentIndex()], self.output_port_dropdown.currentIndex())  # Redraw the image with the updated ROI selections
            self.histogram_original.setText(f"Last {self.current_selection.capitalize()} ROI selection undone.")
        else:
            self.histogram_original.setText(f"No {self.current_selection.capitalize()} selection to undo.")

    def apply_noise(self):
        """Apply selected noise type to the image."""
        selected_port = self.output_port_dropdown.currentIndex()
        noise_type = self.noise_dropdown.currentText()
        if self.current_image is not None:
            self.previous_image = self.current_image.copy()

        if self.current_image:
            if noise_type == "Salt and Pepper":
                self.add_salt_and_pepper_noise(selected_port)
            elif noise_type == "Gaussian":
                self.add_gaussian_noise(selected_port)
            elif noise_type == "Speckle":
                self.add_speckle_noise(selected_port)

    def add_salt_and_pepper_noise(self, selected_port):
        """Add salt and pepper noise."""
        image_array = np.array(self.output_images[selected_port])
        salt_prob, pepper_prob = 0.02, 0.02

        # Generate a copy of the image array to modify
        noisy_image = image_array.copy()

        # Generate salt and pepper masks
        salt_mask = np.random.rand(*image_array.shape) < salt_prob
        pepper_mask = np.random.rand(*image_array.shape) < pepper_prob

        # Apply the masks to the noisy image
        noisy_image[salt_mask] = 255  # Salt noise
        noisy_image[pepper_mask] = 0  # Pepper noise

        # Convert back to an image format
        noisy_image = Image.fromarray(noisy_image.astype(np.uint8))
        self.output_images[selected_port] = noisy_image
        self.current_image = noisy_image
        self.display_image(noisy_image, selected_port)
        self.display_histogram(noisy_image, selected_port)

    def add_gaussian_noise(self, selected_port):
        """Add Gaussian noise to the image."""
        mean, var = 0, 0.1

        image_array = np.array(self.output_images[selected_port])
        noise = np.random.normal(mean, var ** 0.5, image_array.shape)
        noisy_image = np.clip(image_array + noise * 255, 0, 255).astype(np.uint8)
        noisy_image = Image.fromarray(noisy_image)
        self.output_images[selected_port] = noisy_image
        self.current_image = noisy_image
        self.display_image(noisy_image, selected_port)
        self.display_histogram(noisy_image, selected_port)

    def add_speckle_noise(self, selected_port):
        """Add speckle noise to the image."""
        mean, var = 0, 0.1

        image_array = np.array(self.output_images[selected_port])
        noise = np.random.normal(mean, var ** 0.5, image_array.shape)
        noisy_image = np.clip(image_array + image_array * noise, 0, 255).astype(np.uint8)
        noisy_image = Image.fromarray(noisy_image)
        self.output_images[selected_port] = noisy_image
        self.current_image = noisy_image
        self.display_image(noisy_image, selected_port)
        self.display_histogram(noisy_image, selected_port)

    def denoise_image(self):
        """Apply selected denoising method."""
        selected_port = self.output_port_dropdown.currentIndex()
        denoise_method = self.denoise_method_dropdown.currentText()
        if self.current_image is not None:
            self.previous_image = self.current_image.copy()
        if denoise_method == "Gaussian Blur":
            self.denoise_with_gaussian_blur(selected_port)
        elif denoise_method == "Median Blur":
            self.denoise_with_median_blur(selected_port)
        elif denoise_method == "Bilateral Filter":
            self.denoise_with_bilateral_filter(selected_port)
        elif denoise_method == "FastNlMeansDenoising":
            self.denoise_with_fast_nl_means(selected_port)

    def denoise_with_gaussian_blur(self, selected_port):
        """Denoise using Gaussian blur."""
        image_array = np.array(self.output_images[selected_port])
        denoised_image = cv2.GaussianBlur(image_array, (5, 5), 0)
        self.output_images[selected_port] = Image.fromarray(denoised_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def denoise_with_median_blur(self, selected_port):
        """Denoise using median blur."""
        image_array = np.array(self.output_images[selected_port])
        denoised_image = cv2.medianBlur(image_array, 5)
        self.output_images[selected_port] = Image.fromarray(denoised_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def denoise_with_bilateral_filter(self, selected_port):
        """Denoise using bilateral filter."""
        image_array = np.array(self.output_images[selected_port])
        denoised_image = cv2.bilateralFilter(image_array, 9, 75, 75)
        self.output_images[selected_port] = Image.fromarray(denoised_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def denoise_with_fast_nl_means(self, selected_port):
        """Denoise using fast non-local means denoising."""
        image_array = np.array(self.output_images[selected_port])
        denoised_image = cv2.fastNlMeansDenoising(image_array, None, 30, 7, 21)
        self.output_images[selected_port] = Image.fromarray(denoised_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def apply_filter(self):
        """Apply selected filter."""
        selected_port = self.output_port_dropdown.currentIndex()
        filter_type = self.filter_dropdown.currentText()

        if self.current_image is not None:
            self.previous_image = self.current_image.copy()

        if self.current_image:
            if filter_type == "None":
                # Don't apply any filter, just display the current image
                self.display_image(self.output_images[selected_port], selected_port)
                self.display_histogram(self.output_images[selected_port], selected_port)
            elif filter_type == "Lowpass":
                self.apply_lowpass_filter(selected_port)
            elif filter_type == "Highpass":
                self.apply_highpass_filter(selected_port)

    def apply_lowpass_filter(self, selected_port):
        """Apply lowpass filter to the image."""
        if self.output_images[selected_port] is not None:
            image_array = np.array(self.output_images[selected_port])
            kernel = np.ones((5, 5), np.float32) / 25
            filtered_image = cv2.filter2D(image_array, -1, kernel)
            self.output_images[selected_port] = Image.fromarray(filtered_image)
            self.display_image(self.output_images[selected_port], selected_port)
            self.display_histogram(self.output_images[selected_port], selected_port)

    def apply_highpass_filter(self, selected_port):
        """Apply highpass filter to the image."""
        if self.output_images[selected_port] is not None:
            image_array = np.array(self.output_images[selected_port])
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            filtered_image = cv2.filter2D(image_array, -1, kernel)
            self.output_images[selected_port] = Image.fromarray(filtered_image)
            self.display_image(self.output_images[selected_port], selected_port)
            self.display_histogram(self.output_images[selected_port], selected_port)

    def zoom_image(self):
        """Prompt user for zoom factor."""
        zoom_factor, ok = QInputDialog.getDouble(self, "Zoom Factor", "Enter zoom factor (e.g., 2 for 200%):")
        if ok:
            self.zoom_factor = zoom_factor
            self.apply_zoom()

    def apply_zoom(self):
        """Apply zoom effect with selected interpolation."""
        selected_port = self.output_port_dropdown.currentIndex()
        if self.output_images[selected_port] is not None:
            self.previous_image = self.output_images[selected_port].copy()
            interpolation_method = self.interpolation_dropdown.currentText()
            interpolation = Image.Resampling.NEAREST
            if interpolation_method == "Nearest-Neighbor":
                interpolation = Image.Resampling.NEAREST
            elif interpolation_method == "Linear":
                interpolation = Image.Resampling.BILINEAR
            elif interpolation_method == "Bilinear":
                interpolation = Image.Resampling.BILINEAR
            elif interpolation_method == "Cubic":
                interpolation = Image.Resampling.BICUBIC

            new_size = (
                int(self.output_images[selected_port].width * self.zoom_factor),
                int(self.output_images[selected_port].height * self.zoom_factor)
            )
            zoomed_image = self.output_images[selected_port].resize(new_size, resample=interpolation)

            # Update the output image for the selected port
            self.output_images[selected_port] = zoomed_image
            self.display_image(zoomed_image, selected_port)
            self.display_histogram(zoomed_image, selected_port)

    def apply_cnr_adjustment(self):
        """Apply CNR (Contrast-to-Noise Ratio) adjustment."""
        selected_port = self.output_port_dropdown.currentIndex()
        cnr_method = self.cnr_dropdown.currentText()
        if self.output_images[selected_port] is not None:
            self.previous_image = self.output_images[selected_port].copy()

        if self.output_images[selected_port]:
            if cnr_method == "Histogram Equalization":
                self.apply_histogram_equalization(selected_port)
            elif cnr_method == "CLAHE":
                self.apply_clahe(selected_port)
            elif cnr_method == "Gamma Correction":
                self.apply_gamma_correction(selected_port)
            elif cnr_method == "Custom Contrast":
                self.apply_custom_contrast(selected_port)

    def apply_histogram_equalization(self, selected_port):
        """Apply histogram equalization to enhance contrast."""
        image_array = np.array(self.output_images[selected_port])
        equalized_image = cv2.equalizeHist(image_array)
        self.output_images[selected_port] = Image.fromarray(equalized_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def apply_clahe(self, selected_port):
        """Apply CLAHE for contrast enhancement."""
        image_array = np.array(self.output_images[selected_port])
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_image = clahe.apply(image_array)
        self.output_images[selected_port] = Image.fromarray(clahe_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def apply_custom_contrast(self, selected_port):
        """Apply custom contrast based on slider values."""
        contrast_value = self.contrast_slider.value() / 100.0
        brightness_value = self.brightness_slider.value()

        image_array = np.array(self.output_images[selected_port])
        adjusted_image = np.clip((image_array * contrast_value + brightness_value), 0, 255).astype(np.uint8)
        self.output_images[selected_port] = Image.fromarray(adjusted_image)
        self.display_image(self.output_images[selected_port], selected_port)
        self.display_histogram(self.output_images[selected_port], selected_port)

    def undo_last_change(self):
        """Revert the image to its previous state (undo last edit)."""
        selected_port = self.output_port_dropdown.currentIndex()
        if self.previous_image is not None:
            self.output_images[selected_port] = self.previous_image.copy()  # Restore the previous image
            self.display_image(self.output_images[selected_port], selected_port)
            self.display_histogram(self.output_images[selected_port], selected_port)
        else:
            # No changes to undo
            print("No action to undo.")

# Main Code to Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())