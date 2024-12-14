# ---------------------------------------------------------------------------- #

import tensorflow as tf
import tensorflow.keras as tf

# ---------------------------------------------------------------------------- #

from GestureModelClass import GestureToWord as NN
from Preprocessing import PreprocessedData

# ---------------------------------------------------------------------------- #

X_train, y_train, X_test, y_test = PreprocessedData

model = NN(
    name="HandSignModel",
    num_layers=3,
    nodes_per_layer=[64, 128, 64],
    activations=["relu", "relu", "softmax"],
    num_inputs=10
)

model.compile(optimiser=tf.optimizers.Adam(0.2), loss_type="categorical_crossentropy", metrics_vals=["accuracy"])
history = model.fit_and_get_history(X_train, y_train, epochs=50, batch=32, validation_split=0.2, verbose_level=1)
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")


