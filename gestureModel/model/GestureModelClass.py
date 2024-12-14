# ---------------------------------------------------------------------------- #

import tensorflow as tf
import tensorflow.keras as tfkeras

# ---------------------------------------------------------------------------- #

class GestureToWord:
    """Model to convert the handsign data to words"""
    
    def __init__(self, name: str, num_layers: int, nodes_per_layer: list[int], \
                 activations: list[str], num_inputs: int):
        self.name: str = name

        if not (len(nodes_per_layer) == num_layers):
            raise ValueError("Input provided for incorrect number of layers!")

        if not (len(activations) == num_layers):
            raise ValueError(f"Activations provided for only {len(activations)}")

        number_nodes = sum(nodes_per_layer)
        self.model = tfkeras.models.Sequential(
            tfkeras.layers.Dense(
                nodes_per_layer[0], activation = activations[0], input_shape = (num_inputs, )
            )
        )
        for i in range(1, num_layers):
            self.model.add(tfkeras.Dense(nodes_per_layer[i], activation = activations[i]))


    def compile(self, optimiser, loss_type: str, metrics_vals: list[str]) -> None:
        self.model.compile(optimizer = optimiser, loss = loss_type, metrics = metrics_vals)
        return

    def fit_and_get_history(self, X_train, y_train, epochs, batch, validation_split: float, verbose_level):
        history = self.model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch,
            validation_split=validation_split,
            verbose=verbose_level
        )
        return history

    def predict(self, X_test):
        y_pred = self.model.predict(X_test)
        return y_pred

    def evaluate(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test)
        return loss, accuracy

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.model.load(filepath)
