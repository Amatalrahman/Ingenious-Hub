from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np
from tkinter import Tk, Label, Button, filedialog
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# Define image size and class labels
IMAGE_SIZE = (150, 150)
class_labels = ['brain', 'heart', 'limbs', 'liver']

# Load data function
def load_data():
    train_datagen = ImageDataGenerator(
        rescale=1.0/255.0,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    train_generator = train_datagen.flow_from_directory(
        r'G:\dataset',  # Update this path
        target_size=IMAGE_SIZE,
        batch_size=64,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        r'G:\dataset',  # Same path
        target_size=IMAGE_SIZE,
        batch_size=64,
        class_mode='categorical',
        subset='validation'
    )

    return train_generator, validation_generator

# Build model function
def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(class_labels), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Train model function
def train_model():
    train_generator, validation_generator = load_data()
    global model  # Make the model accessible globally
    model = build_model()
    model.fit(train_generator, validation_data=validation_generator, epochs=10)
    model.save('modell.h5')  # This saves both the architecture and weights



# Predict function
def predict_image(image_path):
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img) / 255.0  # Normalize  # range from 1 to -1
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    #model.load_weights('finalmodel.weights.h5')
    predictions = model.predict(img_array) # takes the image and predicts #same parameter as model fit
    predicted_class = class_labels[np.argmax(predictions)] # probabilities of prediction # outputs the highest possibility (argmax)
                                                           # takes the index of the class

    # Display the image and prediction
    plt.figure(figsize=(6, 4))
    plt.imshow(img)
    plt.title(f'Predicted: {predicted_class}')
    plt.axis('off')
    plt.show()

# GUI Setup
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        predict_image(file_path)  # Call the prediction function

root = Tk()
root.title("Organ Classifier")
label = Label(root, text="Choose an image to classify:")
label.pack()
button = Button(root, text="Open File", command=open_file)
button.pack()

# Start training the model
train_model()  # Call this only once, when you want to train the model

root.mainloop()
