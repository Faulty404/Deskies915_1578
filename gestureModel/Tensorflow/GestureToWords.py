import tensorflow.keras as tfkeras


class GestureToWord:
    """Model to convert the handsign data to words"""
    
    def __init__(self, name: str, num_layers: int, nodes_per_layer: list[int], activations: list[str]):
        self.name: str = name

        if not (len(nodes_per_layer) == num_layers):
            raise ValueError("Input provided for incorrect number of layers!")

        if not (len(activations) == num_layers):
            raise ValueError(f"Activations provided for only {len(activations)}")

        number_nodes = sum(nodes_per_layer)
        self.model = tfkeras.models.Sequential(
            tfkeras.layers.Dense(nodes_per_layer[0], activation = activations[0], input_shape = ())
        )
        for i in range(1, len(num_layers)):
            self.model.add(tf.Dense())
