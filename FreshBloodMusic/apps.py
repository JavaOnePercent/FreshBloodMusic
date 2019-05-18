from django.apps import AppConfig
from keras2_model.feature_extractor import KerasModel


class KerasConfig(AppConfig):
    run_flag = False
    name = 'keras'
    verbose_name = "keras music feature extraction"
    model: KerasModel = None

    def ready(self):
        if not KerasConfig.run_flag:
            KerasConfig.run_flag = True
            KerasConfig.model = KerasModel()
