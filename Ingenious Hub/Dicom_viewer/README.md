# DICOM Viewer 

## Overview

This project involves creating a custom DICOM viewer with advanced features for viewing, exploring, and anonymizing DICOM files. The viewer will support 2D, M2D, and 3D DICOM images and offer functionality for interacting with DICOM metadata. This README outlines the project's requirements, features, and usage instructions.

---

## Requirements

Before developing the DICOM viewer, it is recommended to explore existing free DICOM viewers to understand their features and interfaces:

### Popular Free DICOM Viewers:

- **[RadiAnt](https://www.radiantviewer.com/)**
- **[MicroDicom](https://www.microdicom.com/)**
- **[IMAIOS](https://www.imaios.com/)**
- **[ezDICOM](http://www.ezdicom.com/)** (Open-source code available)
- **[OsiriX](https://www.osirix-viewer.com/)** (Famous for Apple OS)



---

## Project Goals

Develop a DICOM viewer that supports the following features:

### 1. File Support

- Open any DICOM file containing 2D, M2D, or 3D images.

### 2. Image Display

- For **2D images**: Display images as static.
- For **M2D images**: Display images as a video.
- For **3D images**: Display images as tiles or allow 3D exploration.

### 3. DICOM Tags Exploration

Provide users with multiple ways to explore DICOM metadata:

- **View All Tags**: Display all DICOM tags in the file along with their values.
- **Search Tags**: Allow users to search for a specific DICOM tag and display its value.
- **Group Exploration**: Explore values of main DICOM elements categorized by groups:
  - Patient
  - Study
  - Modality
  - Physician
  - Image

### 4. Anonymization

- Enable users to anonymize the DICOM file by replacing sensitive information with randomized values.
- Allow users to specify a prefix for anonymized values.

---

## Features

1. **User-Friendly Interface:** Intuitive and accessible UI for exploring and interacting with DICOM files.
2. **Metadata Exploration:** Seamlessly browse and search DICOM tags and categories.
3. **Image Display:** Efficient rendering of 2D, M2D, and 3D DICOM images.
4. **Anonymization Tools:** Protect sensitive patient information with customizable anonymization options.

---

## Setup & Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/dicom-viewer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd dicom-viewer
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

1. Launch the DICOM viewer application.
2. Use the file browser to load a DICOM file.
3. Navigate through the following features:
   - **Image Display:** View 2D, M2D, or 3D images as appropriate.
   - **Tags Exploration:** Explore all tags, search specific tags, or explore by category.
   - **Anonymization:** Anonymize the DICOM file with customizable prefix options.

---

## Contribution

We welcome contributions to enhance this DICOM viewer. If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Special thanks to the developers of the existing DICOM viewers for inspiration and to the community for their feedback and support.

