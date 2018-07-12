# -*- coding: utf-8 -*-

from logging import getLogger
from datetime import datetime as dt
import math

from keras.callbacks import TensorBoard, ModelCheckpoint, Callback
from keras.utils import Sequence
import numpy as np

from dir_path import train_log_datetime_dir_name, WEIGHTS_PATH_NAME

logger = getLogger(__name__)


def add_tensor_board(cbks):
    date_time = dt.now()
    tensor_board = TensorBoard(log_dir=train_log_datetime_dir_name(date_time), histogram_freq=0, write_graph=True)
    cbks.append()


def add_model_checkpoint(cbks):
    mc = ModelCheckpoint(
        filepath=WEIGHTS_PATH_NAME,
        monitor='val_loss',
        verbose=0,
        save_best_only=True,
        save_weights_only=True,
        mode='auto',
        period=1
    )


class MyCallbacks(Callback):

    def __init__(self):
        super(MyCallbacks, self).__init__()
        pass

    def on_epoch_begin(self, epoch, logs={}):
        # epochの開始時にCallされます。
        pass

    def on_epoch_end(self, epoch, logs={}):
        # epochの終了時にCallされます。
        pass

    def on_batch_begin(self, batch, logs={}):
        # batchの開始時にCallされます。
        pass

    def on_batch_end(self, batch, logs={}):
        # batchの終了時にCallされます。
        pass

    def on_train_begin(self, logs={}):
        # 学習の最初にCallされます。
        pass

    def on_train_end(self, logs={}):
        # 学習の最後にCallされます。
        pass

    def _set_params(self, epoch, logs={}):
        # 学習開始時にCallされ、引数にModel情報が渡されます。あまり使いません。
        # TensorBoardのCallbackではこの時にhistogram_summaryをCallしています。
        pass


class MySequenceForFitGenerator(Sequence):

    def __init__(self, x_set, y_set, batch_size):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size

    def __len__(self):
        return math.ceil(len(self.x) / self.batch_size)

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]

        x = np.array([my_load_process(file_path) for file_path in batch_x])
        y = np.array([my_load_process(file_path) for file_path in batch_y])
        return x, y


if __name__ == '__main__':
    pass
