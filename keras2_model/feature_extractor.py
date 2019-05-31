from keras.models import Model
from keras.layers import GlobalAveragePooling2D as GAP2D
from keras.layers import concatenate as concat
import numpy as np
import librosa
import tensorflow as tf

import keras
import kapre

'''print(keras.backend.image_data_format())
print(keras.backend.backend())
print(keras.__version__)
print(kapre.__version__)  # 0c37638'''

SR = 12000  # [Hz]
LEN_SRC = 29.  # [second]
ref_n_src = 12000 * 29


class KerasModel:
    graph = None

    def __init__(self):
        self.feat_extractor = None
        self.prepare_model()

    def load_audio(self, audio_path):
        """Load audio file, shape it and return"""
        src, sr = librosa.load(audio_path, sr=SR, duration=LEN_SRC)
        len_src = len(src)
        if len_src < ref_n_src:
            new_src = np.zeros(ref_n_src)
            new_src[:len_src] = src
            return new_src[np.newaxis, np.newaxis, :]
        else:
            return src[np.newaxis, np.newaxis, :ref_n_src]

    def prepare_model(self):
        model = keras.models.load_model('keras2_model/model_best.hdf5',
                                        custom_objects={'Melspectrogram': kapre.time_frequency.Melspectrogram,
                                                        'Normalization2D': kapre.utils.Normalization2D})

        feat_layer1 = GAP2D()(model.get_layer('elu_1').output)
        feat_layer2 = GAP2D()(model.get_layer('elu_2').output)
        feat_layer3 = GAP2D()(model.get_layer('elu_3').output)
        feat_layer4 = GAP2D()(model.get_layer('elu_4').output)
        feat_layer5 = GAP2D()(model.get_layer('elu_5').output)

        feat_all = concat([feat_layer1, feat_layer2, feat_layer3, feat_layer4, feat_layer5])

        self.feat_extractor = Model(inputs=model.input, outputs=feat_all)
        self.graph = tf.get_default_graph()

    def predict_features(self, audio_path, out_path):
        inp = self.load_audio(audio_path)
        # global self.graph
        with self.graph.as_default():
            feat = self.feat_extractor.predict(inp, batch_size=12)
            np.save(out_path, feat[0])
