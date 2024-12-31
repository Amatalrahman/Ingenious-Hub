import os
import numpy as np
from tkinter import Tk, Label, Button, filedialog, font, Frame, Toplevel
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score
from PIL import Image, ImageTk

# Define image size and class labels
IMAGE_SIZE = (150, 150)
class_labels = ['brain', 'heart', 'limbs', 'liver']


def extract_true_label(img_name):
    return img_name.split('_')[0]  # Adjust based on your actual filename format


def show_incorrect_predictions(incorrect_images):
    if incorrect_images:
        window = Toplevel(root)
        window.title("Incorrect Predictions")
        window.geometry("600x400")

        for img_name in incorrect_images:
            img_path = os.path.join(folder_path, img_name)
            img = Image.open(img_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)

            img_label = Label(window, image=img_tk)
            img_label.image = img_tk  # Keep a reference
            img_label.pack(side="left", padx=5, pady=5)

        Label(window, text="Incorrect Predictions", font=font.Font(size=16)).pack(pady=10)


def predict_images_in_folder(folder_path, result_label, status_label):
    model = load_model('modell.h5')
    true_labels = []
    predictions = []
    incorrect_images = []

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            true_label = extract_true_label(img_name)
            if true_label in class_labels:
                true_labels.append(class_labels.index(true_label))

                img = image.load_img(img_path, target_size=IMAGE_SIZE)
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                pred = np.argmax(model.predict(img_array))
                predictions.append(pred)

                # Check if the prediction is incorrect
                if pred != class_labels.index(true_label):
                    incorrect_images.append(img_name)

    if true_labels and predictions:
        accuracy = accuracy_score(true_labels, predictions)
    else:
        accuracy = 0

    result_label.config(text=f'Accuracy: {accuracy * 100:.2f}%', fg='green')
    status_label.config(text="Prediction completed!", fg="green")

    # Show incorrect predictions
    show_incorrect_predictions(incorrect_images)


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

    # Display the image in the GUI
    img_for_display = Image.open(image_path).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_for_display)
    img_label.config(image=img_tk)
    img_label.image = img_tk  # Keep a reference to prevent garbage collection


def open_folder(result_label, status_label):
    global folder_path  # Use a global variable to access it later
    folder_path = filedialog.askdirectory()
    if folder_path:
        status_label.config(text="Processing images...", fg="blue")
        predict_images_in_folder(folder_path, result_label, status_label)


def open_image(result_label, img_label, status_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        status_label.config(text="Processing image...", fg="blue")
        predict_single_image(file_path, result_label, img_label, status_label)


# GUI Setup
root = Tk()
root.title("Organ Classifier")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

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
button_folder = Button(title_frame, text="Open Folder of Images",
                       command=lambda: open_folder(result_label, status_label),
                       font=button_font, bg='#007BFF', fg='white', padx=10, pady=5)
button_folder.pack(pady=10)

# Button to open a single image
button_image = Button(title_frame, text="Open Single Image",
                      command=lambda: open_image(result_label, img_label, status_label),
                      font=button_font, bg='#28A745', fg='white', padx=10, pady=5)
button_image.pack(pady=10)

# Result label to show prediction
result_label = Label(result_frame, text="Prediction will appear here", font=label_font, bg='#f0f0f0', fg='green')
result_label.pack()

# Status label to show loading state
status_label = Label(status_frame, text="Select a folder or an image to classify", font=label_font, bg='#f0f0f0',
                     fg='black')
status_label.pack()

# Image preview label (initially empty)
img_label = Label(result_frame, bg='#f0f0f0', width=200, height=200, borderwidth=2, relief="groove")
img_label.pack()

root.mainloop()

