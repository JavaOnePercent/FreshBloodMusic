from django.apps import AppConfig
from keras2_model.feature_extractor import KerasModel
import os


class KerasConfig(AppConfig):
    name = 'keras'
    verbose_name = "keras music feature extraction"
    model: KerasModel = None

    def ready(self):
        KerasConfig.model = KerasModel()
        if 'features' not in os.listdir('.'):
            os.mkdir('features')
        if 'albums' not in os.listdir('features'):
            os.mkdir('features/albums')
        if 'performers' not in os.listdir('features'):
            os.mkdir('features/performers')
        if 'media' not in os.listdir('.'):
            os.mkdir('media')
        if 'albums' not in os.listdir('media'):
            os.mkdir('media/albums')
        if 'playlists' not in os.listdir('media'):
            os.mkdir('media/playlists')
        if 'performers' not in os.listdir('media'):
            os.mkdir('media/performers')
