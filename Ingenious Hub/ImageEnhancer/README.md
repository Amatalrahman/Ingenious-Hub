
# Image Viewer Application

This project is an image viewer application that allows users to view, modify, and analyze grayscale images. The application supports various functionalities such as zooming, applying noise and denoising techniques, measuring Signal-to-Noise Ratio (SNR) and Contrast-to-Noise Ratio (CNR), and enhancing images using filters.

## Features & Requirements

### Image Viewport
- **View and Manipulate Images**:
  - Open and view a 2D image in a single input viewport.
  - Modify the image and see the result in one of two available output viewports.
  - Apply multiple changes in sequence: first on the input image, then on the output image from the previous step.

### Histogram Functionality
- The histogram of each image (input and output) is updated dynamically every time the user applies a modification to the image.

### Image Operations
- **Resolution Adjustment**: 
  - The user can specify the zoom factor they want to apply to the image.
  - Different interpolation methods are available when zooming:
    - Nearest-neighbor
    - Linear
    - Bilinear
    - Cubic
- **SNR (Signal-to-Noise Ratio)**:
  - Measure the SNR by selecting two Regions of Interest (ROIs) and calculating the average intensities in those regions.
  - Apply 3 types of noise to the image:
    - Gaussian noise
    - Salt and pepper noise
    - Poisson noise
  - Apply 3 types of denoising filters/techniques to the noisy image:
    - Median filter
    - Gaussian blur
    - Bilateral filter
- **CNR (Contrast-to-Noise Ratio)**:
  - Adjust the brightness and contrast of the image.
  - Apply 3 different contrast adjustment techniques to improve CNR:
    - Histogram Equalization
    - CLAHE (Contrast Limited Adaptive Histogram Equalization)
    - **Gamma Correction** (Contrast adjustment using gamma values)
  - **Custom Contrast Adjustment** (A technique developed for contrast improvement beyond standard methods)

## Getting Started

### Prerequisites
To run the project, ensure you have the following installed:
- Python 3.x (recommended version: 3.8+)
- Required Python packages:
  - `numpy`
  - `matplotlib`
  - `opencv-python`
  - `scipy`
  - `Pillow`

You can install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/image-viewer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd image-viewer
   ```
3. Launch the application:
   ```bash
   python main.py
   ```

### Usage
- Open a grayscale image file using the **Open Image** button.
- Specify the zoom factor you want to apply to the image using the **Zoom Factor** input.
- Apply noise or denoising techniques using the corresponding buttons.
- The histogram is updated in real-time with every change applied to the image.
- Adjust the image's brightness, contrast, and apply filters through the user interface.

## Example Images
Make sure to have different grayscale images ready to test the application. Sample images can be placed in the `images/` folder in the project directory.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Structure of the Project:

- `main.py`: Main application code for the image viewer.
- `requirements.txt`: List of Python packages required to run the application.
- `images/`: Folder containing sample grayscale images for testing.
- `docs/`: Documentation folder with detailed explanations for each feature.

