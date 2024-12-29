import sys
import os
import pydicom
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QPushButton, QScrollArea, QDialog, QLineEdit, QMessageBox,
    QTableWidgetItem, QTableWidget, QTabWidget, QInputDialog, QComboBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import random
import numpy as np

class MetadataViewer(QDialog):
    def __init__(self, dataset=None, parent=None):  # In MetadataViewer
        super().__init__(parent)
        self.setWindowTitle("DICOM Metadata Viewer")
        self.resize(600, 800)

        self.dataset = dataset
        self.tag_names = [
            'AccessionNumber', 'ActualFrameDuration', 'BitsAllocated', 'BitsStored', 
            'CineRate', 'Columns', 'ContentDate', 'ContentTime', 'EffectiveDuration', 
            'FrameDelay', 'FrameIncrementPointer', 'FrameTime', 'HeartRate', 'HighBit', 
            'ImageType', 'InstanceNumber', 'Manufacturer', 'ManufacturerModelName', 
            'Modality', 'NumberOfFrames', 'OperatorsName', 'PatientBirthDate', 
            'PatientBirthTime', 'PatientID', 'PatientName', 'PatientOrientation', 
            'PatientSex', 'PhotometricInterpretation', 'PixelData', 'PixelRepresentation', 
            'PlanarConfiguration', 'PreferredPlaybackSequencing', 'RecommendedDisplayFrameRate', 
            'ReferringPhysicianName', 'Rows', 'SOPClassUID', 'SOPInstanceUID', 'SamplesPerPixel', 
            'SequenceOfUltrasoundRegions', 'SeriesDate', 'SeriesInstanceUID', 'SeriesNumber', 
            'SeriesTime', 'SoftwareVersions', 'StartTrim', 'StationName', 'StopTrim', 'StudyDate', 
            'StudyID', 'StudyInstanceUID', 'StudyTime'
        ]
        
        # Main layout
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()  # to make it horizontal
        self.search_input = QLineEdit()  # to make a field for search
        self.search_input.setPlaceholderText("Enter tag (XXXX,XXXX) or UID")  # written in the field of search
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_tag)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Buttons to choose between limited or all metadata
        self.limited_metadata_button = QPushButton("Show Limited Metadata")
        self.limited_metadata_button.clicked.connect(self.display_limited_metadata)

        self.all_metadata_button = QPushButton("Show All Metadata")
        self.all_metadata_button.clicked.connect(self.display_all_metadata)

        self.replace_two_tag_names = QPushButton("Replace Two Tag Names")
        self.replace_two_tag_names.clicked.connect(self.replace_tag_names)

        # Create two combo boxes for selecting tag names
        self.combo_box1 = QComboBox(self)
        self.combo_box2 = QComboBox(self)

        # Add tag names to both combo boxes
        self.combo_box1.addItems(self.tag_names)
        self.combo_box2.addItems(self.tag_names)

        layout.addWidget(self.limited_metadata_button)
        layout.addWidget(self.all_metadata_button)
        layout.addWidget(self.combo_box1)
        layout.addWidget(self.combo_box2)
        layout.addWidget(self.replace_two_tag_names)

        # Tab widget for original data
        self.tab_widget = QTabWidget()
        self.original_tab = QWidget()
        self.tab_widget.addTab(self.original_tab, "Original Data")

        layout.addWidget(self.tab_widget)

        # Metadata display area
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()

        self.display_limited_metadata()  # Default to limited metadata view

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)  # change the data size
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
#2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
    def replace_tag_names(self):
        # Get the selected tag names from the combo boxes
        tag_name1 = self.combo_box1.currentText()
        tag_name2 = self.combo_box2.currentText()

        print(f"Selected tag_name1: {tag_name1}")
        print(f"Selected tag_name2: {tag_name2}")

        # Initialize values
        value1 = "Not available"
        value2 = "Not available"

        # Check if both tags exist in the dataset
        if tag_name1 in self.dataset:
            value1 = getattr(self.dataset, tag_name1, "Not available")
        if tag_name2 in self.dataset:
            value2 = getattr(self.dataset, tag_name2, "Not available")

        # Replace the values if both tags exist
        if value1 != "Not available" and value2 != "Not available":
            setattr(self.dataset, tag_name1, value2)
            setattr(self.dataset, tag_name2, value1)

            print(f"Replaced {tag_name1} with the value of {tag_name2}: {value2}")
            print(f"Replaced {tag_name2} with the value of {tag_name1}: {value1}")
        else:
            print(f"One or both tags are not available in the dataset.")
        self.display_limited_metadata()

    def display_limited_metadata(self, highlight_query=None):
        """Displays limited set of metadata in the DICOM file."""
        limited_tags = [
            'AccessionNumber', 'ActualFrameDuration', 'BitsAllocated', 'BitsStored', 
            'CineRate', 'Columns', 'ContentDate', 'ContentTime', 'EffectiveDuration', 'FrameDelay', 'FrameIncrementPointer', 
            'FrameTime', 'HeartRate', 'HighBit', 'ImageType', 'InstanceNumber', 'Manufacturer', 'ManufacturerModelName', 'Modality',
              'NumberOfFrames', 'OperatorsName', 'PatientBirthDate', 'PatientBirthTime', 'PatientID', 'PatientName', 'PatientOrientation', 
              'PatientSex', 'PhotometricInterpretation', 'PixelData', 'PixelRepresentation', 'PlanarConfiguration', 'PreferredPlaybackSequencing', 
              'RecommendedDisplayFrameRate', 'ReferringPhysicianName', 'Rows', 'SOPClassUID', 'SOPInstanceUID', 'SamplesPerPixel', 'SequenceOfUltrasoundRegions', 'SeriesDate', 'SeriesInstanceUID', 
             'SeriesNumber', 'SeriesTime', 'SoftwareVersions', 'StartTrim', 'StationName', 'StopTrim', 'StudyDate', 'StudyID', 'StudyInstanceUID', 'StudyTime'
        ]

        # Clear any existing widgets before displaying
        self.clear_metadata_display()

        for tag_name in limited_tags:
            # Get the value of the tag from the dataset (if it exists)
            # print("&&&&&&&&&&&&&&&&&&&&&&&&",tag_name)
           
            # Check if the tag exists in the dataset
            if tag_name in self.dataset:
                # Use getattr to dynamically access the attribute
                value = getattr(self.dataset, tag_name, "Not available")
                print("%%%%%%%%%%%%%%%%%%%%%",f"{tag_name}: {value}")

            # Check if the value is a sequence or binary data and process accordingly
            if isinstance(value, pydicom.sequence.Sequence):
                value = f"Sequence containing {len(value)} items"
            elif isinstance(value, bytes):
                value = f"<Binary Data: {len(value)} bytes>"

            # Highlight matching value if search query exists
            match_found = False
            if highlight_query:
                if highlight_query.lower() in str(value).lower() or highlight_query in tag_name:
                    match_found = True

            # Format the display value with HTML for highlighting
            display_value = f"{value}"
            if match_found:
                display_value = f"<span style='background-color: yellow; font-weight: bold;'>{value}</span>"

            # Add to layout
            entry_label = QLabel(f"<b>{tag_name}:</b> {display_value}")
            entry_label.setWordWrap(True)  # text wrap to be suitable  in displaying
            self.scroll_layout.addWidget(entry_label)
