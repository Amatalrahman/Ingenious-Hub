import sys
import SimpleITK as sitk
import numpy as np
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout,
    QWidget, QPushButton, QLabel, QSlider, QComboBox, QGridLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt


class ITKSNAPClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ITK-SNAP Clone")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("Background-color: grey;")

        # Image settings
        self.image = None
        self.array = None
        self.current_slice_index = None
        self.image_color_map = 'gray'
        self.points = []

        # Store brightness, contrast, and zoom for each view
        self.view_settings = {
            'axial': {'brightness': 50, 'contrast': 50, 'zoom': 50},
            'coronal': {'brightness': 50, 'contrast': 50, 'zoom': 50},
            'sagittal': {'brightness': 50, 'contrast': 50, 'zoom': 50},
        }

        # UI setup
        self.initUI()

    def initUI(self):
        # Buttons
        self.load_button = QPushButton("Load Medical Image")
        self.load_button.clicked.connect(self.load_image)

        self.show_3d_button = QPushButton("Generate 3D Model")
        self.show_3d_button.clicked.connect(self.display_3d)

        self.color_map_selector = QComboBox()
        self.color_map_selector.addItems(['gray', 'jet', 'hot', 'cool'])
        self.color_map_selector.currentTextChanged.connect(self.change_image_color_map)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.vtk_renderer)

        # Slice slider
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.valueChanged.connect(self.update_slice_index)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.show_3d_button)
        layout.addWidget(self.color_map_selector)
        layout.addWidget(QLabel("Slice:"))
        layout.addWidget(self.slice_slider)

        # Create a grid layout for views and their sliders
        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Axial View"), 0, 0)
        grid_layout.addWidget(QLabel("Brightness"), 1, 0)
        self.axial_brightness_slider = self.create_slider('Axial Brightness', 'axial')
        grid_layout.addWidget(self.axial_brightness_slider, 1, 1)

        grid_layout.addWidget(QLabel("Contrast"), 2, 0)
        self.axial_contrast_slider = self.create_slider('Axial Contrast', 'axial')
        grid_layout.addWidget(self.axial_contrast_slider, 2, 1)

        grid_layout.addWidget(QLabel("Zoom"), 3, 0)
        self.axial_zoom_slider = self.create_slider('Axial Zoom', 'axial')
        grid_layout.addWidget(self.axial_zoom_slider, 3, 1)

        # Coronal view
        grid_layout.addWidget(QLabel("Coronal View"), 0, 2)
        grid_layout.addWidget(QLabel("Brightness"), 1, 2)
        self.coronal_brightness_slider = self.create_slider('Coronal Brightness', 'coronal')
        grid_layout.addWidget(self.coronal_brightness_slider, 1, 3)

        grid_layout.addWidget(QLabel("Contrast"), 2, 2)
        self.coronal_contrast_slider = self.create_slider('Coronal Contrast', 'coronal')
        grid_layout.addWidget(self.coronal_contrast_slider, 2, 3)

        grid_layout.addWidget(QLabel("Zoom"), 3, 2)
        self.coronal_zoom_slider = self.create_slider('Coronal Zoom', 'coronal')
        grid_layout.addWidget(self.coronal_zoom_slider, 3, 3)

        # Sagittal view
        grid_layout.addWidget(QLabel("Sagittal View"), 0, 4)
        grid_layout.addWidget(QLabel("Brightness"), 1, 4)
        self.sagittal_brightness_slider = self.create_slider('Sagittal Brightness', 'sagittal')
        grid_layout.addWidget(self.sagittal_brightness_slider, 1, 5)

        grid_layout.addWidget(QLabel("Contrast"), 2, 4)
        self.sagittal_contrast_slider = self.create_slider('Sagittal Contrast', 'sagittal')
        grid_layout.addWidget(self.sagittal_contrast_slider, 2, 5)

        grid_layout.addWidget(QLabel("Zoom"), 3, 4)
        self.sagittal_zoom_slider = self.create_slider('Sagittal Zoom', 'sagittal')
        grid_layout.addWidget(self.sagittal_zoom_slider, 3, 5)

        layout.addLayout(grid_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.vtk_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Mouse settings
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def create_slider(self, label_text, view):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.valueChanged.connect(lambda value: self.update_setting(view, label_text, value))
        return slider

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "NIfTI Files (*.nii *.nii.gz);;DICOM Files (*.dcm)")
        if file_name:
            try:
                self.image = sitk.ReadImage(file_name)
                self.array = sitk.GetArrayFromImage(self.image)
                self.current_slice_index = self.array.shape[0] // 2
                self.slice_slider.setRange(0, self.array.shape[0] - 1)
                self.slice_slider.setValue(self.current_slice_index)
                self.display_slices()
            except Exception as e:
                print(f"Error loading image: {e}")

    def display_slices(self):
        if self.array is not None:
            self.figure.clear()
            axs = self.figure.subplots(1, 3)
            self.plot_slice(axs[0], self.array[self.current_slice_index, :, :], 'Axial', 'axial')
            self.plot_slice(axs[1], self.array[:, self.current_slice_index, :], 'Coronal', 'coronal')
            self.plot_slice(axs[2], self.array[:, :, self.current_slice_index], 'Sagittal', 'sagittal')
            self.canvas.draw()

    def plot_slice(self, ax, slice_data, title, view):
        adjusted_slice = self.adjust_brightness_contrast(slice_data, view)
        ax.clear()
        ax.imshow(adjusted_slice, cmap=self.image_color_map, aspect='auto')
        ax.set_title(title)
        ax.axis('off')

        # Centered zoom functionality
        center_x = slice_data.shape[1] / 2
        center_y = slice_data.shape[0] / 2

        zoom_factor = 0.5 + (self.view_settings[view]['zoom'] / 100.0) * 1.5  # Adjust zoom range
        ax.set_xlim(center_x - (slice_data.shape[1] / zoom_factor) / 2,
                    center_x + (slice_data.shape[1] / zoom_factor) / 2)
        ax.set_ylim(center_y + (slice_data.shape[0] / zoom_factor) / 2,
                    center_y - (slice_data.shape[0] / zoom_factor) / 2)

        for point in self.points:
            ax.plot(point[1], point[0], 'rx', markersize=5)

    def adjust_brightness_contrast(self, slice_data, view):
        brightness_adjusted = (self.view_settings[view]['brightness'] - 50) / 50.0
        contrast_adjusted = (self.view_settings[view]['contrast'] - 50) / 50.0
        slice_data = np.clip(slice_data, 0, 255).astype(np.float32)
        slice_data += brightness_adjusted * 255
        slice_data = 255 * (slice_data / 255) ** (1 + contrast_adjusted)
        return np.clip(slice_data, 0, 255)

    def update_slice_index(self, value):
        self.current_slice_index = value
        self.display_slices()

    def update_setting(self, view, setting_name, value):
        self.view_settings[view][setting_name.split(' ')[1].lower()] = value
        self.display_slices()

    def change_image_color_map(self, color_map):
        self.image_color_map = color_map
        self.display_slices()

    def on_click(self, event):
        if event.inaxes is not None:
            x = int(event.ydata)
            y = int(event.xdata)
            if 0 <= x < self.array.shape[0] and 0 <= y < self.array.shape[1]:
                if event.button == 1:  # Left click
                    self.points.append((x, y))
                elif event.button == 3:  # Right click
                    if self.points:
                        self.points.pop()  # Remove latest point
                self.display_slices()

    def display_3d(self):
        if self.array is not None:
            vtk_data = vtk.vtkImageData()
            vtk_data.SetDimensions(self.array.shape)
            vtk_data.SetSpacing([1.0, 1.0, 1.0])

            flat_data = self.array.ravel(order='F')
            vtk_array = vtk.vtkFloatArray()
            vtk_array.SetNumberOfValues(len(flat_data))
            for i, value in enumerate(flat_data):
                vtk_array.SetValue(i, value)
            vtk_data.GetPointData().SetScalars(vtk_array)

            # Marching Cubes for 3D model generation
            marching_cubes = vtk.vtkMarchingCubes()
            marching_cubes.SetInputData(vtk_data)
            marching_cubes.SetValue(0, 100)  # Adjust isosurface value as needed

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(marching_cubes.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            self.vtk_renderer.RemoveAllViewProps()
            self.vtk_renderer.AddActor(actor)
            self.vtk_renderer.ResetCamera()
            self.vtk_widget.GetRenderWindow().Render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ITKSNAPClone()
    viewer.show()
    sys.exit(app.exec_())
