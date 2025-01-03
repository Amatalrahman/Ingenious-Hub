# Medical Image Classification

## Overview
This project focuses on developing an AI model to classify the main organs in medical images, including:
- **Heart**
- **Brain**
- **Liver**
- **Limbs**

## Approach
1. **Data Preparation**:
   - Gather labeled medical image datasets.
   - Preprocess images (resizing, normalization, augmentation).
   
2. **Model Development**:
   - Build a custom AI classification model.
   - Train and validate the model using the dataset.
   
3. **Evaluation**:
   - Measure the model's accuracy, precision, recall, and F1 score.
   - Test the model on unseen data to ensure robustness.

4. **Future Enhancements**:
   - Incorporate more organ categories.
   - Fine-tune the model for higher accuracy.

## Prerequisites
- Python 3.8+
- TensorFlow or PyTorch (depending on the classification model)
- OpenCV

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medical-classification.git
   cd medical-classification
   ```

## Usage
1. Train the model:
   ```bash
   python train_model.py
   ```
2. Test the model on new images:
   ```bash
   python test_model.py --image_path /path/to/image
   ```
## 🎥 Demonstration Video  
To better understand the application's features and functionality, watch the demonstration video here:  

[![Watch the Video](https://img.shields.io/badge/Watch-Demo%20Video-blue?style=for-the-badge&logo=youtube)](https://drive.google.com/file/d/10Oytu-hFmUK7M7d6o4Q3U-Umv4bUAU1e/view?usp=drivesdk)  


## Project Structure
```
├── train_model.py
├── test_model.py
├── data/
├── models/
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
