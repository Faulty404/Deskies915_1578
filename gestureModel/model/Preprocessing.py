#---------------------------------------------------------------------------- #

import pandas as pd
import numpy as np
import sys

# ---------------------------------------------------------------------------- #

if len(sys.argv) != 2:
    if len(sys.argv) < 2:
        print("Too few aruments provided!")
    else:
        print("Too many aruments provided!")
    print("Usage: python Preprocessing.py <path_to_csv>")
    exit()


filename: str = sys.argv[1]
df = pd.read_csv(filename)
cols = pd.columns

one_hot = pd.get_dummies(df['element_class'])
num_classes = len(one_hot.columns)
df = pd.concat([df.drop('element_class', axis=1), one_hot], axis=1)

import tensorflow as tf
import numpy as np

def scale_dataset_tf_with_one_hot(dataframe, oversample=False):
    X = dataframe.iloc[:, :-num_classes].values  # Features
    y = dataframe.iloc[:, -num_classes:].values  # One-hot encoded labels

    if oversample:
        # Decode one-hot labels to class indices
        y_classes = np.argmax(y, axis=1)

        # Perform oversampling
        unique_classes, class_counts = np.unique(y_classes, return_counts=True)
        max_count = np.max(class_counts)
        
        X_resampled = []
        y_resampled = []

        for cls in unique_classes:
            X_class = X[y_classes == cls]
            y_class = y[y_classes == cls]

            # Replicate samples to match the max class count
            num_samples_to_add = max_count - len(X_class)
            if num_samples_to_add > 0:
                replicated_indices = np.random.choice(len(X_class), num_samples_to_add)
                X_resampled.append(np.vstack([X_class, X_class[replicated_indices]]))
                y_resampled.append(np.vstack([y_class, y_class[replicated_indices]]))
            else:
                X_resampled.append(X_class)
                y_resampled.append(y_class)

        # Combine all classes
        X = np.vstack(X_resampled)
        y = np.vstack(y_resampled)

    # Normalize features using TensorFlow
    X = tf.convert_to_tensor(X, dtype=tf.float32)
    scaler = tf.keras.layers.Normalization(axis=-1)
    scaler.adapt(X)
    X = scaler(X)

    # Combine scaled features and one-hot encoded labels
    y = tf.convert_to_tensor(y, dtype=tf.float32)
    data = tf.concat([X, y], axis=1)

    return data.numpy(), X.numpy(), y.numpy()

train, X_train, y_train = scale_dataset(train, True)
test, X_test, y_test = scale_dataset(test)
train = pd.DataFrame(train, columns = cols)
test = pd.DataFrame(test, columns = cols)

PreprocessedData = (X_train, y_train, X_test, y_test)
