import os
import numpy as np
from tkinter import Tk, Label, Button, filedialog, font, Frame
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score
from PIL import Image, ImageTk

# Define image size and class labels
IMAGE_SIZE = (150, 150)
class_labels = ['brain', 'heart', 'limbs', 'liver']

def extract_true_label(img_name):
    # Extract the true label from the filename
    # Assuming filenames are in the format "label_some_other_text.jpg"
    return img_name.split('_')[0]  # Adjust based on your actual filename format

def predict_images_in_folder(folder_path, result_label, status_label):
    model = load_model('modell.h5')
    true_labels = []
    predictions = []

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        # Check if the file is an image
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Extract true label from the image filename
            true_label = extract_true_label(img_name)
            if true_label in class_labels:
                true_labels.append(class_labels.index(true_label))  # Convert label to index

                # Load and process the image
                img = image.load_img(img_path, target_size=IMAGE_SIZE)
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Make a prediction
                predictions.append(np.argmax(model.predict(img_array)))

    # Calculate accuracy
    if true_labels and predictions:  # Ensure both lists are not empty
        accuracy = accuracy_score(true_labels, predictions)
    else:
        accuracy = 0

    result_label.config(text=f'Accuracy: {accuracy * 100:.2f}%', fg='green')
    status_label.config(text="Prediction completed!", fg="green")

def open_folder(result_label, status_label):
    folder_path = filedialog.askdirectory()
    if folder_path:
        status_label.config(text="Processing images...", fg="blue")
        predict_images_in_folder(folder_path, result_label, status_label)

# GUI Setup
root = Tk()
root.title("Organ Classifier")
root.geometry("800x600")  # Width x Height in pixels
root.configure(bg='#f0f0f0')  # Light gray background

# Create custom fonts
title_font = font.Font(size=20, weight='bold')
label_font = font.Font(size=16)
button_font = font.Font(size=14)

# Create frames for layout
title_frame = Frame(root, bg='#f0f0f0')
title_frame.pack(pady=20)

result_frame = Frame(root, bg='#f0f0f0')
result_frame.pack(pady=10)

status_frame = Frame(root, bg='#f0f0f0')
status_frame.pack(pady=10)

# Title Label
title_label = Label(title_frame, text="Organ Classification from Images", font=title_font, bg='#f0f0f0')
title_label.pack()

# Button to open folder
button = Button(title_frame, text="Open Folder of Images", command=lambda: open_folder(result_label, status_label),
                font=button_font, bg='#007BFF', fg='white', padx=10, pady=5)
button.pack(pady=10)

# Result label to show prediction accuracy
result_label = Label(result_frame, text="Accuracy will appear here", font=label_font, bg='#f0f0f0', fg='green')
result_label.pack()

# Status label to show loading state
status_label = Label(status_frame, text="Select a folder to classify images", font=label_font, bg='#f0f0f0', fg='black')
status_label.pack()

root.mainloop()





def predict_single_image(image_path, result_label, img_label, status_label):
    model = load_model('modell.h5')
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = np.argmax(model.predict(img_array))
    predicted_label = class_labels[prediction]

    # Update the result label and display the image
    result_label.config(text=f'This organ is a {predicted_label}', fg='green')
    status_label.config(text="Prediction completed!", fg="green")