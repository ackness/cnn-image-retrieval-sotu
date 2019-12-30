import os

import cv2
import numpy as np

import h5py
import tensorflow as tf
from keras.backend import clear_session
from vision.vgg16 import VGGNet

os.environ['CUDA_VISIBLE_DEVICES'] = '2'


def get_image_search(im_file, model_name='model/holiday_feature.h5', return_num=10):
    h5f = h5py.File(model_name, 'r')
    feats = h5f['dataset_1'][:]
    imgNames = h5f['dataset_2'][:]
    h5f.close()

    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.1  # 占用GPU10%的显存
    session = tf.Session(config=config)

    model = VGGNet()
    q_vector = model.extract_feat(im_file)
    # print("清除训练模型！")
    clear_session()
    tf.reset_default_graph()

    scores = np.dot(q_vector, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]

    maxres = return_num
    im_list = [str(imgNames[index].decode())
               for i, index in enumerate(rank_ID[0:maxres])]

    im_score = [str(rank_score[i]) for i in range(maxres)]
    result_dict = dict(zip(im_list, im_score))
    return result_dict, im_list, im_score
