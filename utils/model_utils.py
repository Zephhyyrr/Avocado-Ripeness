import os
import tensorflow as tf
from config import MODELS_FOLDER

class ModelHandler:
    def __init__(self):
        self.loaded_models = {}
        
    def get_available_models(self):
        return [f for f in os.listdir(MODELS_FOLDER) if f.endswith('.keras') or f.endswith('.h5')]

    def get_model(self, model_filename):
        if model_filename not in self.loaded_models:
            model_path = os.path.join(MODELS_FOLDER, model_filename)
            if os.path.exists(model_path):
                print(f"Loading {model_filename}...")
                self.loaded_models[model_filename] = tf.keras.models.load_model(model_path)
            else:
                return None
        return self.loaded_models[model_filename]

# Global instance
model_handler = ModelHandler()