#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
    def display_all_metadata(self, highlight_query=None):
        """Displays all metadata in the DICOM file."""
        # Clear any existing widgets before displaying
        self.clear_metadata_display()
        #  patient Name.dataset , Operators'Name.dataset = Operators'Name.dataset , patient Name.dataset
        # Iterate over all elements in the dataset
        for element in self.dataset:
            tag = f"({element.tag.group:04X},{element.tag.element:04X})"
            name = element.name
            value = element.value

            if isinstance(value, pydicom.sequence.Sequence):
                value = f"Sequence containing {len(value)} items"
            elif isinstance(value, bytes):
                value = f"<Binary Data: {len(value)} bytes>"

            # Check if the query matches any part of the tag, name, or value
            match_found = False
            if highlight_query:
                if highlight_query.lower() in name.lower() or highlight_query in tag:
                    match_found = True

            # Format the display value with HTML for highlighting
            display_value = f"{value}"
            if match_found:
                display_value = f"<span style='background-color: yellow; font-weight: bold;'>{value}</span>"

            entry_label = QLabel(f"<b>{tag} - {name}:</b> {display_value}")
            entry_label.setWordWrap(True)
            self.scroll_layout.addWidget(entry_label)

    def clear_metadata_display(self):
        """Clears the current metadata display before showing new data."""
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def search_tag(self):
        """Search for a specific DICOM tag, keyword or UID and highlight results."""
        query = self.search_input.text().strip()

        if not query:
            return

        try:
            # Check if the query is a valid UID (32 characters)
            if len(query) == 32 and query.isalnum():
                found = False
                for element in self.dataset:
                    if hasattr(element, 'UID') and element.value == query:
                        self.display_all_metadata(highlight_query=query)
                        found = True
                        break

                if not found:
                    self.show_not_found_message(query)
            else:
                # If the query is in the format (XXXX,XXXX), try to interpret it as a tag
                if ',' in query and query.startswith('(') and query.endswith(')'):
                    # Extract the group and element numbers
                    tag_str = query.strip('()')
                    group, element = tag_str.split(',')
                    tag = pydicom.tag.Tag(int(group, 16), int(element, 16))

                    # Search for the tag in the dataset
                    if tag in self.dataset:
                        element = self.dataset.get(tag)
                        value = element.value
                        if isinstance(value, bytes):
                            value = f"<Binary Data: {len(value)} bytes>"
                        self.display_all_metadata(highlight_query=tag_str)  # Highlight the tag
                    else:
                        self.show_not_found_message(query)
                else:
                    # Search by keyword (name)
                    found = False
                    for element in self.dataset:
                        if query.lower() in element.name.lower():
                            self.display_all_metadata(highlight_query=query)
                            found = True
                            break
                    if not found:
                        self.show_not_found_message(query)

        except Exception as e:
            error_label = QLabel(f"Error: {str(e)}")
            self.scroll_layout.addWidget(error_label)
            self.scroll_widget.setLayout(self.scroll_layout)

    def show_not_found_message(self, query):
        """Show a message box if the search result is not found."""
        QMessageBox.warning(self, "Not Found", f"Tag or UID '{query}' not found.")


class DICOMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Setup UI components
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Sliders for image adjustments (window level)
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setRange(0, 100)
        self.slice_slider.setValue(50)
        self.slice_slider.valueChanged.connect(self.update_slice)

        self.slice_label = QLabel("Slice Navigation")

        self.load_button = QPushButton("Load DICOM File", self)
        self.load_button.clicked.connect(self.load_dicom_file)

        self.load_folder_button = QPushButton("Load DICOM Folder", self)
        self.load_folder_button.clicked.connect(self.load_dicom_folder)

        # self.load_button = QPushButton("Replace Two Tag Names", self)
        # self.load_button.clicked.connect(self.replace_tag_names)

        self.view_metadata_button = QPushButton("View Metadata", self)
        self.view_metadata_button.clicked.connect(self.view_metadata)
        self.view_metadata_button.setEnabled(False)

        # Anonymize button
        self.anonymize_button = QPushButton("Anonymize DICOM", self)
        self.anonymize_button.clicked.connect(self.anonymize_dicom)
        self.anonymize_button.setEnabled(False)
        ##000000000000000000000000000000000000000
        self.tiles_button = QPushButton("View Tiles", self)
        self.tiles_button.clicked.connect(self.display_tiles)
        self.tiles_button.setEnabled(False)

        self.load_m2d_button = QPushButton("Load M2D File", self)
        self.load_m2d_button.clicked.connect(self.load_and_play_m2d)

        # New Play/Pause button for M2D video
        self.play_pause_button = QPushButton("Play/Pause", self)
        self.play_pause_button.clicked.connect(self.toggle_m2d_playback)
        self.play_pause_button.setEnabled(False)

        self.timer = QTimer(self)

        # Layout for sliders and controls
        self.controls_layout = QVBoxLayout()
        self.controls_layout.addWidget(self.load_button)
        self.controls_layout.addWidget(self.load_folder_button)
        self.controls_layout.addWidget(self.load_m2d_button)
        self.controls_layout.addWidget(self.play_pause_button)  # Add play/pause button
        self.controls_layout.addWidget(self.view_metadata_button)
        self.controls_layout.addWidget(self.anonymize_button)
        self.controls_layout.addWidget(self.slice_label)
        self.controls_layout.addWidget(self.slice_slider)
        self.controls_layout.addWidget(self.tiles_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.image_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.dicom_files = []
        self.dicom_array = None
        self.dataset = None
        self.current_slice_index = 0
        self.m2d_frames = None
        self.current_frame_index = 0
        self.is_m2d_playing = False  # Track play/pause state

        self.apply_styles()

    def apply_styles(self):
        """Apply color styling to the main window."""
        self.setStyleSheet(""" 
            QMainWindow {
                background-color: #f0f8ff; 
            }

            QLabel {
                font-size: 14px;
                color: #333333;
            }

            QPushButton {
                background-color: #008CBA;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }

            QPushButton:hover {
                background-color: #005f73;
            }

            QPushButton:pressed {
                background-color: #003f4d;
            } 
        """)
    

    def load_dicom_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm)")
        if file_path:
            self.dataset = pydicom.dcmread(file_path)
            self.dicom_array = [self.dataset.pixel_array]
            self.dicom_files = [file_path]
            self.current_slice_index = 0
            self.view_metadata_button.setEnabled(True)
            self.anonymize_button.setEnabled(True)
            self.update_image()
            self.tiles_button.setEnabled(True)

    def load_dicom_folder(self):
        """Loads a folder of DICOM files, processes them, and updates the display."""

        # Clear previous data and reset UI elements
        if hasattr(self, 'dicom_array') and self.dicom_array is not None:
            self.dicom_array = []
            self.dicom_files = []
            self.current_slice_index = 0
            self.dataset = None
            if hasattr(self, 'timer') and self.timer.isActive():
                self.timer.stop()
            self.image_label.clear()  # Clear the previous image from the display

        # Open folder dialog to select a DICOM folder
        folder_path = QFileDialog.getExistingDirectory(self, "Open DICOM Folder")
        if folder_path:
            # Get all DICOM files in the selected folder
            dicom_files = [
                os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".dcm")
            ]
            if not dicom_files:
                return  # No DICOM files found in the selected folder

            # Read all DICOM files and extract pixel data
            self.dicom_files = dicom_files
            self.dicom_array = [pydicom.dcmread(f).pixel_array for f in dicom_files]

            # Set the dataset to the first file's data
            self.dataset = pydicom.dcmread(self.dicom_files[0])
            self.current_slice_index = 0

            # Enable metadata and anonymization buttons
            self.view_metadata_button.setEnabled(True)
            self.anonymize_button.setEnabled(True)

            # Update the display with the first slice
            self.update_image()

            # Enable the tiles button
            self.tiles_button.setEnabled(True)

    def view_metadata(self):
        if self.dataset:
            metadata_viewer = MetadataViewer(self.dataset, self)
            metadata_viewer.exec_()

    def update_slice(self):
        """Update the slice navigation when the slider is changed."""
        if self.dicom_array:
            index = int(self.slice_slider.value() / 100 * (len(self.dicom_array) - 1))
            self.current_slice_index = max(0, min(index, len(self.dicom_array) - 1))
            self.update_image()

    def update_image(self):
        if self.dicom_array:
            # Get the current slice (without brightness/contrast adjustments)
            image = self.dicom_array[self.current_slice_index]

            # Normalize to 8-bit image (0-255)
            image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)

            height, width = image.shape
            qimage = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
            self.image_label.setPixmap(QPixmap.fromImage(qimage))

    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    def anonymize_dicom(self):
        """Anonymize the DICOM files by replacing sensitive information with random values and save them to a new folder."""
        if not self.dicom_files:
            QMessageBox.warning(self, "No Files Loaded", "Please load DICOM files before anonymizing.")
            return

        # Ask the user for a prefix to anonymize with
        prefix, ok = QInputDialog.getText(self, "Enter Prefix", "Enter a prefix for anonymization:")
        if not ok or not prefix:
            QMessageBox.warning(self, "No Prefix", "Please enter a prefix for anonymization.")
            return

        # List of fields to anonymize
        fields_to_anonymize = [
            "PatientName", "PatientID", "AccessionNumber", "StudyID", "InstitutionName"
        ]

        # Ask the user to select a directory to save the anonymized files
        save_folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Anonymized Files")
        if not save_folder:
            return

        # Create a new folder for anonymized files
        anonymized_folder = os.path.join(save_folder, "Anonymized")
        if not os.path.exists(anonymized_folder):
            os.makedirs(anonymized_folder)

        anonymized_files = []

        # Handle both single frame and multi-frame DICOM files
        files_to_process = self.dicom_files if self.dicom_files else [self.dataset.filename]
        for dicom_file in files_to_process:
            # 00000000000000000000000000000000000000000000000000000000
            # Load the DICOM dataset
            dataset = pydicom.dcmread(dicom_file)

            # Anonymize the relevant fields
            for field in fields_to_anonymize:
                if hasattr(dataset, field):
                    random_value = f"{prefix}{random.randint(1000, 9999)}"
                    setattr(dataset, field, random_value)

            # Get the filename and construct the new path in the anonymized folder
            file_name = os.path.basename(dicom_file)
            anonymized_file_path = os.path.join(anonymized_folder, f"anon_{file_name}")

            # Save the anonymized file
            dataset.save_as(anonymized_file_path)
            anonymized_files.append(anonymized_file_path)

        # Update the class attributes if needed
        if hasattr(self, 'm2d_frames') and self.m2d_frames is not None:
            self.dicom_files = anonymized_files
            self.dataset = pydicom.dcmread(anonymized_files[0])
        # 0000000000000000000000000000000000000000000
        # Inform the user that anonymization is complete
        QMessageBox.information(self, "Anonymization Complete", f"Anonymized files saved to:\n{anonymized_folder}")

    def display_tiles(self):
        """Displays all slices in a grid layout."""
        if not self.dicom_array:
            QMessageBox.warning(self, "No Data", "Please load DICOM data first.")
            return

        # Create a new dialog for the tiles view
        tiles_dialog = QDialog(self)
        tiles_dialog.setWindowTitle("DICOM Tiles View")
        tiles_dialog.resize(800, 600)

        scroll_area = QScrollArea(tiles_dialog)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        grid_layout = QVBoxLayout()

        # Number of columns for the grid
        columns = 6
        row_layout = None

        for i, slice_data in enumerate(self.dicom_array):

            # Normalize the slice data to 8-bit grayscale
            image = ((slice_data - slice_data.min()) / (slice_data.max() - slice_data.min()) * 255).astype(np.uint8)
            height, width = image.shape
            qimage = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)

            slice_label = QLabel()
            slice_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            slice_label.setAlignment(Qt.AlignCenter)
            # 00000000000000000000000000000000000000000000000000000000000
            # Create a new row if necessary
            if i % columns == 0:
                if row_layout:
                    grid_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()

            # Add the slice to the current row
            row_layout.addWidget(slice_label)

        # Add the last row to the layout
        if row_layout:
            grid_layout.addLayout(row_layout)

        scroll_widget.setLayout(grid_layout)
        scroll_area.setWidget(scroll_widget)

        dialog_layout = QVBoxLayout(tiles_dialog)
        dialog_layout.addWidget(scroll_area)
        tiles_dialog.setLayout(dialog_layout)
        tiles_dialog.exec_()

    def load_and_play_m2d(self):
        """Loads a multi-frame DICOM (M2D) file, displays it as a video, and allows metadata extraction."""

        # Clear previous frames and reset UI elements
        if hasattr(self, 'm2d_frames') and self.m2d_frames is not None:
            self.m2d_frames = None
            self.current_frame_index = 0
            if hasattr(self, 'timer') and self.timer.isActive():
                self.timer.stop()
            self.image_label.clear()  # Clear the previous image from the display

        # Open file dialog to select a DICOM file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Multi-frame DICOM File", "", "DICOM Files (*.dcm)")
        if not file_path:
            return  # User canceled file selection

        try:
            # Read the DICOM file
            dataset = pydicom.dcmread(file_path)

            # Check for valid pixel data
            if not hasattr(dataset, "pixel_array"):
                QMessageBox.warning(self, "Invalid File", "The selected file does not contain valid pixel data.")
                return

            # Handle both single and multi-frame DICOM files
            frames = dataset.pixel_array
            if len(frames.shape) < 3:
                # For single-frame images, create a single frame array
                frames = frames[np.newaxis, ...]

            # Set up for playback
            self.dataset = dataset
            self.dicom_files = [file_path]  # Update this to support anonymization
            self.m2d_frames = frames
            self.current_frame_index = 0
            self.is_m2d_playing = True  # Start playing by default

            # Set up timer
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_m2d_frame)
            self.timer.start(1000 // 24)  # Play at 24 FPS

            # Update display with the first frame
            self.update_m2d_frame()

            # Enable metadata viewing, anonymization, and play/pause buttons
            self.view_metadata_button.setEnabled(True)
            self.anonymize_button.setEnabled(True)
            self.play_pause_button.setEnabled(True)

        except AttributeError as e:
            QMessageBox.critical(self, "Error", f"Failed to read pixel data: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load DICOM file: {str(e)}")

    def update_m2d_frame(self):
        """Updates the display to show the current frame of the M2D file."""
        if not hasattr(self, 'm2d_frames') or self.m2d_frames is None or not self.is_m2d_playing:
            return

        # Get the current frame
        frame = self.m2d_frames[self.current_frame_index]

        # Handle frames with more than two dimensions (e.g., RGB or multi-channel images)
        if len(frame.shape) == 3:  # e.g., (rows, cols, channels)
            frame = frame[..., 0]  # Take the first channel (assuming grayscale data)

        # Normalize to 8-bit image (0-255)
        frame = ((frame - frame.min()) / (frame.max() - frame.min()) * 255).astype(np.uint8)

        # Convert to QImage and display
        height, width = frame.shape
        qimage = QImage(frame.data, width, height, width, QImage.Format_Grayscale8)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))

        # Update frame index for the next iteration
        self.current_frame_index = (self.current_frame_index + 1) % len(self.m2d_frames)

    def toggle_m2d_playback(self):
        """Toggle play/pause for M2D video playback."""
        if not hasattr(self, 'm2d_frames') or self.m2d_frames is None:
            return

        # Toggle play/pause state
        self.is_m2d_playing = not self.is_m2d_playing

        if self.is_m2d_playing:
            # If changing from paused to playing, restart the timer
            if not self.timer.isActive():
                self.timer.start(1000 // 24)
        else:
            # If pausing, stop the timer
            self.timer.stop()


if __name__ == "__main__":  # Corrected
    app = QApplication(sys.argv)
    window = DICOMViewer()
    window.show()
    sys.exit(app.exec_())