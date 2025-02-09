import pickle
import tensorflow as tf

class ModelPipeline:
    def __init__(self, model_h5_path, model_pckl_path):
        self.model_h5_path = model_h5_path
        self.model_pckl_path = model_pckl_path

    def load_h5_model(self):
        return tf.keras.models.load_model(self.model_h5_path)

    def load_pckl_model(self):
        with open(self.model_pckl_path, 'rb') as f:
            return pickle.load(f)

    def predict(self, data, model_type="h5"):
        if model_type == "h5":
            model = self.load_h5_model()
        elif model_type == "pckl":
            model = self.load_pckl_model()
        else:
            raise ValueError("Invalid model type. Use 'h5' or 'pckl'.")
        return model.predict(data)
