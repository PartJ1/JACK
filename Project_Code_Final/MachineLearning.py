import os
import numpy as np
import cv2

from tensorflow.keras import layers, models
import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np
from scipy import stats
import cv2

import time
import matplotlib.pyplot as plt


def train_model(x, y, filepath, progress, epoch, root, num_students):
    model = load_model(filepath)

    img_height = 200
    img_width = 200

    print(x.shape)
    print(y.shape)
    print(x)
    print(y)

    # Create a new Sequential model up to the second-to-last layer
    new_model = models.Sequential()

    for layer in model.layers[:-1]:  # Exclude the last layer
        new_model.add(layer)

    # Add the new Dense layer
    print("num of students", num_students)
    new_model.add(layers.Dense(num_students, activation='relu', name="transfer_layer"))

    new_model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(
                      from_logits=True),
                  metrics=['accuracy'])

    for i in range(epoch):
        history = new_model.fit(x=x, y=y, epochs=1)
        progress.step(1)
        root.update()

    new_model.save(filepath)
    print(filepath)
    print(new_model.summary())


def dir_to_array(dirrect):
    total = 0

    for j, i in enumerate(os.listdir(dirrect)):
        for person in os.listdir(os.path.join(dirrect, i)):
            total += 1

    x = np.zeros((total, 200, 200, 3))
    y = np.zeros((total,))
    print(total)
    total = 0
    student_to_id = {}

    for j, i in enumerate(os.listdir(dirrect)):
        student_to_id[j] = i
        for person in os.listdir(os.path.join(dirrect, i)):
            path = os.path.join(dirrect, i, person)
            print(path)
            # Load the image
            image = cv2.imread(path)

            # convert to rgb
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # resize to reduce no of pixels to reduce time it takes to proccess but
            # still retain meaningfull features to CNN can extract
            image_resized = cv2.resize(image_rgb, (200, 200))

            # turn it into activation of a pixle
            image_np = np.array(image_resized) / 255.
            x[total] = image_np
            y[total] = j
            total += 1

    print("Student to id", student_to_id)
    return x, y.astype("int"), student_to_id

class UseModel():
    def __init__(self, filepath):
        print(filepath)
        self.model = load_model(filepath)

    def process_image(self, images):
        raw_pred = self.model.predict(images)
        results = np.argmax(raw_pred, axis=1)
        mode_result = stats.mode(results)
        return {"result": mode_result.mode, "confidence": np.sum(raw_pred[:, mode_result.mode]) / np.sum(raw_pred)}


