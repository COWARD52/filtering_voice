# coding:gbk
import librosa
import os
from random import shuffle
import numpy as np
from sklearn import svm
import sklearn
from sklearn.externals import joblib
from app.tool.transform import Voice2Word
from app.tool.word_classify import classify

data_feature = []


def getData(filename, mfcc_feature_num=16):
    y, sr = librosa.load(filename)  # filename indicate the path of wav file

    mfcc_feature = librosa.feature.mfcc(y, sr, n_mfcc=16)
    zcr_feature = librosa.feature.zero_crossing_rate(y)
    energy_feature = librosa.feature.rmse(y)
    rms_feature = librosa.feature.rmse(y)

    mfcc_feature = mfcc_feature.T.flatten()[:mfcc_feature_num]
    zcr_feature = zcr_feature.flatten()
    energy_feature = energy_feature.flatten()
    rms_feature = rms_feature.flatten()

    zcr_feature = np.array([np.mean(zcr_feature)])
    energy_feature = np.array([np.mean(energy_feature)])
    rms_feature = np.array([np.mean(rms_feature)])

    data_feature.append(np.concatenate((mfcc_feature, zcr_feature, energy_feature, rms_feature)))

    return np.array(data_feature)


def get(filename):
    clf = joblib.load("train_model.m")  # load model
    print(filename)
    processed_data = getData(filename)  # getData() transform wav file  to numpy array, as input
    pre = clf.predict(processed_data)[0]  # predict
    print('语音音频分析:')
    if pre:
        status = 0
        print('音频正常')
        print('语音语义分析:')
        word = Voice2Word(filename)
        word = word['result'][0].strip().rstrip('。')
        word_result = classify(word)
        print(word_result)
    else:
        status = 1
        print('检测到机器学习级别攻击-001')
    return status
