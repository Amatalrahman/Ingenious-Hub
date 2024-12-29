# Multi-Planar Image Viewer

This project is a multi-planar image viewer designed to display and interact with 3D medical images. The application provides navigation, image manipulation, and cross-referencing features to enhance the analysis of volumetric data.

## Features

### 1. Multi-Planar Viewports
- **3 Viewers:** Displays three orthogonal planes (axial, coronal, sagittal) of the 3D image volume simultaneously.

### 2. Basic Navigation Features
- **Scroll Through Slices:** Navigate through image slices in each viewport using the mouse or keyboard.
- **Cine Play/Pause/Stop:** Enable cine mode for dynamic scrolling through slices.
- **Slice Indicator:** Highlights the current slice location in the other planar viewers.

### 3. Basic Image Manipulation Features
- **Zoom:** Zoom in and out of images using mouse wheel or gestures.
- **Brightness and Contrast:** Adjust brightness and contrast interactively using the mouse. These adjustments are directly reflected in all relevant 2D viewers, enhancing image analysis.

### 4. 3D Point Mapping
- **Single Point Localization:** Specify a point in the 3D volume and visualize its corresponding location in each 2D viewport. This allows for precise cross-referencing and analysis of specific areas within the volume.

### 5. 3D Module
- **3D Volume Rendering:** Generate and interact with a 3D model of the image volume for comprehensive visualization. 
- **Integration with 2D Viewers:** Cross-reference the 3D model with the 2D slices for enhanced analysis. The 3D model offers rotational and zoom capabilities, providing an intuitive understanding of the spatial relationships within the data.

## Requirements

### Hardware
- A computer capable of running Python and required libraries.
- A mouse or trackpad for navigation and interaction.

### Software
- **Python (3.10 or later)**
- Required libraries:
  - Numpy
  - Matplotlib
  - PyQt5 (or similar GUI framework)
  - VTK (Visualization Toolkit)
  - Pydicom (if working with DICOM images)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/multi_planar_viewer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd multi_planar_viewer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Launch the application:
   ```bash
   python main.py
   ```
2. Load a 3D medical image volume (e.g., DICOM series).
3. Use the following features to analyze the data:
   - Adjust brightness and contrast interactively.
   - Scroll through slices or enable cine mode in any viewer.
   - View the spatial position of a single 3D point across 2D viewers.
   - Explore the 3D model with rotation, zoom, and cross-referencing capabilities.

## Controls
- **Scroll Through Slices:** Use the mouse wheel or arrow keys.
- **Cine Mode:** Use play/pause/stop buttons.
- **Zoom:** Scroll the mouse wheel while holding `Ctrl`.
- **Brightness and Contrast:** Drag the mouse while holding `Shift`.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to the branch.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
This project leverages the power of VTK and PyQt5 for rendering and interactivity. Special thanks to the open-source community for providing tools and libraries to facilitate medical imaging development.

---
Feel free to contact us for any questions or suggestions!

